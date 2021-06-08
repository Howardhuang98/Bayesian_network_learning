import pandas as pd

from LearningWithExpertKnowledge.estimator import *
from LearningWithExpertKnowledge.expert import *

if __name__ == '__main__':
    """
    run result30.csv
    max_iter=50

    """
    data = pd.read_csv(r"../rpv_data/data3.csv")
    expert_data = pd.read_excel(r"../rpv_data/expert_knowledge.xlsx", index_col=0)
    huang = ExpertKnowledge(data=expert_data)
    est = Estimator(data=data, expert=huang, k=1)
    print(est.expert_score('D1',['LS_YJL']))
    print(est.expert_score('FL_JXWYL',['D2']))
    print(est.expert_score('FL_ZKL',['LS_YJL']))
