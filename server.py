import sqlite3

DATABASE = 'dev_rev.db'
conn = sqlite3.connect(DATABASE)
conn.row_factory = sqlite3.Row

    
create_database()
