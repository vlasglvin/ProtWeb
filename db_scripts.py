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

    def get_plane_by_id(self, plane_id):
        self.open()
        self.cursor.execute('''SELECT * FROM planes WHERE id=? ''', [plane_id])
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
    
    def get_all_planes_by_categories(self):
        planes = {}
        categories = self.get_all_categories()
        for category in categories:
            category_planes = self.get_planes_by_category(category['id'])
            planes[category['title']] = category_planes

        return planes
    
    def search_planes(self, query):
        self.open()
        query = query + '%'
        self.cursor.execute('''SELECT * FROM planes WHERE (name LIKE ? OR country LIKE ? OR wing_shape LIKE ? OR producedstart LIKE ? OR description LIKE ?)''', 
                            [query , query, query, query, query])
        data = self.cursor.fetchall()
        self.close()
        data = [dict(row) for row in data]
        return data
    
    def get_all_articles(self):
        self.open()
        self.cursor.execute('''SELECT * FROM articles ''')
        data = self.cursor.fetchall()
        self.close()
        data = [dict(row) for row in data]
        return data
    
    def check_login_data(self, username):
        self.open()
        self.cursor.execute('''SELECT * FROM users WHERE username=?''',
                            [username])
        data = self.cursor.fetchall()
        if data:
            data = [dict(row) for row in data]
            return data[0]
        else:
            return None
        
    def get_user(self, user_id):
        self.open()
        self.cursor.execute('''SELECT * FROM users WHERE id=?''',
                            [user_id])
        data = self.cursor.fetchall()
        if data:
            data = [dict(row) for row in data]
            return data[0]
        else:
            return None
        
    def is_username_exist(self, username):
        self.open()
        self.cursor.execute('''SELECT * FROM users WHERE username=?''',
                            [username])
        data = self.cursor.fetchone()
        self.close()
        return data
    
    def is_email_exist(self, email):
        self.open()
        self.cursor.execute('''SELECT * FROM users WHERE email=?''',
                            [email])
        data = self.cursor.fetchone()
        self.close()
        return data

    def create_user(self, name, username, email, password):
        self.open()
        self.cursor.execute('''
            INSERT INTO users (name, username, email, password)
            VALUES (?,?,?,?)''',
             [ name, username, email, password] )
        self.conn.commit()
        self.close()

    def create_plane(self, name, category_id, image, country,
                      quantity, produsedstart, produsedend, cost, 
                      wingshape, specifications, description, history):
        self.open()
        self.cursor.execute('''
            INSERT INTO planes (name, category_id, image, country,
                      quantity, producedstart, producedend, cost, 
                      wing_shape, specifications, description, history)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''',
             [name, category_id, image, country,
                      quantity, produsedstart, produsedend, cost, 
                      wingshape, specifications, description, history] )
        self.conn.commit()
        self.close()

    def delete_plane(self, plane_id):
        self.open()
        self.cursor.execute(''' DELETE FROM planes WHERE id=?''', [plane_id])
        self.conn.commit()
        self.close()

        