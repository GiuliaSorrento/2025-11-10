import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph=nx.DiGraph()
        self._orders=[]
        self._idMapO={}
        self._optPath = None
        self._optScore = None

    #percorso di peso massimo
    #peso degli archi nel percorso strettamente decrescente
    #un vertice puo entrare una sola volta nel percorso
    #vertice partenza calcolato nel punto precedente
    def getSolOttima(self,sourceStr):
        self._optPath = []
        self._optScore = -1
        source = self._idMapO[int(sourceStr)]
        parziale = [source]
        self._ricorsione(parziale, None) #passiamo anche il peso dell'ultimo arco preso che inizalmente è un numero molto negativo visto che non abbiamo ancora arco
        return self._optPath, self._optScore

    def _ricorsione(self,parziale, peso_precedente):
        #condizione di terminazione --> secondo me non esiste perche stiamo cercando il peso massimo, non abbiamo una fine sicura
        if self._score(parziale) > self._optScore:
            self._optPath = copy.deepcopy(parziale)
            self._optScore = self._score(parziale)

        nodo_corrente = parziale[-1]  # E PIU UTILE RICAVARSI IL NODO CORRENTE PIUTTOSTO CHE USARE UN INDICE

        for vicino in self._graph.successors(nodo_corrente):
            # Vincolo 1: Cammino SEMPLICE (il nodo non deve essere già stato visitato)
            if vicino not in parziale:
                # Vincolo 2: peso strettamente decrescente

                pesoSuccessivo = self._graph[nodo_corrente][vicino]["weight"]
                if peso_precedente is None or peso_precedente > pesoSuccessivo:
                    # Svolta (Backtracking)
                    parziale.append(vicino)

                    # Ricorsione: non serve l'indice 'i', andiamo avanti finché troviamo vicini validi
                    self._ricorsione(parziale, pesoSuccessivo)

                    # Contro-svolta
                    parziale.pop()
    def _score(self, parziale):
        if len(parziale)  < 2:
            return 0
        peso = 0
        #DEVI PER FORZA SCORRERE COSI PERCHE SENNO NON RISPETTI ORDINE DEI NODI IN PARZIALE
        for i in range(len(parziale)-1):
            u= parziale[i]
            v=parziale[i+1]
            peso += self._graph[u][v]["weight"]
        return peso



    def getStores(self):
        return DAO.getAllStores()

    def getAllNodes(self):
        return self._graph.nodes()

    def buildGraph(self, store_name, k):
        self._graph.clear()
        self._orders.clear()
        self._orders = DAO.getAllNodes(store_name)
        self._graph.add_nodes_from(self._orders)
        for order in self._orders:
            self._idMapO[order.order_id]=order

        myedges = DAO.getAllEdgePesati(store_name,k, self._idMapO)
        for edge in myedges:
            self._graph.add_edge(edge.ordine1,edge.ordine2,weight=edge.peso)

    def getGraphDetails(self):
        return len(self._graph.nodes()), len(self._graph.edges())

    def getTop5Archi(self):
        edges = sorted(self._graph.edges(data=True), key=lambda x: x[2]["weight"], reverse=True)
        return edges[:5]

    def getCammino(self, sourceStr):
        #VISUALIZZARE IL CAMMINO PIU LUNGO PARTENDO DA UN NODO
        #SCEGLERE ALG MIGLIORE TRA DFS E BFS

        source = self._idMapO[int(sourceStr)]  #recupera nodo a partire dalla stringa id selezionata dall'utente
        lp = [] #lista che conterra il cammino

        #CAMMINO PIU LUNGO ---> DFS
        tree = nx.dfs_tree(self._graph, source) #ALBERO CHE CONTIENE TUTTI I NODI RAGGIUNGIBILI DA SOURCE
        nodi = list(tree.nodes())

        for node in nodi:
            tmp = [node] #lista temporanea che all'inizio contiene solo il nodo finale

            while tmp[0] != source: #finche non arrivo al nodo di origine
                pred = nx.predecessor(tree, source, tmp[0])  #recupero il padre del nodo che ho ora
                tmp.insert(0, pred[0])

            if len(tmp) > len(lp):
                lp = copy.deepcopy(tmp)

        return lp