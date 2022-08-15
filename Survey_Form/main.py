from flask import *
from flask_mysqldb import *


app=Flask(__name__ , template_folder='templates')


app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='Muthu@123'
app.config['MYSQL_DB']='survey'
#app.config['MYSQL_CURSORCLASS']='DictCursor'
#app.config['UPLOAD_FOLDER']='C:/Users/s/Documents/newpro/upload'
mysql=MySQL(app)




@app.route('/')
def home():
 	return render_template("home.html")

@app.route('/form', methods=['GET','POST'])
def form():
	if request.method=='POST':
		fname=request.form['fname']
		lname=request.form['lname']
		name=fname+lname         
		dob=request.form['db']
		age=request.form['age']
		gender=request.form['gender']
		mobile_num=request.form['num']
		email=request.form['Email']
		faname=request.form['faname']
		foc=request.form['fac']
		maname=request.form['maname']
		adress=request.form['Address']
		city=request.form['city']
		state=request.form['sta']
		pincode=request.form['pin']
		hiqual=request.form['select']
		major=request.form['major']
		perc=request.form['perc']
		rollno=request.form['roll']
		resume=request.files['resume']
		f_name=resume.filename
		bfile=resume.read()
		print("saved")
		tenperc=request.form['1perc']
		twleperc=request.form['2perc']
		pic=request.files['pic']
		pic_name=pic.filename
		bpic=pic.read()
		print("saved")

	
	

		mycursor=mysql.connection.cursor()

		#f_query="insert into personal(rollno,name,dob,age,gender,faname,foc,maname,adress,city,state,pincode) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(rollno,name,dob,age,gender,faname,foc,maname,adress,city,state,pincode)
		mycursor.execute("insert into personal(rollno,name,dob,age,gender,faname,foc,maname,adress,city,state,pincode) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(rollno,name,dob,age,gender,faname,foc,maname,adress,city,state,pincode))
		
		#s_query="insert into quali(rollno,hiqual,major,perc,resume,tenperc,twleperc) values(%s,%s,%s,%s,%s,%s,%s)",(rollno,hiqual,major,perc,resume,tenperc,twleperc)

		mycursor.execute("insert into quali(rollno,hiqual,major,perc,resume,tenperc,twleperc,fname) values(%s,%s,%s,%s,%s,%s,%s,%s)",(rollno,hiqual,major,perc,resume,tenperc,twleperc,f_name))
		
		#t_query="insert into con(rollno,mobile_num,email,pic) values (%s,%s,%s,%s)",(rollno,mobile_num,email,pic)
		mycursor.execute("insert into con(rollno,mobile_num,email,pic,picname) values (%s,%s,%s,%s,%s)",(rollno,mobile_num,email,pic,pic_name))

		mysql.connection.commit()
		mycursor.close()
		return '<h3>Register Sucees<h3><p>You can Safe now Close Window</p>'    
	return render_template("form.html")


@app.route('/admin', methods=['GET','POST'])
def admin():
	if request.method=='GET':
		mycursor=mysql.connection.cursor()
		mycursor.execute("select * from Personal")
		data=mycursor.fetchall()
	return render_template("admin.html", dataf=data)


@app.route('/view,<rollno>', methods=['GET','POST'])
def view(rollno):
	if request.method=='GET':
		mycursor=mysql.connection.cursor()
		mycursor.execute("select * from personal where rollno=%s",(rollno,))
		datas=mycursor.fetchall()
		mycursor.execute("select * from con where rollno=%s",(rollno,))
		datas_1=mycursor.fetchall()
		mycursor.execute("select * from quali where rollno=%s",(rollno,))
		datas_2=mycursor.fetchall()
	return render_template('view.html',datas=datas,datas_1=datas_1,datas_2=datas_2)	





@app.route('/download,<data>')
def download(data):
	mycursor=mysql.connection.cursor()
	mycursor.execute("select * from quali where fname=%s",(data,))
	ans=mycursor.fetchall()
	for i  in ans: 
		with open(i[8],'wb') as s:
			s.write(i[4])
	path=i[8]
	return send_file(path,as_attachment=True)

@app.route('/downloadby,<data>')
def downloadby(data):
	mycursor=mysql.connection.cursor()
	mycursor.execute("select * from con where picname=%s",(data,))
	ans=mycursor.fetchall()
	for i  in ans:
		with open(i[5],'wb') as s:
			s.write(i[3])
	path=i[5]
	return send_file(path,as_attachment=True)




@app.route('/login',methods=['GET','POST'])
def login():
	if request.method=='POST':
		userid=request.form["userid"]
		password=request.form["password"]
		mycursor=mysql.connection.cursor()

		mycursor.execute("select * from user_login where username=%s",(userid,))
		row=mycursor.fetchall()
		for user in row:
			if user[0]==userid and user[1]==password:
				return redirect('/admin')

		else:
			return "<h2>invalid</h2>"

	return render_template('login.html')		
				 





if __name__=='__main__':
	app.run(debug=True)
 	
	
        
        
		


