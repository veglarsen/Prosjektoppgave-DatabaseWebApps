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
            self.cursor.execute("""SELECT blogg_navn as tittel FROM stud_v21_larsen.blogg""")
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
                print(err)
        return result