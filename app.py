from flask import Flask, request, render_template, redirect
from pony.orm import *

from database import db
from models import ShoppingLista, Proizvod
app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dodaj-listu', methods=['POST'])
@db_session
def dodaj_listu():
    trgovina = request.form.get('trgovina')
    datum = request.form.get('datum')
    ShoppingLista(
        trgovina=trgovina,
        datum=datum
    )
    commit()
    return redirect('/liste')

def lista_id(lista):
    return lista.id
@app.route('/liste')
@db_session
def prikaz_liste():
    trgovina = request.args.get('trgovina')
    if trgovina:
        sve_liste = ShoppingLista.select()
        liste = []
        for lista in sve_liste:
            if lista.trgovina.lower() == trgovina.lower():
                liste.append(lista)
    else:
        liste = list(ShoppingLista.select())
    liste.sort(key=lista_id, reverse=True)
    return render_template(
        'liste.html',
        liste=liste,
        trgovina=trgovina
    )

@app.route('/obrisi-listu/<int:id>', methods=['POST'])
@db_session
def obrisi_listu(id):
    lista = ShoppingLista.get(id=id)
    lista.delete()
    commit()
    return redirect('/liste')

@app.route('/stats')
@db_session
def prikaz_stats():
    liste = ShoppingLista.select()
    trgovine = {}

    for lista in liste:
        if lista.trgovina in trgovine:
            trgovine[lista.trgovina] += 1
        else:
            trgovine[lista.trgovina] = 1

    return render_template(
        'stats.html',
        trgovine = trgovine
    )

def proizvod_id(proizvod):
    return proizvod.id

@app.route('/liste/<int:id>')
@db_session
def detalji_liste(id):
    lista = ShoppingLista.get(id=id)
    proizvodi = sorted(
        lista.proizvodi,
        key=proizvod_id
    )
    return render_template(
        'proizvodi.html',
        lista=lista,
        proizvodi=proizvodi
    )

@app.route('/liste/<int:id>/dodaj-proizvod', methods=['POST'])
@db_session
def dodaj_proizvod(id):
    lista = ShoppingLista.get(id=id)
    naziv = request.form.get('naziv')
    kolicina = request.form.get('kolicina')
    Proizvod(
        naziv=naziv,
        kolicina=int(kolicina),
        lista=lista
    )
    commit()
    return redirect(f'/liste/{id}')

@app.route('/proizvod/toggle/<int:id>', methods=['POST'])
@db_session
def toggle_proizvod(id):
    proizvod = Proizvod.get(id=id)
    proizvod.kupljeno = not proizvod.kupljeno
    commit()
    return redirect(f'/liste/{proizvod.lista.id}')

@app.route('/proizvod/obrisi/<int:id>', methods=['POST'])
@db_session
def obrisi_proizvod(id):
    proizvod = Proizvod.get(id=id)
    lista_id = proizvod.lista.id
    proizvod.delete()
    commit()
    return redirect(f'/liste/{lista_id}')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
