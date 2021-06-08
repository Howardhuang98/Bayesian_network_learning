import networkx as nx
import matplotlib.pyplot as plt
g = nx.DiGraph([('LS_YJL', 'FL_ZKL'), ('LS_YJL', 'ZJ_D'), ('LS_YJL', 'ZJ_U'), ('LS_YJL', 'ZX_IN'), ('LS_YJL', 'ZX_OUT'),
                ('LS_YJL', 'SR2'), ('FL_ZKL', 'D13'), ('ZJ_D', 'T2'), ('ZJ_U', 'SR2'), ('ZJ_U', 'D15'),
                ('JX_IN', 'ZX_OUT'), ('ZX_OUT', 'D12'), ('θ', 'FL_ZKL'), ('θ', 'ZJ_D'), ('θ', 'ZJ_U'), ('θ', 'JX_OUT'),
                ('θ', 'JX_IN'), ('θ', 'ZX_IN'), ('θ', 'ZX_OUT'), ('θ', 'H3'), ('T2', 'H3'), ('T1', 'D12'), ('H2', 'H3'),
                ('H1', 'D15'), ('SR2', 'T2'), ('SR2', 'H3'), ('D17', 'T2'), ('D17', 'D15'), ('D15', 'SR2'),
                ('D14', 'D15'), ('D14', 'D12'), ('D13', 'ZX_IN'), ('D13', 'ZX_OUT'), ('D13', 'ZJ_D'), ('D13', 'ZJ_U'),
                ('D13', 'SR2'), ('D13', 'D15'), ('D12', 'D15'), ('D11', 'ZX_IN'), ('D11', 'ZX_OUT'), ('D11', 'ZJ_D'),
                ('D11', 'ZJ_U'), ('D11', 'T2'), ('D11', 'D12'), ('D9', 'D12'), ('D8', 'T2'), ('D7', 'SR2'),
                ('D7', 'D12'), ('D3', 'T2'), ('D2', 'SR2')]
               )
nx.draw_networkx(g)
plt.show()