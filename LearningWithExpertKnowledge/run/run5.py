from LearningWithExpertKnowledge.estimator import *
from LearningWithExpertKnowledge.expert import *

if __name__ == '__main__':
    """
    [('LS_YJL', 'FL_ZKL'), ('LS_YJL', 'ZJ_D'), ('LS_YJL', 'ZJ_U'), ('LS_YJL', 'ZX_IN'), ('LS_YJL', 'ZX_OUT'), ('θ', 'FL_ZKL'), ('θ', 'ZJ_D'), ('θ', 'ZJ_U'), ('θ', 'JX_OUT'), ('θ', 'JX_IN'), ('θ', 'ZX_IN'), ('θ', 'ZX_OUT'), ('θ', 'SR2'), ('θ', 'H3'), ('T2', 'H3'), ('T1', 'SR2'), ('H3', 'D17'), ('H3', 'D8'), ('H3', 'D7'), ('H2', 'H3'), ('SR2', 'T2'), ('SR2', 'H3'), ('SR2', 'D17'), ('SR2', 'D8'), ('SR2', 'D7'), ('D15', 'SR2'), ('D14', 'D8'), ('D13', 'ZX_IN'), ('D13', 'ZX_OUT'), ('D13', 'ZJ_D'), ('D13', 'ZJ_U'), ('D13', 'SR2'), ('D13', 'H3'), ('D13', 'FL_ZKL'), ('D13', 'D17'), ('D12', 'D8'), ('D11', 'ZX_IN'), ('D11', 'ZX_OUT'), ('D11', 'ZJ_D'), ('D11', 'ZJ_U'), ('D11', 'SR2'), ('D11', 'FL_ZKL'), ('D10', 'D8'), ('D10', 'D7'), ('D9', 'D17'), ('D2', 'H3'), ('D2', 'D17'), ('D1', 'SR2'), ('D1', 'D17'), ('D1', 'D8')]

    """
    data = pd.read_csv(r"../rpv_data/data3.csv")
    expert_data = pd.read_excel(r"../rpv_data/expert_knowledge.xlsx", index_col=0)
    huang = ExpertKnowledge(data=expert_data)
    est = Estimator(data=data, expert=huang, k=10e-5)
    est.run(max_iter=50)
    print(est.DAG.edges)