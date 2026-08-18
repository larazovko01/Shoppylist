from pony.orm import *
from database import db

class ShoppingLista(db.Entity):
    id = PrimaryKey(int, auto=True)
    trgovina = Required(str)
    datum = Required(str)

    proizvodi = Set('Proizvod')
    
class Proizvod(db.Entity):
    id = PrimaryKey(int, auto=True)
    naziv = Required(str)
    kolicina = Required(int)
    kupljeno = Required(bool, default=False)

    lista = Required(ShoppingLista)