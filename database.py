import mysql.connector
from wtforms import ValidationError


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
            self.cursor.execute("""SELECT blogg_navn, blogg_ID as tittel, eier FROM blogg""")
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(err)
        return result

    def selectEnBlogg(self, id):
        try:
            self.cursor.execute("""SELECT blogg_navn, blogg_ID, eier FROM blogg where blogg_ID = %s""", (id, ))
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
            self.cursor.execute("""SELECT blogg_navn, innlegg_id, innlegg.blogg_ID, innlegg, dato, treff, ingress,
                                tittel, eier FROM innlegg inner join blogg 
                                on innlegg.blogg_ID = blogg.blogg_ID where blogg.blogg_ID = (%s)""", (id,))
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(err)
        return result

    def selectAlleInnleggTag(self, tag):
        try:
            self.cursor.execute("""SELECT blogg_navn, innlegg_id, innlegg.blogg_ID, innlegg, dato, treff, ingress, 
            tittel, eier, tag_navn FROM innlegg 
                                   inner join blogg on innlegg.blogg_ID = blogg.blogg_ID
                                   inner join tag_innlegg on innlegg.innlegg_id = tag_innlegg.innlegg_innlegg_ID 
                                   JOIN tag ON tag_innlegg.tag_tag_ID = tag.tag_ID where tag_tag_ID = (%s)""", (tag,))
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(err)
        return result


    def selectEtInnlegg(self, id):
        try:
            self.cursor.execute("""SELECT blogg_navn, innlegg_id, innlegg.blogg_ID, innlegg, dato, treff, ingress, 
                                tittel, eier FROM innlegg inner join blogg 
                                on innlegg.blogg_ID = blogg.blogg_ID where innlegg.innlegg_id = (%s)""", (id, ))
            result = self.cursor.fetchone()
        except mysql.connector.Error as err:
            print(err)
        return result
    def selectTags(self, innlegg_ID):
        try:
            self.cursor.execute("""SELECT tag_ID, tag_navn FROM tag_innlegg inner join tag on tag_tag_ID = tag.tag_ID 
                                where innlegg_innlegg_ID = (%s)""", (innlegg_ID,))
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(err)
        return result

    def selectEnKommentar(self, id):
        try:
            self.cursor.execute("""SELECT kommentar_id, innlegg_id, blogg_id, bruker, kommentar, dato FROM kommentar where kommentar_id = (%s)""", (id,))
            result = self.cursor.fetchone()
        except mysql.connector.Error as err:
            print(err)
        return result

    def validate_tag_navn(self, tag_navn):
        with myDB() as db:
            listTag = db.selectTag()
            print(listTag)
            if tag_navn in str(listTag):
                print(f'Brukernavet {tag_navn} er allerede i bruk')
                raise ValidationError(message="Brukernavn er allerede i bruk")


    def nyttInnlegg(self, nyttInnlegg, tag, newTag):
        try:
            sql1 = '''INSERT INTO innlegg (innlegg_ID, blogg_ID, tittel, ingress, innlegg, treff)
                      VALUES (NULL, %s, %s , %s , %s, 0);'''
            self.cursor.execute(sql1, nyttInnlegg)
            innlegg_ID = self.cursor.lastrowid
            with myDB() as db:
                listTag = db.selectTag()
                print(listTag)
                if newTag in str(listTag):
                    sjekk = True
                else:
                    sjekk = False

            if len(tag) != 0:
                for x in tag:
                    tag_ID = x;
                    sql1 = '''INSERT INTO tag_innlegg (tag_tag_ID, innlegg_innlegg_ID, innlegg_blogg_ID)
                                        VALUES ((%s), (%s), (SELECT blogg_ID from innlegg where innlegg_ID = (%s)))'''
                    data = (tag_ID, innlegg_ID, innlegg_ID)
                    self.cursor.execute(sql1, data)

            elif newTag != " " and sjekk == False:
                sql1 = '''INSERT INTO tag (tag_navn) VALUES (%s)'''
                self.cursor.execute(sql1, newTag)

                tag_ID = self.cursor.lastrowid
                sql1 = '''INSERT INTO tag_innlegg (tag_tag_ID, innlegg_innlegg_ID, innlegg_blogg_ID)
                          VALUES ((%s), (%s), (SELECT blogg_ID from innlegg where innlegg_ID = (%s)))'''
                data = (tag_ID, innlegg_ID, innlegg_ID)
                self.cursor.execute(sql1, data)
            else:
                sql1 = '''INSERT INTO tag_innlegg (tag_tag_ID, innlegg_innlegg_ID, innlegg_blogg_ID)
                                        VALUES ((%s), (%s), (SELECT blogg_ID from innlegg where innlegg_ID = (%s)))'''
                data = (1, innlegg_ID, innlegg_ID)
                self.cursor.execute(sql1, data)

        except mysql.connector.Error as err:
            print(err)
        return innlegg_ID

    def newBlogg(self, blogg_navn, eier):
        try:
            self.cursor.execute("""INSERT INTO blogg(eier, blogg_navn) VALUES (%s, %s)""", (eier, blogg_navn, ))
            # sql1 = ("""INSERT INTO blogg(eier, blogg_navn) VALUES (%s, %s)""")
            # self.cursor.execute(sql1, blogg, )
        except mysql.connector.Error as err:
            print(err)

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

    def nyKommentar(self, kommentar):
        try:
            sql1 = '''INSERT INTO
            `kommentar`
            (`innlegg_ID`, `blogg_ID`, `bruker`, `kommentar`) 
            VALUES 
            ((%s), (SELECT innlegg.blogg_ID FROM innlegg WHERE innlegg.innlegg_ID = (%s)
            ), (%s), (%s));
            '''
            self.cursor.execute(sql1, kommentar)
        except mysql.connector.Error as err:
            print(err)

    def redigerKommentar(self, kommentar): # fiks at dato oppdateres
        try:
            sql1 = '''UPDATE
                kommentar
            SET
                kommentar = (%s)
            WHERE
                kommentar_ID = (%s)'''
            self.cursor.execute(sql1, kommentar)
        except mysql.connector.Error as err:
            print(err)

    def selectBruker(self, bruker_navn):
        try:
            self.cursor.execute("SELECT * FROM bruker where bruker = (%s)", (bruker_navn,))
            result = self.cursor.fetchone()
        except mysql.connector.Error as err:
                print(err)
        return result

    def selectAllBrukernavn(self):
        try:
            self.cursor.execute("SELECT bruker from bruker")
            result = self.cursor.fetchall()
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

    def selectTag(self):
        try:
            self.cursor.execute('''SELECT CAST(tag_ID as char) as tag_ID, tag_navn from tag;''')
            result = self.cursor.fetchall()
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

    def getLastAddedInnleggID(self):
        try:
            result = self.cursor.lastrowid
        except mysql.connector.Error as err:
            print(err)
        return result
    def searchAndTag(self, search, tag_ID):
        try:
            self.cursor.execute('''SELECT blogg_navn, innlegg_id, innlegg.blogg_ID, innlegg, dato, treff, ingress, tittel, eier FROM innlegg 
                                   join blogg on innlegg.blogg_ID = blogg.blogg_ID
                                   join tag_innlegg on innlegg.innlegg_ID = tag_innlegg.innlegg_innlegg_ID
                                   WHERE (tittel LIKE %s OR innlegg LIKE %s OR ingress LIKE %s) 
                                   and tag_tag_ID = %s''',("%" + search + "%", "%" + search + "%", "%" + search + "%", tag_ID, ))
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(err)
        return result

    def search(self, search):
        try:
            self.cursor.execute('''SELECT blogg_navn, innlegg_id, innlegg.blogg_ID, innlegg, dato, treff, ingress, tittel, eier FROM 
                                innlegg join blogg on innlegg.blogg_ID = blogg.blogg_ID WHERE tittel LIKE %s OR innlegg LIKE %s OR ingress LIKE %s''',
                                ("%" + search + "%", "%" + search + "%", "%" + search + "%",))
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(err)
        return result

