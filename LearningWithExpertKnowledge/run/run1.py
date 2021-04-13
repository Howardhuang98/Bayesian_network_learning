from LearningWithExpertKnowledge.estimator import *
from LearningWithExpertKnowledge.expert import *

if __name__ == '__main__':
    """
    run result30.csv
    max_iter=10000
    """
    asian_data = pd.read_csv(r"../data/result30.csv", index_col=0)
    expert_data = pd.read_csv(r"../data/rpv_expert.csv", index_col=0)
    huang = ExpertKnowledge(data=expert_data)
    est = Estimator(data=asian_data, expert=huang, k=100000)
    est.run(max_iter=1e4)
    est.DAG.save_to_png(weight=False)
    print(est.centrality_of_nodes())
