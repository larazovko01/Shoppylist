from pony.orm import *

db = Database()

db.bind(
    provider='sqlite',
    filename='shoppy.sqlite',
    create_db=True,
)

import models
db.generate_mapping(create_tables=True)


