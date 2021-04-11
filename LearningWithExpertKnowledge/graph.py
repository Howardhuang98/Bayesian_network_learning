import matplotlib.pyplot as plt
import networkx as nx


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
