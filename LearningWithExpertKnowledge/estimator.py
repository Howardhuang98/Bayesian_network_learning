from itertools import permutations
from LearningWithExpertKnowledge.expert import *
from LearningWithExpertKnowledge.graph import DAG
import networkx as nx
import numpy as np
from tqdm import trange
from collections import deque
import logging


class Estimator:
    def __init__(self, data: pd.DataFrame, expert: ExpertKnowledge):
        self.data = data
        self.expert = expert
        self.DAG = DAG()
        self.vars = data.columns
        self.state_names = {
            var: self._collect_state_names(var) for var in self.vars
        }
        # 检查data的columns与expert的columns是否符合
        for var in self.vars:
            if var in data.columns:
                continue
            else:
                raise ValueError("专家信息与data不符！")
        # log 文件设置
        logging.basicConfig(filename='log.txt', level=0, filemode="w", format="")
        logging.info("*****日志文件*****")
        logging.info("数据预览：")
        logging.info(self.data.head(5))
        logging.info("专家知识预览：")
        logging.info(self.expert.data)

    def _collect_state_names(self, variable):
        """
        收集该变量的状态名
        :param variable:
        :return:
        """
        states = sorted(list(self.data.loc[:, variable].dropna().unique()))
        return states

    def state_counts(self, variable, parents=None):
        """

        :param variable:
        :param parents:
        :return:
        """
        if parents is None:
            parents = []
        parents = list(parents)

        # ignores either any row containing NaN, or only those where the variable or its parents is NaN
        data = self.data

        if not parents:
            # count how often each state of 'variable' occurred
            state_count_data = data.loc[:, variable].value_counts()
            state_counts = (
                state_count_data.reindex(self.state_names[variable]).fillna(0).to_frame()
            )

        else:
            parents_states = [self.state_names[parent] for parent in parents]
            # count how often each state of 'variable' occurred, conditional on parents' states
            state_count_data = (
                data.groupby([variable] + parents).size().unstack(parents)
            )
            if not isinstance(state_count_data.columns, pd.MultiIndex):
                state_count_data.columns = pd.MultiIndex.from_arrays(
                    [state_count_data.columns]
                )

            # reindex rows & columns to sort them and to add missing ones
            # missing row    = some state of 'variable' did not occur in data
            # missing column = some state configuration of current 'variable's parents
            #                  did not occur in data
            row_index = self.state_names[variable]
            column_index = pd.MultiIndex.from_product(parents_states, names=parents)
            state_counts = state_count_data.reindex(
                index=row_index, columns=column_index
            ).fillna(0)

        return state_counts

    def expert_score(self, variable, parents):
        """
        专家评分部分
        :param variable:
        :param parents:
        :return:
        """
        parents = set(parents)
        sample_size = len(self.data)
        # 专家分数计算
        score = 0
        for node in self.vars:
            thinks = self.expert.think(variable, node)
            if node == variable:
                continue
            else:
                if node in parents:
                    score += thinks[1] - 0.5 * thinks[2]
                else:
                    score += 0.5 * thinks[2]
        # 可能性两极化处理
        score_max = len(self.vars) - 1
        score_min = -0.5 * (len(self.vars) - 1)
        score = -np.log(-(score - score_min) / (score_max - score_min) + 1)

        # 考虑样本影响：
        score *= 1000000 / sample_size

        return score

    def score_function(self, variable, parents):
        """

        :param variable:
        :param parents:
        :return:
        """
        var_states = self.state_names[variable]
        var_cardinality = len(var_states)
        state_counts = self.state_counts(variable, parents)
        sample_size = len(self.data)
        num_parents_states = float(state_counts.shape[1])

        counts = np.asarray(state_counts)
        log_likelihoods = np.zeros_like(counts, dtype=np.float_)

        # Compute the log-counts
        np.log(counts, out=log_likelihoods, where=counts > 0)

        # Compute the log-conditional sample size
        log_conditionals = np.sum(counts, axis=0, dtype=np.float_)
        np.log(log_conditionals, out=log_conditionals, where=log_conditionals > 0)
        # Compute the log-likelihoods
        log_likelihoods -= log_conditionals
        log_likelihoods *= counts

        likelihood_score = np.sum(log_likelihoods)
        ################
        #
        #  log似然的计算
        #  加上这段代码就是BIC评分
        #  score -= 0.5 * log(sample_size) * num_parents_states * (var_cardinality - 1)
        #
        ################
        expert_score = self.expert_score(variable=variable, parents=parents)
        score = likelihood_score + expert_score
        logging.info("{}与{}组成的部分结构，得分为：{}+{}={}".format(variable, parents, likelihood_score, expert_score, score))

        return score

    def legal_operations(self, tabu_list):
        tabu_list = set(tabu_list)
        potential_new_edges = (
                set(permutations(self.vars, 2))
                - set(self.DAG.edges())
                - set([(Y, X) for (X, Y) in self.DAG.edges()])
        )
        for (X, Y) in potential_new_edges:
            # Check if adding (X, Y) will create a cycle.
            if not nx.has_path(self.DAG, Y, X):
                operation = ("+", (X, Y))
                if operation not in tabu_list:
                    old_parents = self.DAG.get_parents(Y)
                    new_parents = old_parents + [X]
                    score_delta = self.score_function(Y, new_parents) - self.score_function(Y, old_parents)
                    yield (operation, score_delta)

        for (X, Y) in self.DAG.edges():
            operation = ("-", (X, Y))
            if operation not in tabu_list:
                old_parents = self.DAG.get_parents(Y)
                new_parents = old_parents[:]
                new_parents.remove(X)
                score_delta = self.score_function(Y, new_parents) - self.score_function(Y, old_parents)
                yield (operation, score_delta)

        for (X, Y) in self.DAG.edges():
            # Check if flipping creates any cycles
            if not any(
                    map(lambda path: len(path) > 2, nx.all_simple_paths(self.DAG, X, Y))
            ):
                operation = ("flip", (X, Y))
                if operation not in tabu_list:
                    old_X_parents = self.DAG.get_parents(X)
                    old_Y_parents = self.DAG.get_parents(Y)
                    new_X_parents = old_X_parents + [Y]
                    new_Y_parents = old_Y_parents[:]
                    new_Y_parents.remove(X)
                    score_delta = (
                            self.score_function(X, new_X_parents)
                            + self.score_function(Y, new_Y_parents)
                            - self.score_function(X, old_X_parents)
                            - self.score_function(Y, old_Y_parents)
                    )
                    yield (operation, score_delta)

    def run(self, epsilon=1e-4, max_iter=1e6):
        """

        :param epsilon:
        :param max_iter:
        :return:
        """
        ########
        # 初始检查：略去
        ########
        # 初始化
        start_dag = self.DAG
        start_dag.add_nodes_from(self.vars)
        tabu_list = deque(maxlen=100)
        current_model = start_dag
        # 每次迭代，找到最佳的 (operation, score_delta)
        iteration = trange(int(max_iter))
        for _ in iteration:
            logging.debug(current_model.edges)
            best_operation, best_score_delta = max(
                self.legal_operations(tabu_list),
                key=lambda t: t[1],
            )
            logging.info("搜索到的最佳操作为：{}".format(best_operation))
            if best_operation is None or best_score_delta < epsilon:
                break
            elif best_operation[0] == "+":
                current_model.add_edge(*best_operation[1])
                tabu_list.append(("-", best_operation[1]))
            elif best_operation[0] == "-":
                current_model.remove_edge(*best_operation[1])
                tabu_list.append(("+", best_operation[1]))
            elif best_operation[0] == "flip":
                X, Y = best_operation[1]
                current_model.remove_edge(X, Y)
                current_model.add_edge(Y, X)
                tabu_list.append(best_operation)
        return current_model

    def mic_of_edge(self, u, v):
        """
        计算一对边之间的相关性，MIC
        参考文献：Detecting novel associations in large data sets[J]. science, 2011, 334(6062): 1518-1524.
        :param u:
        :param v:
        :return:
        """
        pass

    def corr_of_edges(self, u, v):
        """
        计算两个节点之间的相关系数
        ps:相关系数衡量随机变量X与Y相关程度的一种方法，相关系数的取值范围是[-1,1]。
        相关系数的绝对值越大，则表明X与Y相关度越高。 当X与Y线性相关时，相关系数取值为1（正线性相关）或-1（负线性相关）
        :param u:
        :param v:
        :return:
        """
        var1 = self.data[u].values
        var2 = self.data[v].values
        corr = np.corrcoef(var1, var2)[0][1]
        return corr

    def add_weight_to_edges(self):
        """
        给每条边，根据corr增加权重,经过变换：
        100：最远，相关性最弱
        0：最近，相关性最强
        :return:
        """
        if self.DAG.edges is None:
            print("No edge was found!")
            return None
        for edge in self.DAG.edges:
            weight = (1 - abs(self.corr_of_edges(edge[0], edge[1]))) * 100
            self.DAG[edge[0]][edge[1]]["weight"] = weight

    def importance_of_node(self,node):
        """
        计算该节点的重要度
        参考文献：复杂网络中节点重要度评估的节点收缩方法[D]. , 2006.
        :param node:
        :return:
        """
        # 计算距离矩阵
        distance_matrix = nx.floyd_warshall_numpy(self.DAG,weight="weight")
        # 计算初始网络的凝聚度
        where_are_inf = np.isinf(distance_matrix)
        _distance_matrix = distance_matrix
        _distance_matrix[where_are_inf] = 0
        cohesion_of_initial_network = (len(self.DAG.nodes)-1)/_distance_matrix.sum()
        # 对node进行节点收缩
        # 当对node进行节点收缩时，相当于把node的所有相邻节点到node的距离变为0

    def centrality_of_nodes(self):
        centrality = nx.katz_centrality(self.DAG,weight="weight")
        return centrality

        return cohesion_of_initial_network







if __name__ == '__main__':
    chen_data = pd.DataFrame({
        "A": [0, 0.8, 0, 0.3],
        "B": [0.1, 0, 0.3, 0.9],
        "C": [1, 0.2, 0, 0.1],
        "D": [0.3, 0.2, 0.1, 0]
    }, index=["A", "B", "C", "D"])
    print(chen_data)
    chen = ExpertKnowledge(data=chen_data)
    data = pd.read_excel(r"./data/data.xlsx")
    a = Estimator(data=data, expert=chen)
    a.run()
    print(a.corr_of_edges('A', 'B'))
    a.add_weight_to_edges()
    print(a.DAG.edges.data())
    print(a.centrality_of_nodes())
