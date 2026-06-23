import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def handleCreaGrafo(self, e):
        store = self._view._ddStore.value #mi da il name
        k = self._view._txtIntK.value #mi da il numero in stringa

        #controlli
        if store is None or k is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("attenzione, per procedere devi selezionare uno store e scrivere un valore numerico nel campo di testo"))
            self._view.update_page()
            return
        try:
            kInt = int(k)
        except:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, nel campo di testo puoi inserire solo un valore numerico intero"))
            self._view.update_page()
            return

        #creo grafo
        self._model.buildGraph(store, kInt)
        self.fillDDNodes()
        self._view._ddNode.disabled = False
        self._view._btnCerca.disabled = False
        self._view._btnRicorsione.disabled = False
        n,a = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Grafo correttamente creato con {n} nodi e {a} archi"))

        top5 = self._model.getTop5Archi()
        self._view.txt_result.controls.append(
            ft.Text(f"ecco i 5 archi con peso maggiore"))

        for t in top5:
            self._view.txt_result.controls.append(
                ft.Text(f"{t[0].order_id}-->{t[1].order_id} - peso {t[2]["weight"]}"))
        self._view.update_page()


    def handleCerca(self, e):
        scelta = self._view._ddNode.value
        cammino = self._model.getCammino(scelta)


        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Percorso massimo a partire dal nodo {scelta}"))
        for a in cammino:
            self._view.txt_result.controls.append(
                ft.Text(a))


        self._view.update_page()



    def handleRicorsione(self, e):
        bestPath, bestScore = self._model.getSolOttima(self._view._ddNode.value)
        #ci sarebbe da fare il controllo
        self._view.txt_result.controls.append(ft.Text(f"percorso di peso massimo pari a {bestScore}"))
        for a in bestPath:
            self._view.txt_result.controls.append(ft.Text(a.order_id))
        self._view.update_page()

    def fillDDStores(self):
        stores = self._model.getStores()
        for s in stores:
            self._view._ddStore.options.append(ft.dropdown.Option(text=s.store_name, data = s))
        self._view.update_page()

    def fillDDNodes(self):

        store = self._view._ddStore.value  # mi da il name
        if store is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("attenzione, per procedere devi selezionare uno store"))
            self._view.update_page()
            return
        nodi = self._model.getAllNodes()
        for n in nodi:
            self._view._ddNode.options.append(ft.dropdown.Option(text=n.order_id, data = n))
        self._view.update_page()

