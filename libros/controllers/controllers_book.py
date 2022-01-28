
from flask import redirect, render_template, request
from libros.models.model_author import Autor
from libros.models.model_book import Book
from libros import app

@app.route('/books',methods=["GET"])
def getBooks():
    books = Book.getLibros()
    return render_template('books.html',books=books)

@app.route('/create_book',methods=["POST"])
def create_book():
    book = {
        "titulo" : request.form["titulo"],
        "num_paginas" : request.form["num_paginas"]
    }
    resultado = Book.createLibro(book)
    print(resultado)
    if (resultado > 0):
        return redirect('/books')

@app.route('/books/<id_libro>',methods=["GET"])
def view_author_of_books(id_libro):
    data = {
        "libro_id" : id_libro
    }
    book = Book.getAuthorFavoriteOfBooks(data)
    AuthorsNoFavorite = Book.getAuthorsNoFavoriteOfBook(data)
    return render_template('mostrar_libro.html',books=book,AuthorsNoFavorite=AuthorsNoFavorite)

@app.route('/add_author_favorite',methods=["POST"])
def add_author_favorite():
    libro_id = request.form["libro_id"]
    data = {
        "autor_id" : request.form["autor_id"],
        "libro_id" : request.form["libro_id"]
    }
    resultado = Book.getAddAuthorFavorite(data)
    print(resultado)
    if (resultado > 0):
        return redirect('/books/'+libro_id)