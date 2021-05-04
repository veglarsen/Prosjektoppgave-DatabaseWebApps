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
        # sjekk om prepared og buffered kan leve sammen
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

    def currentBlogg(self):
        try:
            self.cursor.execute("""SELECT eier FROM blogg""")
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(err)
        return result

    def selectAlleInnlegg(self, id):
        try:
            self.cursor.execute("""SELECT blogg_navn, innlegg_id, innlegg.blogg_ID, innlegg, dato, tag, treff, ingress,
                                tittel, eier FROM innlegg inner join blogg 
                                on innlegg.blogg_ID = blogg.blogg_ID where blogg.blogg_ID = (%s)""", (id,))
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(err)
        return result

    def selectEtInnlegg(self, id):
        try:
            self.cursor.execute("""SELECT blogg_navn, innlegg_id, innlegg.blogg_ID, innlegg, dato, tag, treff, ingress, 
                                tittel, eier FROM innlegg inner join blogg 
                                on innlegg.blogg_ID = blogg.blogg_ID where innlegg.innlegg_id = (%s)""", (id,))
            result = self.cursor.fetchone()
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
        except mysql.connector.Error as err:
            print(err)

    def kommentarer(self, id):
        try:
            self.cursor.execute("SELECT * FROM kommentar where innlegg_ID = (%s)", (id,))
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(err)
        return result

    def selectBruker(self, bruker_navn):
        try:
            self.cursor.execute("SELECT * FROM bruker where bruker = (%s)", (bruker_navn,))
            result = self.cursor.fetchone()
        except mysql.connector.Error as err:
                print(err)
        return result

    def addBruker(self, bruker):
        # try:
        #     self.cursor.execute("""INSERT INTO bruker('bruker', 'etternavn', 'fornavn', 'passord', 'eMail')
        #                         VALUES (NULL, (%s), (%s), (%s), (%s), (%s));""", (brukernavn, etternavn, fornavn, passord, eMail ))
        #     result = self.cursor.fetchall()
        # except mysql.connector.Error as err:
        #         print(err)
        # return result
        try:
            sql = '''INSERT INTO 
            bruker
            (id, bruker, etternavn, fornavn, passord, eMail)
            VALUES 
            (NULL, %s, %s, %s, %s, %s)'''
            self.cursor.execute(sql, bruker)
        except mysql.connector.Error as err:
            print(err)




    def brukerEndre(self, bruker):  # kanskje tillate å endre brukernavn
        try:
            sql1 = '''UPDATE 
                bruker 
            SET 
                fornavn = %s, etternavn = %s, eMail = %s, passord = %s
            WHERE
                bruker = %s'''
            self.cursor.execute(sql1, bruker)
        except mysql.connector.Error as err:
            print(err)

    def selectAllVedlegg(self):
        try:
            self.cursor.execute('''SELECT * from vedlegg where innlegg_ID=1''')
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(err)
        return result

    def addVedlegg(self, attachment):
        try:
            sql = '''INSERT
            INTO
                vedlegg(vedlegg_ID, fil_navn, fil_type, fil_data, size, innlegg_ID)
            VALUES
                (NULL, %s, %s, %s, %s, %s)'''
            self.cursor.execute(sql, attachment)

        except mysql.connector.Error as err:
            print(err)

    def getVedlegg(self, id):
        try:
           self.cursor.execute("SELECT * FROM vedlegg WHERE vedlegg_ID=(%s)", (id,))
           result = self.cursor.fetchone()
        except mysql.connector.Error as err:
            print(err)
        return result
    def redigerInnlegg(self, redigerInnlegg):
        try:
           sql1 = ('''UPDATE innlegg
                                    SET innlegg = (%s), innlegg.tittel = (%s), innlegg.ingress = (%s)
                                WHERE innlegg.innlegg_ID = (%s)''')
           result = self.cursor.execute(sql1, redigerInnlegg)
        except mysql.connector.Error as err:
            print(err)
        return result
