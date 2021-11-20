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
  if myresult == []:
    return myresult
  return myresult[0]

def log_in(username, password):
  data = get_user(username)
  if not data:
    return {"code":2, "msg": "User does not exist"}

  if password != data[1]:
    return {"code":3, "msg": "Username and password do not match"}

  return {"code":0, "msg": "SUCCESS"}

def log_action(username, action, points):
  sql = "insert into history (username, action, points) values (%s, %s, %s)"
  vals = (username, action, points)
  mycursor.execute(sql, vals)

  user_data = get_user(username)
  prev_points = user_data[0][2]
  sql = "update users set points = %s where username = %s"
  vals = (int(points) + prev_points, username)
  mycursor.execute(sql, vals)

  mydb.commit()

def log_active_request(latitude, longitude, action, message):
  sql = "insert into active_requests (latitude, longitude, action, message) values (%s, %s, %s, %s)"
  vals = (latitude, longitude, action, message)
  mycursor.execute(sql, vals)
  mydb.commit()

def get_request_data(latitude, longitude):
  sql = "select * from active_requests where latitude = '%s' and longitude = '%s'"
  vals = (latitude, longitude)
  mycursor.execute(sql, vals)
  myresult = mycursor.fetchall()
  return myresult

def get_active_requests():
  sql = "select * from active_requests"
  mycursor.execute(sql)
  myresult = mycursor.fetchall()
  return myresult

def rm_requests(latitude, longitude):
  sql = "delete from active_requests where latitude = '%s' and longitude = '%s'"
  vals = (latitude, longitude)
  mycursor.execute(sql, vals)
  mydb.commit()


# lat, lon = 48.1105110, 11.5839377
# log_active_request(lat, lon, "report", "asdfghjk")
# lat, lon = 48.1105110, 11.5839377
# log_active_request(lat, lon, "report", "asdfghjk")
# lat, lon = 48.1096278, 11.5845053
# log_active_request(lat, lon, "report", "asdfghjk")

# log_action("aster", "report", 1)
# log_active_request(1000, 1000, "report", "asdfghjk")
# log_action("aster", "pickup", 10)
# log_action("aster", "report", 1)
# log_active_request(1000, 1001, "report", "asdfghjk")
# log_action("aster", "report", 1)
# log_active_request(1000, 1001, "report", "asdfghjk")
# rm_requests(1000, 1001)
# print(get_request_data(1000, 1000))

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
#     latitude VARCHAR(255) NOT NULL,
#     longitude VARCHAR(255) NOT NULL,
#     action VARCHAR(255),
#     message VARCHAR(255)
# );
