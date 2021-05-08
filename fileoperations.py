import mysql.connector

class fileDB:

    def __init__(self) -> None:
        dbconfig = {'host': 'kark.uit.no',
                    'user': 'stud_v21_larsen',
                    'password': 'Hvorer1Arild',
                    'database': 'stud_v21_larsen', }
        self.configuration = dbconfig

    def __enter__(self) -> 'cursor':
        self.conn = mysql.connector.connect(**self.configuration)
        self.cursor = self.conn.cursor(buffered=True)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.conn.commit()
        self.cursor.close()
        self.conn.close

    def selectAllVedlegg(self, id):
        try:
            # sql = '''SELECT * from vedlegg where innlegg_ID= (%s)'''
            self.cursor.execute("SELECT * from vedlegg where innlegg_ID=(%s)", (id,))
            # self.cursor.execute(sql)
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

    def slettAlleVedlegg(self, id):
        try:
            self.cursor.execute("SELECT vedlegg_ID FROM vedlegg WHERE innlegg_ID = (%s)", (id,))
            allVedlegg = self.cursor.fetchall()
            for vedlegg in allVedlegg:
                vedleggID = vedlegg[0]
                self.cursor.execute("DELETE FROM vedlegg WHERE innlegg_ID = (%s) AND vedlegg_ID = (%s)",
                                    (id, vedleggID))
        except mysql.connector.Error as err:
            print(err)

    def slettVedlegg(self, id, vedleggID):
        try:
            self.cursor.execute("DELETE FROM vedlegg WHERE innlegg_ID = (%s) and vedlegg_ID = (%s)",
                                (id, vedleggID))
        except mysql.connector.Error as err:
            print(err)

    def slettTags(self, id):
        try:
            self.cursor.execute("SELECT innlegg_blogg_ID from tag_innlegg WHERE innlegg_innlegg_ID = (%s)", (id,))
            innleggBloggID = self.cursor.fetchone()
            self.cursor.execute("SELECT tag_tag_ID from tag_innlegg WHERE innlegg_innlegg_ID = (%s)", (id,))
            allTags = self.cursor.fetchall()
            for tag in allTags:
                tagID = tag[0]
                self.cursor.execute(
                    "DELETE FROM tag_innlegg WHERE tag_tag_ID = (%s) and innlegg_innlegg_ID = (%s) and innlegg_blogg_ID = (%s)",
                    (tagID, id, innleggBloggID[0]))
        except mysql.connector.Error as err:
            print(err)

    def slettKommentarer(self, id):
        try:
            self.cursor.execute("SELECT kommentar_ID from kommentar WHERE innlegg_ID = (%s)", (id,))
            allKommentarID = self.cursor.fetchall()
            for kommentar in allKommentarID:
                kommentarID = kommentar[0]
                self.cursor.execute("DELETE FROM kommentar where kommentar_ID = (%s)", (kommentarID,))
        except mysql.connector.Error as err:
            print(err)

    def slettInnlegg(self, id):
        try:
            self.slettAlleVedlegg(id)
            self.slettTags(id)
            self.slettKommentarer(id)
            self.cursor.execute("DELETE FROM innlegg WHERE innlegg_ID = (%s)", (id,))
        except mysql.connector.Error as err:
            print(err)