import sqlite3

CONN = sqlite3.connect('recipe.db')
CURSOR = CONN.cursor()