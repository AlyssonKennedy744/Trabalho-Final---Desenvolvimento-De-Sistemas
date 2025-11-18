import sqlite3

class Database:
    def __init__(self, db_name="filmes.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS categorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS filmes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                diretor TEXT,
                ano INTEGER,
                categoria_id INTEGER,
                FOREIGN KEY (categoria_id) REFERENCES categorias(id)
            )
        """)
        self.cursor.execute("SELECT count(*) FROM categorias")
        if self.cursor.fetchone()[0] == 0:
            self.cursor.executemany("INSERT INTO categorias (nome) VALUES (?)", 
                                    [('Ação',), ('Comédia',), ('Drama',), ('Sci-Fi',)])
            self.conn.commit()
        self.conn.commit()
    
    def add_filme(self, titulo, diretor, ano, categoria_id):
        self.cursor.execute("INSERT INTO filmes (titulo, diretor, ano, categoria_id) VALUES (?, ?, ?, ?)",
                            (titulo, diretor, ano, categoria_id))
        self.conn.commit()

    def get_filmes(self):
        query = """
            SELECT f.id, f.titulo, f.diretor, f.ano, c.nome 
            FROM filmes f
            JOIN categorias c ON f.categoria_id = c.id
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def update_filme(self, id, titulo, diretor, ano, categoria_id):
        self.cursor.execute("""
            UPDATE filmes SET titulo=?, diretor=?, ano=?, categoria_id=? WHERE id=?
        """, (titulo, diretor, ano, categoria_id, id))
        self.conn.commit()

    def delete_filme(self, id):
        self.cursor.execute("DELETE FROM filmes WHERE id=?", (id,))
        self.conn.commit()

    def get_categorias(self):
        self.cursor.execute("SELECT * FROM categorias")
        return self.cursor.fetchall()