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
        else:
            out_str = "Cycles are not allowed in a DAG."
            out_str += "\nEdges indicating the path taken for a loop: "
            out_str += "".join([f"({u},{v}) " for (u, v) in cycles])
            raise

