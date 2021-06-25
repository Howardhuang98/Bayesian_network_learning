from LearningWithExpertKnowledge.estimator import *

if __name__ == '__main__':
    """

    """
    g = DAG([('LS_YJL', 'FL_ZKL'), ('LS_YJL', 'ZJ_D'), ('LS_YJL', 'ZJ_U'), ('LS_YJL', 'ZX_IN'), ('LS_YJL', 'ZX_OUT'),
             ('θ', 'JX_OUT'), ('θ', 'JX_IN'), ('θ', 'FL_ZKL'), ('θ', 'ZJ_D'), ('θ', 'ZJ_U'), ('θ', 'ZX_IN'),
             ('θ', 'ZX_OUT'), ('θ', 'D15'), ('T1', 'θ'), ('H2', 'D8'), ('H1', 'D15'), ('SR2', 'T2'), ('SR2', 'θ'),
             ('D15', 'ZX_IN'), ('D15', 'ZJ_D'), ('D14', 'ZX_IN'), ('D14', 'ZX_OUT'), ('D14', 'ZJ_U'), ('D14', 'ZJ_D'),
             ('D14', 'FL_ZKL'), ('D14', 'D15'), ('D13', 'ZX_IN'), ('D13', 'ZX_OUT'), ('D13', 'ZJ_U'), ('D13', 'FL_ZKL'),
             ('D13', 'θ'), ('D13', 'D8'), ('D13', 'D15'), ('D12', 'ZX_OUT'), ('D12', 'ZJ_D'), ('D12', 'ZJ_U'),
             ('D12', 'FL_ZKL'), ('D12', 'D8'), ('D12', 'D15'), ('D11', 'ZJ_U'), ('D11', 'ZJ_D'), ('D11', 'ZX_IN'),
             ('D11', 'ZX_OUT'), ('D10', 'D8'), ('D9', 'θ'), ('D9', 'D8'), ('D3', 'D8'), ('D2', 'θ'), ('D1', 'θ')]

            )
    g.to_excel(r"../results/dag7.xlsx")
