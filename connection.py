
import pymysql
import json

c_info = {
    "host": "user-service-db.ci3ta0leimzm.us-east-2.rds.amazonaws.com",
    "user": "admin",
    "password": "12345678",
    "cursorclass": pymysql.cursors.DictCursor,
}

conn = pymysql.connect(**c_info)

cur = conn.cursor()
res = cur.execute("show databases;")
res = cur.fetchall()

print(f"database: {json.dumps(res, indent=4, default=str)}")


# next show table in schema. 

query_text = """
select *
from rds_user_service.Users;
"""

res = cur.execute(query_text)
res = cur.fetchall()

print(f"query result: {json.dumps(res, indent=4, default=str)}")

