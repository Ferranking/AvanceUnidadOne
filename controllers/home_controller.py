from flask import render_template

def index():
    data = {
        "title": "Mi Página de Inicio",
        "message": "Bienvenido a mi sitio web!"
    }
    return render_template("index.html", data=data)