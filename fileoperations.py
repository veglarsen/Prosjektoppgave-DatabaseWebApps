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