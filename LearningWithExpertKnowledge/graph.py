import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd


class DAG(nx.DiGraph):
    def __init__(self, edges=None):
        super(DAG, self).__init__(edges)
        # 检查是否出现cycles
        cycles = []
        try:
            cycles = list(nx.find_cycle(self))
        except nx.NetworkXNoCycle:
            pass

    def get_parents(self, node):
        """
        返回该node的parents节点
        :param node:
        :return:
        """
        return list(self.predecessors(node))

    def save_to_png(self, weight=True):
        position = nx.random_layout(self)
        nx.draw_networkx(self, pos=position, with_labels=True)
        if weight:
            nx.draw_networkx_edge_labels(self, pos=position,
                                         edge_labels={(a, b): round(c["weight"], 2) for (a, b, c) in self.edges.data()})
        plt.savefig("DAG.png")

    def to_excel(self,io):
        edge_list = self.edges
        edges_data = pd.DataFrame(columns=['source','target'])
        for edge_pair in edge_list:
            edges_data.loc[edges_data.shape[0]]={'source':edge_pair[0],'target':edge_pair[1]}
        edges_data.to_excel(io)

        return None
