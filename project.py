from flask import *
import sqlite3
app=Flask(__name__)

class User:
	EmpID=""
	Desg=""
	Name=""
	Qtr_No=""
	Num=""
	def change(self,eid,desg,name,qn,num):
		self.EmpID=eid
		self.Desg=desg
		self.Name=name
		self.Qtr_No=qn
		self.Num=num
	def clear(self):
		self.EmpID=""
		self.Desg=""
		self.Name=""
		self.Qtr_No=""
		self.Num=""
	def check(self):
		if self.Name == "":
			return 1

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

@app.route('/newreq')
def newreq():
	return render_template("newreq.html",user=userl)

@app.route('/pending')
def pending():
	return render_template("pending.html",user=userl)

@app.route('/completed')
def completed():
	return render_template("completed.html",user=userl)

@app.route('/exit')
def exit():
	userl.clear()
	return render_template("exit.html",user=userl)

@app.route('/newAcc')
def newacc():
	return render_template("newAcc.html")

@app.route("/")
def begin():
	return render_template("login.html")

@app.route("/saveacc",methods=["POST","GET"])
def saveacc():
	if request.method=="POST":
		eid=request.form["EmpID"]
		sal=request.form["sal"]
		name=request.form["name"]
		qn=request.form["qtrno"]
		num=request.form["num"]
		pwd=request.form["pwd"]
		with sqlite3.connect("data.sqlite") as con:
			cur=con.cursor()
			cur.execute('Select * from users where EmpID = ? OR Name = ?',(eid,name))
			rows=cur.fetchone()
			if rows is None:
				if eid is ""  or name is "" or qn is "" or num is "" or pwd is "":
					return render_template("useraddfail.html") 
				cur.execute("INSERT into Users Values(?,?,?,?,?,?)",(eid,sal,name,qn,num,pwd))
				con.commit()	
				return render_template("useraddsuccess.html")
			else:			
				con.rollback()
				return render_template("useraddfail.html")
		

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
			userl.change(rows[0],rows[1],rows[2],rows[3],rows[4])
			return render_template("true.html",user=userl)

if __name__=='__main__':
	app.run(debug=True)