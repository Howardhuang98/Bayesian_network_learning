from LearningWithExpertKnowledge.estimator import *
from LearningWithExpertKnowledge.expert import *
from LearningWithExpertKnowledge.graph import *
import pandas as pd

if __name__ == '__main__':
    """
    run asian dataset
    
    """
    asian_data = pd.read_csv(r"../data/asian.csv",index_col=0)
    expert_data =