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
        self.cursor.execute('''SELECT * FROM planes WHERE visibility="visible"''')
        data = self.cursor.fetchall()
        self.close()
        data = [dict(row) for row in data]
        return data
    
    def get_suggested_planes(self):
        self.open()
        self.cursor.execute('''SELECT * FROM planes WHERE visibility="hidden"''')
        data = self.cursor.fetchall()
        self.close()
        if data and len(data) > 0:
            data = [dict(row) for row in data]
            return data
        else:
            return None
    
    def get_plane(self, name):
        self.open()
        self.cursor.execute('''SELECT * FROM planes WHERE name=? AND visibility="visible" ''', [name])
        data = self.cursor.fetchone()
        self.close()
        if data is not None:
            data = dict(data)
            print(data)
            return data
        else:
            return None
        

    def get_plane_by_id(self, plane_id):
        self.open()
        self.cursor.execute('''SELECT * FROM planes WHERE id=? ''', [plane_id])
        data = self.cursor.fetchall()
        self.close()
        if data:
            data = [dict(row) for row in data]
            return data[0]
        else:
            return None

    def get_all_categories(self):
        self.open()
        self.cursor.execute('''SELECT * FROM categories ''')
        data = self.cursor.fetchall()
        self.close()
        data = [dict(row) for row in data]
        return data
    
    def get_planes_by_category(self, category_id):
        self.open()
        self.cursor.execute('''SELECT * FROM planes WHERE category_id=? AND visibility="visible"''', [category_id])
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
                      wingshape, specifications, description, history, visibility="visible"):
        self.open()
        self.cursor.execute('''
            INSERT INTO planes (name, category_id, image, country,
                      quantity, producedstart, producedend, cost, 
                      wing_shape, specifications, description, history, visibility)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''',
             [name, category_id, image, country,
                      quantity, produsedstart, produsedend, cost, 
                      wingshape, specifications, description, history, visibility] )
        self.conn.commit()
        self.close()

    def delete_plane(self, plane_id):
        self.open()
        self.cursor.execute(''' DELETE FROM planes WHERE id=?''', [plane_id])
        self.conn.commit()
        self.close()

    def update_plane(self, plane_id, name, category_id, image, country,
                      quantity, producedstart, producedend, cost, 
                      wingshape, specifications, description, history, visibility):
        self.open()
        self.cursor.execute('''UPDATE planes
                            SET name = ?,category_id=?, image = ?, 
                            country=?, quantity=?,producedstart=?,
                            producedend=?,cost=?,wing_shape=?,
                            specifications=?,description=?,history=?, visibility=?
                    WHERE id = ?''',[
                        name, category_id, image, country,
                      quantity, producedstart, producedend, cost, 
                      wingshape, specifications, description, history, visibility, plane_id
                    ])
        self.conn.commit()
        self.close()


    def create_article(self, title, text, image, author):
        self.open()
        self.cursor.execute('''
            INSERT INTO articles (title, text, image, author)
            VALUES (?,?,?,?)''',
             [title, text, image, author] )
        self.conn.commit()
        self.close()

    def delete_article(self, article_id):
        self.open()
        self.cursor.execute(''' DELETE FROM articles WHERE id=?''', [article_id])
        self.conn.commit()
        self.close()

    def get_article_by_id(self, article_id):
        self.open()
        self.cursor.execute('''SELECT * FROM articles WHERE id=? ''', [article_id])
        data = self.cursor.fetchall()
        self.close()
        data = [dict(row) for row in data]
        
        return data[0]
    
    def update_article(self, article_id, title, text, image, author):
        self.open()
        self.cursor.execute('''UPDATE articles
                            SET title = ?,text=?, image = ?, 
                            author=?
                        WHERE id = ?''',[
                            title, text, image, author, article_id
                    ])
        self.conn.commit()
        self.close()
