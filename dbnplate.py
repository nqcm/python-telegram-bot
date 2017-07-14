import sqlite3

class DBHelper:
    def __init__(self, dbname="nplate.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    # def setup(self):
    #     stmt = "CREATE TABLE IF NOT EXISTS items (num text)"
    #     self.conn.execute(stmt)
    #     self.conn.commit()

    def add_item(self, item_text):
        stmt = "INSERT INTO items (num) VALUES (?)"
        args = (item_text, )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_item(self, item_text):
        stmt = "DELETE FROM items WHERE num = (?)"
        args =(item_text, )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_items(self):
        stmt = "SELECT num FROM items"
        return [x[0] for x in self.conn.execute(stmt)]
