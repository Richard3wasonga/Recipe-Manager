from models.__init__ import CONN, CURSOR
from models.recipe import Recipe
#from models.ingredient import Ingredient
import ipdb

def testing():
    Recipe.drop_table()
    Recipe.create_table()

    rice = Recipe.create("rice", "chinese", "30")

testing()
ipdb.set_trace()