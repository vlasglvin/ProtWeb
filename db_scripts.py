import sqlite3


class PlanesDB:
    def __init__(self, dbname):
        self.name = dbname
        self.conn = None
        self.cursor = None

    def open(self):
        self.conn = sqlite3.connect(self.name)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def get_all_planes(self):
        self.open()
        self.cursor.execute('''SELECT * FROM planes ''')
        data = self.cursor.fetchall()
        self.close()
        data = [dict(row) for row in data]
        return data
    
    def get_plane(self, name):
        self.open()
        self.cursor.execute('''SELECT * FROM planes WHERE name=? ''', [name])
        data = self.cursor.fetchall()
        self.close()
        data = [dict(row) for row in data]
        
        return data[0]
    
    def get_all_categories(self):
        self.open()
        self.cursor.execute('''SELECT * FROM categories ''')
        data = self.cursor.fetchall()
        self.close()
        data = [dict(row) for row in data]
        return data
    
    def get_planes_by_category(self, category_id):
        self.open()
        self.cursor.execute('''SELECT * FROM planes WHERE category_id=?''', [category_id])
        data = self.cursor.fetchall()
        self.close()
        data = [dict(row) for row in data]
        return data
    
    def get_category(self, category_id):
        self.open()
        self.cursor.execute('''SELECT * FROM categories WHERE id=? ''', [category_id])
        data = self.cursor.fetchall()
        self.close()
        data = [dict(row) for row in data]

        return data[0]['title']
    
    # def get_all_planes_by_categories(self):
    #     self.open()
    #     self.cursor.execute('''SELECT * 
    #     FROM categories JOIN planes ON categories.id = planes.category_id ORDER BY category_name''')
    #     data = self.cursor.fetchall()
    #     self.close()
    #     data = [dict(row) for row in data]
    #     return data
    