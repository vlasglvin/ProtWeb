from functools import wraps
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

    def get_query(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            self.open()
            data = func(self, *args, **kwargs)
            self.close()
            if type(data) == list:
                data = [dict(row) for row in data]
            elif data is not None:
                data = dict(data)
            else:
                data = None
            return data
        
        return wrapper

    def post_query(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            self.open()
            func(self, *args, **kwargs)
            self.conn.commit()
            self.close()

        return wrapper


    @get_query
    def get_all_planes(self):
        self.cursor.execute('''SELECT * FROM planes WHERE visibility="visible"''')
        return self.cursor.fetchall()   

    @get_query
    def get_suggested_planes(self):
        self.cursor.execute('''SELECT * FROM planes WHERE visibility="hidden"''')
        return self.cursor.fetchall()
    
    @get_query
    def get_plane(self, name):
        self.cursor.execute('''SELECT * FROM planes WHERE name=? AND visibility="visible" ''', [name])
        return self.cursor.fetchone()

        
    @get_query
    def get_plane_by_id(self, plane_id):
        
        self.cursor.execute('''SELECT * FROM planes WHERE id=? ''', [plane_id])
        return self.cursor.fetchone()
        
    @get_query
    def get_all_categories(self):
        self.cursor.execute('''SELECT * FROM categories ''')
        return self.cursor.fetchall()
     
    @get_query
    def get_planes_by_category(self, category_id):
        self.cursor.execute('''SELECT * FROM planes WHERE category_id=? AND visibility="visible"''', [category_id])
        return self.cursor.fetchall()
        
    @get_query   
    def get_category(self, category_id):
       
        self.cursor.execute('''SELECT * FROM categories WHERE id=? ''', [category_id])
        return self.cursor.fetchone()
    
    def get_all_planes_by_categories(self):
        planes = {}
        categories = self.get_all_categories()
        for category in categories:
            category_planes = self.get_planes_by_category(category['id'])
            planes[category['title']] = category_planes

        return planes
    @get_query
    def search_planes(self, query):
        query = query + '%'
        self.cursor.execute('''SELECT * FROM planes WHERE (name LIKE ? OR country LIKE ? OR wing_shape LIKE ? OR producedstart LIKE ? OR description LIKE ?)''', 
                            [query , query, query, query, query])
        return self.cursor.fetchall()

    @get_query
    def get_all_articles(self):
        self.cursor.execute('''SELECT * FROM articles ''')
        return self.cursor.fetchall()
     
    @get_query
    def check_login_data(self, username):
        self.cursor.execute('''SELECT * FROM users WHERE username=?''',
                            [username])
        return self.cursor.fetchone()

    @get_query    
    def get_user(self, user_id):
        self.cursor.execute('''SELECT * FROM users WHERE id=?''',
                            [user_id])
        return self.cursor.fetchone()
       
    @get_query    
    def is_username_exist(self, username):
        self.cursor.execute('''SELECT * FROM users WHERE username=?''',
                            [username])
        return self.cursor.fetchone()

    @get_query     
    def is_email_exist(self, email):
        self.cursor.execute('''SELECT * FROM users WHERE email=?''',
                            [email])
        return self.cursor.fetchone()
        
    @post_query
    def create_user(self, name, username, email, password):
        self.cursor.execute('''
            INSERT INTO users (name, username, email, password)
            VALUES (?,?,?,?)''',
             [ name, username, email, password] )
        

    @post_query
    def create_plane(self, name, category_id, image, country,
                      quantity, produsedstart, produsedend, cost, 
                      wingshape, specifications, description, history, visibility="visible"):
        self.cursor.execute('''
            INSERT INTO planes (name, category_id, image, country,
                      quantity, producedstart, producedend, cost, 
                      wing_shape, specifications, description, history, visibility)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''',
             [name, category_id, image, country,
                      quantity, produsedstart, produsedend, cost, 
                      wingshape, specifications, description, history, visibility] )


    @post_query
    def delete_plane(self, plane_id):
        self.cursor.execute(''' DELETE FROM planes WHERE id=?''', [plane_id])
    
    @post_query
    def update_plane(self, plane_id, name, category_id, image, country,
                      quantity, producedstart, producedend, cost, 
                      wingshape, specifications, description, history, visibility):
       
        self.cursor.execute('''UPDATE planes
                            SET name = ?,category_id=?, image = ?, 
                            country=?, quantity=?,producedstart=?,
                            producedend=?,cost=?,wing_shape=?,
                            specifications=?,description=?,history=?, visibility=?
                    WHERE id = ?''',[
                        name, category_id, image, country,
                      quantity, producedstart, producedend, cost, 
                      wingshape, specifications, description, history, visibility,   plane_id
                    ])
       

    @post_query
    def create_article(self, title, text, image, author):
        self.cursor.execute('''
            INSERT INTO articles (title, text, image, author)
            VALUES (?,?,?,?)''',
             [title, text, image, author] )

    @post_query
    def delete_article(self, article_id):
        self.cursor.execute(''' DELETE FROM articles WHERE id=?''', [article_id])

    @get_query   
    def get_article_by_id(self, article_id):
        self.cursor.execute('''SELECT * FROM articles WHERE id=? ''', [article_id])
        return self.cursor.fetchone()
  
    
    @post_query
    def update_article(self, article_id, title, text, image, author):
        self.cursor.execute('''UPDATE articles
                            SET title = ?,text=?, image = ?, 
                            author=?
                        WHERE id = ?''',[
                            title, text, image, author, article_id
                    ])
