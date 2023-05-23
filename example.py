import sqlite3

# Establish connection
connection = sqlite3.connect("data.db")
cursor = connection.cursor() # an object that can execute queries

# Query data based on contidion
# * selects all but can select specific columns seperated by commas
cursor.execute("SELECT * FROM events WHERE date='2022.10.10'") # Returns a list of tuples
rows = cursor.fetchall()
print(rows)

# Insert new rows
# Prepare a list of tuples
new_rows = [('Cats', 'Cat City', '2024.10.23'),
            ('Chicken', 'Chicken City', '2024.12.1')]

# ? replaced by value of tuples
cursor.executemany("INSERT INTO events VALUES(?,?,?)", new_rows)
connection.commit() # commit the changes (write)

# Query all data
cursor.execute("SELECT * FROM events")
rows = cursor.fetchall()
print(rows)