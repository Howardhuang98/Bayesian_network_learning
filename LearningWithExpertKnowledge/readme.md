# 融合专家知识的贝叶斯网络结构学习算法  
score-based learning：  
criterion：BIC with expert score，greedy hill climb.  
本算法可以融合专家知识矩阵来提高贝叶斯网络结构学习的精度，提供了BIC评分的改进形式  
算法由三个class组成，分别为estimator，expert，DAG组成。后期可以对estimator.score_function以及expert进行重写，对该算法进行改进。

expert专家部分  
 &emsp;|----think  
graph图部分  
 &emsp;|----get_parents  
 &emsp;|----save_to_png  
estimator算法主体  
 &emsp;|----run   
 &emsp;|----add_weight_to_edges  
 &emsp;|----centrality_of_nodes  
run/与data/  
 &emsp;|----放置运行脚本与数据  
results/  
 &emsp;|----放置网络结构结果   文件格式为xlsx，可以直接放置在Cytoscape里进行可视化   https://cytoscape.org/   

## Example with asian dataset
```python
from LearningWithExpertKnowledge.estimator import * 
from LearningWithExpertKnowledge.expert import *
if __name__ == '__main__':          
   asian_data = pd.read_csv(r"../data/asian.csv", index_col=0)     
   expert_data = pd.read_csv(r"../data/asian_expert.csv", index_col=0)     
   huang = ExpertKnowledge(data=expert_data)     # 实例化专家huang
   est = Estimator(data=asian_data, expert=huang, k=100000)     # 将数据，专家，超参数传入estimator
   est.run()     # 运行估计器，每次迭代结果可以在log.txt中实时查看
   est.DAG.save_to_png(weight=False)     # 保存DAG为png文件
   print(est.DAG.edges)     # 打印结果
```




## Reference：
高晓光, 叶思懋, 邸若海, 等. 基于融合先验方法的贝叶斯网络结构学习[J]. 系统工程与电子技术, 2018, 40(4): 790-796.