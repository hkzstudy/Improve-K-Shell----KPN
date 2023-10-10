import networkx as nx

class KPN:
    '''
    熊才权, 古小惠, 吴歆韵. 基于K-shell位置和两阶邻居的复杂网络节点重要性评估方法[J]. 计算机应用研究, 2023, 40(3): 738-742.
    '''
    
    def __init__(self, G):

        self.G = G.copy()
        self.nodes = list(self.G.nodes())
        self.degs  = dict(nx.degree(self.G))
        self.edges = list(self.G.edges())
        self.nbrs  = {}

        for node in self.nodes:
            nbrs = nx.neighbors(self.G, node)
            self.nbrs[node] = nbrs

        self.ks = {} # 存放 k-shell 的值
        self.kp = {}
        self.nodes_kpn = {}
    
    def kpn(self):
        '''
        核心步骤
        '''

        self.graph = self.G.copy()

        importance_dict = {}
        ks = 1
        while self.graph.nodes():

            temp = []
  
            de = dict(self.graph.degree)

            kks = min(de.values())
            ri = {}
            count = 1
            while True:
                for k, v in de.items():
                    if v == kks:
                        temp.append(k)
                        self.graph.remove_node(k)
                        ri[k] = count
                        
                de = dict(self.graph.degree)

                count += 1
                
                        
                if kks not in de.values():
                    break
            importance_dict[ks] = temp

            for node in temp:
                self.kp[node] = ks + (ri[node] / (max(list(ri.values())) +1) )

            ks += 1

        for k,v in importance_dict.items():
            for j in v:
                self.ks[j] = k
        

        alpa = 0.7
        beta = 1 - alpa

        for node in self.nodes:
            self.nodes_kpn[node] = self.kp[node]
            nbrs1 = self.nbrs[node]
            for nbr in nbrs1:
                self.nodes_kpn[node] += alpa * self.kp[nbr]

                nbrs2 = self.nbrs[nbr]
                for nbr2 in nbrs2:
                    self.nodes_kpn[node] += beta * self.kp[nbr2]

    def main(self):

        self.kpn()

        return self.nodes_kpn
