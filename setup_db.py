"""
Database setup script - creates the MySQL database and runs migrations.
Run this once: python setup_db.py
"""
import pymysql

# Create database if it doesn't exist
conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='May202005@',
    charset='utf8mb4'
)

cursor = conn.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS `jobtrack` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
cursor.execute("USE `jobtrack`;")
conn.commit()
cursor.close()
conn.close()

print("✓ Database 'jobtrack' created/verified.")
print("Now run: flask db init && flask db migrate -m 'initial' && flask db upgrade")
