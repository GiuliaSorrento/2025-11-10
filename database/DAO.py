from database.DB_connect import DBConnect
from model.arco import Arco
from model.order import Order

from model.store import Store


class DAO():
    @staticmethod
    def getAllStores():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * from stores"

        cursor.execute(query)

        for row in cursor:
            results.append(Store(**row))

        cursor.close()
        conn.close()
        return results



    @staticmethod
    def getAllNodes(store_name):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select o.*
                from orders o, stores s
                where o.store_id = s.store_id 
                and s.store_name = %s"""

        cursor.execute(query,(store_name,))

        for row in cursor:
            results.append(Order(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdgePesati(store_name, k, idMapO):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        #nb. QUANDO ORDINI UN PRODOTTO POSSONO ESSERCI PIU QUANTITA DI QUEL PRODOTTO, DEVI FARE SUM DI QUANTITY NON COUNT DELL'ID PRODOTTO
        #COALESCE+NULLIF: Prova a dividere la somma degli oggetti per i giorni di differenza.
        # Se i giorni sono 0 (che farebbe crashare il sistema), fai finta che non sia successo nulla e prendi semplicemente la somma totale
        # degli oggetti come peso dell'arco.

        #NB.IL NUMERO DI OGGETTI è DATO DAL PRODOTTO DEL NUMERO DI OGGETTI PER LA LORO QUANTITA
        query = """SELECT o1.order_id as ordine1, o2.order_id as ordine2, 
                   CAST((o1.sumQ * o2.countR) + (o2.sumQ * o1.countR) AS DOUBLE) / DATEDIFF(o2.data, o1.data) as peso
            FROM
                (SELECT o.order_id as order_id, o.order_date as data, 
                        SUM(oi.quantity) as sumQ, COUNT(oi.item_id) as countR
                 FROM orders o, order_items oi, stores s
                 WHERE o.order_id = oi.order_id AND o.store_id = s.store_id 
                 AND s.store_name = %s
                 GROUP BY o.order_id, o.order_date) o1,
                (SELECT o.order_id as order_id, o.order_date as data, 
                        SUM(oi.quantity) as sumQ, COUNT(oi.item_id) as countR
                 FROM orders o, order_items oi, stores s
                 WHERE o.order_id = oi.order_id AND o.store_id = s.store_id 
                 AND s.store_name = %s
                 GROUP BY o.order_id, o.order_date) o2
            WHERE o1.order_id <> o2.order_id 
              AND o1.data < o2.data
              AND DATEDIFF(o2.data, o1.data) <= %s
              AND DATEDIFF(o2.data, o1.data) > 0"""

        cursor.execute(query, (store_name, store_name, k))

        for row in cursor:
            results.append(Arco(idMapO[row["ordine1"]], idMapO[row["ordine2"]], row["peso"]))

        cursor.close()
        conn.close()
        return results



