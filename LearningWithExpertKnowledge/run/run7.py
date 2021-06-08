from LearningWithExpertKnowledge.estimator import *

if __name__ == '__main__':
    """

    """
    g = DAG([('LS_YJL', 'FL_ZKL'), ('LS_YJL', 'ZJ_D'), ('LS_YJL', 'ZJ_U'), ('LS_YJL', 'ZX_IN'), ('LS_YJL', 'ZX_OUT'),
             ('θ', 'FL_ZKL'), ('θ', 'ZJ_D'), ('θ', 'ZJ_U'), ('θ', 'JX_OUT'), ('θ', 'JX_IN'), ('θ', 'ZX_IN'),
             ('θ', 'ZX_OUT'), ('θ', 'D12'), ('T1', 'θ'), ('H2', 'D15'), ('H2', 'D8'), ('SR2', 'D15'), ('SR2', 'T2'),
             ('SR2', 'θ'), ('D17', 'D12'), ('D14', 'D15'), ('D14', 'D12'), ('D14', 'D10'), ('D13', 'ZX_IN'),
             ('D13', 'ZX_OUT'), ('D13', 'ZJ_D'), ('D13', 'ZJ_U'), ('D13', 'D15'), ('D13', 'θ'), ('D13', 'FL_ZKL'),
             ('D13', 'D8'), ('D13', 'D12'), ('D13', 'D10'), ('D12', 'D15'), ('D12', 'D8'), ('D11', 'ZX_IN'),
             ('D11', 'ZX_OUT'), ('D11', 'ZJ_D'), ('D11', 'ZJ_U'), ('D11', 'FL_ZKL'), ('D10', 'D15'), ('D10', 'D8'),
             ('D9', 'θ'), ('D9', 'D8'), ('D7', 'D12'), ('D3', 'D8'), ('D3', 'D10'), ('D2', 'θ'), ('D1', 'θ'),
             ('D1', 'D12')]
            )
    g.to_excel(r"dag7.xlsx")
