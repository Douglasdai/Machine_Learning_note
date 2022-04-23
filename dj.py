import networkx as nx
import pylab
import numpy as np

row  =np.array([0,1,1,1,2,2,3,4 ,5,6,6,7,7 ,9 ,10,10,11])
col  =np.array([1,2,4,5,5,7,4,11,6,7,9,8,12,10,11,12,12])
value=np.array([3,5,5,4,4,6,6,6 ,3,2,6,2,7 ,1 ,3 ,1 ,4])

#生成一个空的无向图
G=nx.Graph()
#为这个网络添加节点
for i in range(0,np.size(col)+1):
    G.add_node(i)
#'在网络中添加带权中的边...
for i in range(np.size(row)):
    G.add_weighted_edges_from([(row[i],col[i],value[i])])

#给网路设置布局...
pos=nx.shell_layout(G)
nx.draw(G,pos,with_labels=True, node_color='white', edge_color='red', node_size=400, alpha=0.5 )
pylab.title('Self_Define Net',fontsize=15)
pylab.show()

'''
Shortest Path with dijkstra_path
'''
#dijkstra方法寻找最短路径：
path=nx.dijkstra_path(G, source=0, target=2)
print('节点0到2的路径：', path)
#dijkstra方法寻找最短距离：
distance=nx.dijkstra_path_length(G, source=0, target=2)
print('节点0到2的距离为：', distance)

path=nx.dijkstra_path(G, source=0, target=3)
print('节点0到3的路径：', path)
distance=nx.dijkstra_path_length(G, source=0, target=3)
print('节点0到3的距离为：', distance)

path=nx.dijkstra_path(G, source=0, target=8)
print('节点0到8的路径：', path)
distance=nx.dijkstra_path_length(G, source=0, target=8)
print('节点0到8的距离为：', distance)

path=nx.dijkstra_path(G, source=0, target=9)
print('节点0到9的路径：', path)
distance=nx.dijkstra_path_length(G, source=0, target=9)
print('节点0到9的距离为：', distance)

path=nx.dijkstra_path(G, source=2, target=3)
print('节点2到3的路径：', path)
distance=nx.dijkstra_path_length(G, source=2, target=3)
print('节点2到3的距离为：', distance)

path=nx.dijkstra_path(G, source=2, target=8)
print('节点2到8的路径：', path)
distance=nx.dijkstra_path_length(G, source=2, target=8)
print('节点2到8的距离为：', distance)

path=nx.dijkstra_path(G, source=2, target=9)
print('节点2到9的路径：', path)
distance=nx.dijkstra_path_length(G, source=2, target=9)
print('节点2到9的距离为：', distance)

path=nx.dijkstra_path(G, source=3, target=8)
print('节点3到8的路径：', path)
distance=nx.dijkstra_path_length(G, source=3, target=8)
print('节点3到8的距离为：', distance)

path=nx.dijkstra_path(G, source=3, target=9)
print('节点3到9的路径：', path)
distance=nx.dijkstra_path_length(G, source=3, target=9)
print('节点3到9的距离为：', distance)


path=nx.dijkstra_path(G, source=8, target=9)
print('节点8到9的路径：', path)
distance=nx.dijkstra_path_length(G, source=8, target=9)
print('节点8到9的距离为：', distance)

# 用邻接表表示带权图
n = 5 # 节点数
a,b,c,d,e= range(n) # 节点名称,对应0，2，3，8，9
graph = [
  {b:8, c:14, d:14, e:16},
  {a:8, c:16, d:8, e:13},
  {a:14, b:16, d:22, e:16},
  {a:14, b:8, c:22, e:10,},
  {a:16, b:13, c:16, d:10}
]
x = [0]*(n+1) # 一个解（n+1元数组，长度固定）
X = []     # 一组解
best_x = [0]*(n+1) # 已找到的最佳解（路径）
min_cost = 0    # 最小旅费
# 冲突检测
def conflict(k):
  global n,graph,x,best_x,min_cost
  # 第k个节点，是否前面已经走过
  if k < n and x[k] in x[:k]:
    return True
  # 回到出发节点
  if k == n and x[k] != x[0]:
    return True
  # 前面部分解的旅费之和超出已经找到的最小总旅费
  cost = sum([graph[node1][node2] for node1,node2 in zip(x[:k], x[1:k+1])])
  if 0 < min_cost < cost:
    return True
  return False # 无冲突
# 旅行商问题（TSP）
def tsp(k): # 到达（解x的）第k个节点
  global n,a,b,c,d,e,graph,x,X,min_cost,best_x
  if k > n: # 解的长度超出，已走遍n+1个节点 （若不回到出发节点，则 k==n）
    cost = sum([graph[node1][node2] for node1,node2 in zip(x[:-1], x[1:])]) # 计算总旅费
    if min_cost == 0 or cost < min_cost:
      best_x = x[:]
      min_cost = cost
      #print(x)
  else:
    for node in graph[x[k-1]]: # 遍历节点x[k-1]的邻接节点（状态空间）
      x[k] = node
      if not conflict(k): # 剪枝
        tsp(k+1)
# 测试
x[0] = b # 出发节点：路径x的第一个节点（随便哪个）
tsp(1)  # 开始处理解x中的第2个节点
print(best_x)
print(min_cost)