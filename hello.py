from flask import *
import sqlite3
app=Flask(__name__)

class User:
	EmpID=""
	Desg=""
	Name=""
	Qtr_T=""
	Qtr_No=""
	Num=""
	def __init__(self,eid="",desg="",name="",qt="",qn="",num=""):
		self.EmpID=eid
		self.Desg=desg
		self.Name=name
		self.Qtr_T=qt
		self.Qtr_No=qn
		self.Num=num
	def change(self,eid,desg,name,qt,qn,num):
		self.EmpID=eid
		self.Desg=desg
		self.Name=name
		self.Qtr_T=qt
		self.Qtr_No=qn
		self.Num=num

userl=User()

@app.route('/view')
def view():
	con = sqlite3.connect("data.sqlite")
	con.row_factory= sqlite3.Row
	cur=con.cursor()
	cur.execute("Select * from Users")
	rows=cur.fetchall()
	return render_template('view.html',rows=rows)

@app.route('/mainmenu')
def mmenu():
	return render_template("mainmenu.html",user=userl)

@app.route("/")
def begin():
	return render_template("login.html")

@app.route("/logincheck",methods=["POST","GET"])
def check():
	if request.method=="POST":
		user=request.form["user"]
		pwd=request.form["pwd"]
		with sqlite3.connect("data.sqlite") as con:
			cur=con.cursor()
			cur.execute('Select * from users where EmpID = ? AND Password=?',(user,pwd))
			rows=cur.fetchone()
			if user=="admin":
				return render_template("admin.html")
			if rows is None:
				return render_template("fail.html")			
			userl.change(rows[0],rows[1],rows[2],rows[3],rows[4],rows[5])
			return render_template("true.html",user=userl)

if __name__=='__main__':
	app.run(debug=True)