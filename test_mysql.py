import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="pythoncourse",
    database="school"
)

cursor = conn.cursor()
cursor.execute("SELECT * FROM students LIMIT 1")
result = cursor.fetchall()
print(result)

cursor.close()
conn.close()
