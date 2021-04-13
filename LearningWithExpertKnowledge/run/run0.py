from LearningWithExpertKnowledge.estimator import *
from LearningWithExpertKnowledge.expert import *

if __name__ == '__main__':
    """
    run asian dataset
    Asian data is not numerical, so can not run add_weight_to_edges()
    此时k对结果影响很大哦！
    """
    asian_data = pd.read_csv(r"../data/asian.csv", index_col=0)
    expert_data = pd.read_csv(r"../data/asian_expert.csv", index_col=0)
    huang = ExpertKnowledge(data=expert_data)
    est = Estimator(data=asian_data, expert=huang, k=100000)
    est.run()
    est.DAG.save_to_png(weight=False)
    print(est.centrality_of_nodes())
