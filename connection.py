
import pymysql

c_info = {
    "host": "user-service-db.ci3ta0leimzm.us-east-2.rds.amazonaws.com",
    "user": "admin",
    "password": "12345678",
    "cursorclass": pymysql.cursor.DictCursor,
}

conn = pymysql.connect(**c_info)
