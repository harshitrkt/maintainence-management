import sqlite3

conn = sqlite3.connect('data.sqlite')
print ("Opened database successfully");

user=input("Username: ")
pw=input("Password: ")
cursor = conn.execute("SELECT EmpID,Password from Users")
flag=0;
for row in cursor:
	if row[0]==user and row[1]==pw:
		print("User found")
		flag=1;
if flag==0:
	print("Incorrect UserID")
print ("Operation done successfully");
conn.close()