from itertools import permutations
from LearningWithExpertKnowledge.expert import *
from LearningWithExpertKnowledge.graph import DAG
import networkx as nx
import numpy as np
from math import log


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

    def _collect_state_names(self, variable):
        """
        收集该变量的状态名
        :param variable:
        :return:
        """
        states = sorted(list(self.data.loc[:, variable].dropna().unique()))
        return states

    def state_counts(self, variable, parents=[]):
        """

        :param variable:
        :param parents:
        :return:
        """
        parents = list(parents)

        # ignores either any row containing NaN, or only those where the variable or its parents is NaN
        data = self.data

        if not parents:
            # count how often each state of 'variable' occured
            state_count_data = data.loc[:, variable].value_counts()
            state_counts = (
                state_count_data.reindex(self.state_names[variable])
                    .fillna(0)
                    .to_frame()
            )

        else:
            parents_states = [self.state_names[parent] for parent in parents]
            # count how often each state of 'variable' occured, conditional on parents' states
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
        score = -np.log(-score+1)

        # 考虑样本影响：
        score *= 10000/sample_size

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

        score = np.sum(log_likelihoods)
        ################
        #
        #  log似然的计算
        #  加上这段代码就是BIC评分
        #  score -= 0.5 * log(sample_size) * num_parents_states * (var_cardinality - 1)
        #
        ################
        score += self.expert_score(variable=variable,parents=parents)

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
            if not nx.has_path(DAG, Y, X):
                operation = ("+", (X, Y))
                if operation not in tabu_list:
                    old_parents = DAG.get_parents(Y)
                    new_parents = old_parents + [X]
                    score_delta = self.score_function(Y, new_parents) - self.score_function(Y, old_parents)
                    yield (operation, score_delta)


if __name__ == '__main__':
    chen_data = pd.DataFrame({
        "A": [0, 0.8, 0.7, 0.3],
        "B": [0.1, 0, 0.3, 0.9],
        "C": [0.5, 0.2, 0, 0.1],
        "D": [0.3, 0.2, 0.1, 0]
    }, index=["A", "B", "C", "D"])
    chen = ExpertKnowledge(data=chen_data)
    data = pd.read_excel(r"./data/data.xlsx")
    a = Estimator(data=data, expert=chen)
    a.legal_operations(tabu_list=[])
    print(a._collect_state_names("A"))
    print(a.state_counts("A", "B"))
    print(a.score_function("A", "B"))
    print(a.expert_score("A", "B"))
