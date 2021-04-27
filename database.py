import mysql.connector

class myDB:

    def __init__(self) -> None:
        dbconfig = {'host': 'kark.uit.no',
                    'user': 'stud_v21_larsen',
                    'password': 'Hvorer1Arild',
                    'database': 'stud_v21_larsen', }
        self.configuration = dbconfig

    def __enter__(self) -> 'cursor':
        self.conn = mysql.connector.connect(**self.configuration)
        self.cursor = self.conn.cursor(prepared=True)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.conn.commit()
        self.cursor.close()
        self.conn.close

    def selectBlogg(self):
        try:
            self.cursor.execute("""SELECT blogg_navn, blogg_ID as tittel FROM blogg""")
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
                print(err)
        return result

    def selectAlleInnlegg(self, id):
        try:
            self.cursor.execute("""SELECT blogg_navn, innlegg_id, innlegg.blogg_ID, innlegg, dato, tag, treff 
                                FROM innlegg inner join blogg 
                                on innlegg.blogg_ID = blogg.blogg_ID where blogg.blogg_ID = (%s)""", (id,))
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
                print(err)
        return result

    def selectEtInnlegg(self, id):
        try:
            self.cursor.execute("""SELECT blogg_navn, innlegg_id, innlegg.blogg_ID, innlegg, dato, tag, treff 
                                FROM innlegg inner join blogg 
                                on innlegg.blogg_ID = blogg.blogg_ID where innlegg.innlegg_id = (%s)""" , (id,))
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
                print(err)
        return result

    def newBlogg(self, bruker_navn, blogg_navn):
        try:
            self.cursor.execute("""INSERT INTO blogg (blogg_ID, eier, blogg_navn) VALUES (NULL, %s, %s);""")
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(err)
        return result

    def incrementTreff(self, id):
        try:
            self.cursor.execute('UPDATE innlegg SET treff = (SELECT treff FROM innlegg where innlegg_ID=(%s)) + 1 WHERE innlegg_ID = (%s)', (id, id))
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(err)
        return result
