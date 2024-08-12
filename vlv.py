from flask import Flask,render_template,request,session
from tabulate import tabulate
from twilio.rest import Client
import sqlite3
app=Flask(__name__)
app.secret_key = "111_vlv"


sid="ACb43647e57171b9015553b0dbc43d71bd"
token="cf809f8b45e71a74b086e7c5870a5405"
mynum="+19492168529"
tonum="+919346745866"


# Dummy database of doctors
doctors = {
    'Dr.Adam Martin': '123',
    'Dr.Eve Martin': '456'
}


def create_connection():
    conn=sqlite3.connect('smbbddl7m.db')
    return conn

def create_table():
    conn=create_connection()
    conn.cursor().execute('''CREATE TABLE IF NOT EXISTS patients(
                          ID INTEGER PRIMARY KEY AUTOINCREMENT,
                          First_name CHAR NOT NULL,
                          Last_name CHAR NOT NULL,
                          Age INTEGER NOT NULL,
                          Gender TEXT NOT NULL,
                          Email_id EMAIL NOT NULL UNIQUE,
                          Mobile_number NUMBER NOT NULL,
                          Issue TEXT NOT NULL,
                          Doctor TEXT NOT NULL,
                          Date DATE NOT NULL,
                          Time TEXT NOT NULL,
                          Address TEXT NOT NULL)''')
    conn.commit()
    conn.close()


@app.route('/appoint',methods=["GET","POST"])
def appoint():
    if request.method=='POST':
        First_name=request.form['First_name']
        Last_name=request.form['Last_name']
        Age=request.form['Age']
        Gender=request.form['Gender']
        Email_id=request.form['Email_id']
        Mobile_number=request.form['Mobile_number']
        Issue=request.form['Issue']
        Doctor=request.form['Doctor']
        Address=request.form['Address']
        Time=request.form['Time']
        Date=request.form['Date']


        conn=create_connection()
        conn.cursor().execute('''INSERT INTO patients('First_name','Last_name','Age','Gender','Email_id','Mobile_number','Issue','Doctor','Address','Time','Date') VALUES(?,?,?,?,?,?,?,?,?,?,?)''',(First_name,Last_name,Age,Gender,Email_id,Mobile_number,Issue,Doctor,Address,Time,Date))
        conn.commit()
        conn.close()

        client=Client(sid,token)
        message=client.messages.create(
        body="THANKS FOR MAKING APPOINTMENT WITH VLV HOSPITAL.WE WILL ALWAYS BE THERE FOR YOU WHENEVER YOU NEED.",
        from_=mynum,
        to=tonum)

        conn = sqlite3.connect('smbbddl7m.db')
        cursor = conn.cursor()

        # Fetch data from the specified table
        cursor.execute('SELECT * FROM patients WHERE First_name = ? ',(First_name,))
        data = cursor.fetchall()
        conn.commit()
        conn.close()
        print(data)
        return render_template('table.html',doc=Doctor,date=Date,time=Time)

    return render_template('appoint.html')



@app.route('/login',methods=["GET","POST"])
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        if username in doctors and doctors[username] == password:
            session['logged_in'] = True
            session['username'] = username
            conn = sqlite3.connect('smbbddl7m.db')
            cursor = conn.cursor()

        # Fetch data from the specified table
            cursor.execute('SELECT First_name,Last_name,Age,Gender,Issue,Date,Time FROM patients WHERE Doctor=? ',(username,))
            data = cursor.fetchall()
            print(data)
        return render_template('display.html',data=data)
    else:
        return render_template('login.html')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__=='__main__':
    create_table()
    app.run(debug=True)