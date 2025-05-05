from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._fermate = DAO.getAllFermate()
        self._grafo = nx.DiGraph()
        self._idMapFermate = {}
        for f in self._fermate:
            self._idMapFermate[f.id_fermata] = f

    def getBFSNodesFromTree(self, source):
        tree = nx.bfs_tree(self._grafo, source)
        archi = list(tree.edges())
        nodi = list(tree.nodes())
        return nodi[1:]


    def getDFSNodesFromTree(self, source):
        tree = nx.dfs_tree(self._grafo, source)
        nodi = list(tree.nodes())
        return nodi[1:]

    def getBFSNodesFromEdges(self, source):
        archi = nx.bfs_edges(self._grafo, source)
        res = []
        for u,v in archi:
            res.append(v)

        return res

    def getDFSNodesFromEdges(self, source):
        archi = nx.dfs_edges(self._grafo, source)
        res = []
        for u, v in archi:
            res.append(v)

        return res


    def buildGraph(self):
        # aggiungiamo in nodi --> li prendiamo in "fermate"
        self._grafo.add_nodes_from(self._fermate)
        self.addEdges3()

    def addEdges1(self):
        '''
        Aggiungo gli archi ciclando con doppio ciclo sui nodi e testando se per ogni coppia
        eiste una connessione
        '''
        for u in self._fermate:
            for v in self._fermate:
                if DAO.hasConnessione(u,v):
                    self._grafo.add_edge(u, v)
                    print(f"Aggiungo arco tra {u} e {v}")

    def addEdges2(self):
        '''
        Ciclo solo una volta, e faccio una query per trovare tutti i vicini
        '''
        for u in self._fermate:
            for con in DAO.getVicini(u):
                v = self._idMapFermate[con.id_stazA]
                self._grafo.add_edge(u, v)

    def addEdges3(self):
        '''
        faccio una query unica che prende tutti gli archi e poi ciclo qui.
        '''
        allEdges = DAO.getAllEdges()
        for edge in allEdges:
            u = self._idMapFermate[edge.id_stazP]
            v = self._idMapFermate[edge.id_stazA]
            self._grafo.add_edge(u, v)

    def addEdgesPesati(self):
        self._grafo.clear_edges()
        allEdges = DAO.getAllEdges()
        for edge in allEdges:
            u = self._idMapFermate[edge.id_stazP]
            v = self._idMapFermate[edge.id_stazA]

            if self._grafo.has_edge(u, v):
                self._grafo[u][v]["weight"] += 1
            else:
                self._grafo.add_edge(u, v, weight=1)

    def getArchiPesoMaggiore(self):
        edges = self._grafo.edges(data=True)
        res = []
        for e in edges:
            if self._grafo.get_edge_data(e[0], e[1])["weight"] > 1:
                res.append(e)
        return (res)

    def getNumNodi(self):
        return len(self._grafo.nodes)

    def getNumArchi(self):
        return len(self._grafo.edges)

    @property
    def fermate(self):
        return self._fermate

