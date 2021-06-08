from LearningWithExpertKnowledge.estimator import *
from LearningWithExpertKnowledge.expert import *

if __name__ == '__main__':
    """
   
    """
    data = pd.read_csv(r"../rpv_data/data3.csv")
    expert_data = pd.read_excel(r"../rpv_data/expert_knowledge2.xlsx", index_col=0)
    huang = ExpertKnowledge(data=expert_data)
    est = Estimator(data=data, expert=huang, k=10e-5)
    est.run(max_iter=50)
    est.DAG.to_excel(r"../results/dag6.xlsx")