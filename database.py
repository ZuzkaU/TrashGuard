import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="username",
  password="password",
  db = "trash"
)

mycursor = mydb.cursor()

def add_user(username, password, name, phone, address):
  if get_user(username):
    return {"code":1, "msg": "User already exists"}

  sql = "insert into users (username, password, points, name, phone, address) values (%s, %s, %s, %s, %s, %s)"
  vals = (username, password, 0, name, phone, address)

  mycursor.execute(sql, vals)
  mydb.commit()

  return {"code":0, "msg":"SUCCESS"}

def get_user(username):
  sql = "select * from users where username = '" + username + "'"
  mycursor.execute(sql)
  myresult = mycursor.fetchall()

  return myresult

def log_in(username, password):
  data = get_user(username)
  if not data:
    return {"code":2, "msg": "User does not exist"}

  if password != data[1]:
    return {"code":3, "msg": "Username and password do not match"}

  return {"code":0, "msg": "SUCCESS"}


# print(add_user("aster", "pass", "a", "b", "c"))
# print(get_user("aster"))

# CREATE TABLE users(
#     username VARCHAR(255) PRIMARY KEY,
#     password VARCHAR(255) NOT NULL,
#     points INT NOT NULL,
#     name VARCHAR(255),
#     phone VARCHAR(255),
#     address VARCHAR(255)
#     );

# CREATE TABLE history(
#   username VARCHAR(255),
#   timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#   action VARCHAR(255),
#   points INT NOT NULL
# );

# CREATE TABLE active_requests(
#     request_id INT AUTO_INCREMENT PRIMARY KEY,
#     latitude INT NOT NULL,
#     longitude INT NOT NULL,
#     action VARCHAR(255),
#     message VARCHAR(255)
# );