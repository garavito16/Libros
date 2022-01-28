
from flask import redirect, render_template, request
from libros.models.model_author import Autor
from libros import app

@app.route('/authors',methods=["GET"])
def getAuthors():
    autores = Autor.getAutores()
    return render_template('autores.html',autores=autores)

@app.route('/create_author',methods=["POST"])
def create_author():
    author = {
        "nombres" : request.form["nombres"],
        "apellidos" : request.form["apellidos"]
    }
    resultado = Autor.createAuthor(author)
    print(resultado)
    if (resultado > 0):
        return redirect('/authors')

@app.route('/authors/<id_author>',methods=["GET"])
def view_books_of_author(id_author):
    author = {
        "autor_id" : id_author
    }
    autor = Autor.getBooksFavoriteOfAuthor(author)
    booksNoFavorite = Autor.getBooksNoFavoriteOfAuthor(author)
    return render_template('mostrar_autor.html',autor=autor,booksNoFavorite=booksNoFavorite)

@app.route('/add_book_favorite',methods=["POST"])
def add_book_favorite():
    autor_id = request.form["autor_id"]
    data = {
        "autor_id" : request.form["autor_id"],
        "libro_id" : request.form["libro_id"]
    }
    resultado = Autor.getAddBookFavorite(data)
    print(resultado)
    if (resultado > 0):
        return redirect('/authors/'+autor_id)