from libros.config.mysqlconnection import connectToMySQL
from libros.models import model_book

class Autor:
    name_db = "esquema_libros"

    def __init__(self,id,nombres,apellidos,created_at):
        self.id = id
        self.nombres = nombres
        self.apellidos = apellidos
        self.created_at = created_at
        self.books = []


    def addBook(self,book):
        self.books.append(book)

    @classmethod
    def getAutores(cls):
        query = "SELECT * FROM autores"
        resultado = connectToMySQL(cls.name_db).query_db(query)
        return resultado

    @classmethod
    def createAuthor(cls,data):
        query = "INSERT INTO autores (nombres, apellidos,created_at) VALUES (%(nombres)s,%(apellidos)s,now());"
        resultado = connectToMySQL(cls.name_db).query_db(query,data)
        return resultado

    @classmethod
    def getBooksFavoriteOfAuthor(cls,data):
        query = '''
                    SELECT aux.*, a.nombres, a.apellidos, a.created_at as created_at_autor, a.id AS id_autor
                    FROM autores a 
                    LEFT JOIN (SELECT l.*, f.autor_id
                    FROM libros l 
                    INNER JOIN favoritos f ON l.id = f.libro_id) aux ON aux.autor_id = a.id
                    WHERE a.id = %(autor_id)s
                '''
        resultado = connectToMySQL(cls.name_db).query_db(query,data)
        autor = None
        if len(resultado) > 0:
            print("id de autor")
            print(resultado[0]["id_autor"])
            autor = Autor(resultado[0]["id_autor"],resultado[0]["nombres"],resultado[0]["apellidos"],resultado[0]["created_at_autor"])
            for book in resultado:
                if book["id"] != None:
                    autor.addBook(model_book.Book(book["id"],book["titulo"],book["num_paginas"],book["created_at"]))
        return autor
    
    @classmethod
    def getAddBookFavorite(cls,data):
        query = "INSERT INTO favoritos (autor_id,libro_id,created_at) VALUES (%(autor_id)s,%(libro_id)s,now());"
        resultado = connectToMySQL(cls.name_db).query_db(query,data)
        return resultado

    @classmethod
    def getBooksNoFavoriteOfAuthor(cls,data):
        query = '''
                SELECT li.* FROM libros li
                LEFT JOIN (
                SELECT l.id, f.autor_id
                FROM libros l 
                INNER JOIN favoritos f ON l.id = f.libro_id
                WHERE f.autor_id = %(autor_id)s)aux ON li.id = aux.id
                WHERE aux.autor_id IS NULL
                '''
        resultado = connectToMySQL(cls.name_db).query_db(query,data)
        return resultado