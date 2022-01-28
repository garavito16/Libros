from libros.config.mysqlconnection import connectToMySQL
from libros.models import model_author

class Book:
    name_db = "esquema_libros"

    def __init__(self,id,titulo,num_paginas,created_at):
        self.id = id
        self.titulo = titulo
        self.num_paginas = num_paginas
        self.created_at = created_at
        self.autores = []

    def addAutor(self,autor):
        self.autores.append(autor)

    @classmethod
    def getLibros(cls):
        query = "SELECT * FROM libros"
        resultado = connectToMySQL(cls.name_db).query_db(query)
        return resultado

    @classmethod
    def createLibro(cls,data):
        query = "INSERT INTO libros (titulo, num_paginas,created_at) VALUES (%(titulo)s,%(num_paginas)s,now());"
        resultado = connectToMySQL(cls.name_db).query_db(query,data)
        return resultado

    @classmethod
    def getAuthorFavoriteOfBooks(cls,data):
        query = '''
                    SELECT aux.*, l.titulo, l.num_paginas,  l.id AS id_libro, l.created_at AS created_at_libro
                    FROM libros l 
                    LEFT JOIN (SELECT a.*, f.libro_id
                    FROM autores a
                    INNER JOIN favoritos f ON a.id = f.autor_id) aux ON aux.libro_id = l.id
                    WHERE l.id = %(libro_id)s
                '''
        resultado = connectToMySQL(cls.name_db).query_db(query,data)
        print(resultado)
        book = None
        if len(resultado) > 0:
            book = Book(resultado[0]["id_libro"],resultado[0]["titulo"],resultado[0]["num_paginas"],resultado[0]["created_at_libro"])
            for autor in resultado:
                if autor["id"] != None:
                    book.addAutor(model_author.Autor(autor["id"],autor["nombres"],autor["apellidos"],autor["created_at"]))
        return book

    @classmethod
    def getAuthorsNoFavoriteOfBook(cls,data):
        query = '''
                SELECT a.* FROM autores a
                LEFT JOIN (
                SELECT a.id, f.libro_id
                FROM autores a
                INNER JOIN favoritos f ON a.id = f.autor_id
                WHERE f.libro_id = %(libro_id)s)aux ON a.id = aux.id
                WHERE aux.libro_id IS NULL
                '''
        resultado = connectToMySQL(cls.name_db).query_db(query,data)
        return resultado

    @classmethod
    def getAddAuthorFavorite(cls,data):
        query = "INSERT INTO favoritos (autor_id,libro_id,created_at) VALUES (%(autor_id)s,%(libro_id)s,now());"
        resultado = connectToMySQL(cls.name_db).query_db(query,data)
        return resultado