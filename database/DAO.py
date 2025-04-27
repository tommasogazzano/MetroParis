from database.DB_connect import DBConnect
from model.fermata import Fermata


class DAO():

    @staticmethod
    def getAllFermate():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM fermata"
        cursor.execute(query)

        for row in cursor:
            result.append(Fermata(row["id_fermata"], row["nome"], row["coordX"], row["coordY"]))
        cursor.close()
        conn.close()
        return result

