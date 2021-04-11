from LearningWithExpertKnowledge.estimator import *
from LearningWithExpertKnowledge.expert import *
from LearningWithExpertKnowledge.graph import *
import pandas as pd

if __name__ == '__main__':
    """
    run asian dataset
    
    """
    asian_data = pd.read_csv(r"../data/asian.csv", index_col=0)
    expert_data = pd.read_csv(r"../data/asian_expert.csv", index_col=0)
    huang = ExpertKnowledge(data=expert_data)
    est = Estimator(data=asian_data, expert=huang)
    est.run()
    est.add_weight_to_edges()
    est.DAG.save_to_png(weight=False)
    print(est.centrality_of_nodes())
