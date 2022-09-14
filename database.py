import re
import sqlite3
from typing import List
from utils import User

class DataBase:

   cursor: sqlite3.Cursor
   connection: sqlite3.Connection

   def __init__(self) -> None:
      conn = sqlite3.connect('users.db')

      self.connection = conn
      self.cursor = conn.cursor()

      self.cursor.execute("""CREATE TABLE IF NOT EXISTS Users(
         userid INTEGER PRIMARY KEY AUTOINCREMENT,
         username VARCHAR(20) CHECK( LENGTH(username) <= 20 ) NOT NULL,
         psw_hash TEXT NOT NULL,
         rank TEXT CHECK( rank IN
            ('beginner','curious','traveler','geographer','omniscient') )
            NOT NULL DEFAULT 'beginner'
         );
      """)
   
   def add_user(self, user: User) -> None:
      '''
      Add a user to the database with the structure:
      User(username:str, psw_hash:str, rank.str)
      '''
      # TODO:Evitar sql injection
      self.cursor.execute(f"INSERT INTO Users(username, psw_hash ,rank)\
         VALUES ('{user.username}', '{user.psw_hash}', '{user.rank}');")
      self.connection.commit()
      print('A new user is added')

   def get_user(self, username: str) -> User:
      '''
      Get a username and returns the user with that name if ti exists
      or the empty template User(username='', psw_hash='', rank='') in
      other case.
      '''
      user = User("","","")
      self.cursor.execute(f"SELECT * FROM Users WHERE Users.username = '{username}'")
      results = self.cursor.fetchall()
      if len(results) > 0:
         user = User(results[0][1],results[0][2],results[0][3])
      return user

   def get_all_users(self) -> List[User]:
      results = self.cursor.execute(f"SELECT * FROM Users").fetchall()
      # print(results)
      return results

# cur.execute("SELECT * FROM users;")
# one_result = cur.fetchone() #3
# print(one_result)

# cur.execute("DELETE FROM users WHERE lname='Parker';")
# conn.commit()

# db = DataBase()
# db.get_all_users()