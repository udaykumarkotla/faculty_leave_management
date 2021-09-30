from flask import Flask, render_template, request, redirect, url_for,session
import pymysql.cursors
import pymysql
import re

app = Flask(__name__)

@app.route('/login', methods=['GET','POST'])
def login():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='sreekarteja09',
                                 db='faculty')
    if request.method == 'POST' :
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            with connection.cursor() as cursor:
                 cursor.execute('select username,id from credentials where email=%s and password=%s ',(email,password))
                 account=cursor.fetchone()
                 cursor.execute('select username,id from admins where email=%s and password1=%s',(email,password))
                 acc=cursor.fetchone()
                 cursor.execute('select username,id from headofdept where email=%s and password1=%s', (email, password))
                 hod=cursor.fetchone()
                 cursor.execute('select username,id from princi where email=%s and password1=%s', (email, password))
                 princi=cursor.fetchone()
                 if account:
                     session['loggedin']=True
                     session['username']=account[0]
                     session['id']=account[1]
                     return redirect(url_for('home'))
                 elif acc:
                     session['loggedin'] = True
                     session['username'] = acc[0]
                     session['id'] = acc[1]
                     return render_template('add_user.html', msg="Succes")
                 elif hod:
                     session['loggedin'] = True
                     session['username'] = hod[0]
                     session['id'] = hod[1]
                     return redirect(url_for('Hod_requests'))
                 elif princi:
                     session['loggedin'] = True
                     session['username'] = princi[0]
                     session['id'] = princi[1]
                     return redirect(url_for('Principal_requests'))
                 else:
                     return render_template('lo.html',msg="invalid user")
        finally:
            connection.close()

@app.route('/add_user',methods=['GET','POST'])
def add_user():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='sreekarteja09',
                                 db='faculty')
    if 'loggedin' in session:
        if request.method == 'POST':
            details=request.form
            fname=details['fname']
            lname=details['lname']
            dept=details['de']
            type=details['ty']
            designation = details['designation']
            mobile=details['phone']
            try:
                with connection.cursor() as cursor:
                    sql="insert into basic(fname, lname ,dept ,type ,designation ,mobile) values(%s,%s,%s,%s,%s,%s)"
                    cursor.execute(sql,(fname,lname,dept,type,designation,mobile))
                    connection.commit()
                    return redirect(url_for('Afac_lis'))
            finally:
                connection.close()


@app.route('/check_leave')
def check_leave():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='sreekarteja09',
                                  db='faculty')
    if 'loggedin' in session:
        try:
            with connection.cursor() as cursor:
                cursor.execute("select onduty,annual,casual from stats where id=%s order by rownum desc limit 1",session['id'])
                details = cursor.fetchall()
                if details:
                    return render_template('check_leave.html', details=details)
                else:
                    return render_template('empty3.html')
        finally:
            connection.close()

@app.route('/home')
def home():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='sreekarteja09',
                                 db='faculty')
    if 'loggedin' in session:
        try:
            with connection.cursor() as cursor:
                cursor.execute("select id,username,applied ,noofdays,fromdate,todate,type,reason,status,finalstatus from applyleave where id=%s and (status='Pending' or status='Forwarded to Principal') and (visited=0 or visited=1) and finalstatus='Pending' ",(session['id']))
                details=cursor.fetchall()
                if details:
                    return render_template('faculty_dashboard.html',details=details)
                else:
                    return render_template('empty.html')
        finally:
            connection.close()

@app.route('/profile')
def profile():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='sreekarteja09',
                                 db='faculty')
    if 'loggedin' in session:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM staff where id=%s",session['id'])
                details = cursor.fetchone()
                return render_template('profile.html', details=details)
        finally:
            connection.close()

@app.route('/apply_leave',methods=['GET','POST'])
def apply_leave():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='sreekarteja09',
                                 db='faculty')
    if 'loggedin' in session:
        if request.method == 'POST':
            details = request.form
            id=session['id']
            username=session['username']
            noofdays = details['NOD']
            fromdate = details['fdate']
            todate=details['tdate']
            type=details['tl']
            reason=details['msg']
            try:
                with connection.cursor() as cursor:
                    sql="INSERT INTO applyleave(id,username,noofdays,fromdate,todate,type,reason,applied,time)VALUES(%s,%s,%s,%s,%s,%s,%s,now(),now())"
                    cursor.execute(sql,(id,username,noofdays,fromdate,todate,type,reason));
                connection.commit()
            finally:
                connection.close()
    return redirect(url_for('home'))

@app.route('/change_password',methods=['GET','POST'])
def change_password():
    connection=pymysql.connect(host='localhost',
                                 user='root',
                                 password='sreekarteja09',
                                 db='faculty')
    if 'loggedin' in session:
        if request.method =='POST':
            details=request.form
            id=session['id']
            password=details['password']
            passwordn1=details['passwordn1']
            try:
                with connection.cursor() as cursor:
                    cursor.execute("update credentials set password=%s where id=%s and password=%s",(passwordn1,id,password))
                    connection.commit()
                    return render_template('faculty_dashboard.html')
            finally:
                connection.close()


@app.route('/leave_history')
def leave_history():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='sreekarteja09',
                                 db='faculty')
    if 'loggedin' in session:
        try:
            with connection.cursor() as cursor:
                cursor.execute("select id,username,applied,noofdays,fromdate,todate,type,reason,status,finalstatus from applyleave where id=%s and (status='Rejected' or finalstatus='Accepted')order by time desc",(session['id']))
                details=cursor.fetchall()
                if details:
                    return render_template('leave_history.html',details=details)
                else:
                    return render_template('empty1.html')
        finally:
            connection.close()

@app.route('/fac_lis')
def fac_lis():
    connection=pymysql.connect(host='localhost',
                               user='root',
                               password='sreekarteja09',
                               db='faculty')
    if 'loggedin' in session:
        try:
            with connection.cursor() as cursor:
                cursor.execute("select * from staff");
                details=cursor.fetchall()
                return render_template('fac_list.html',details=details)
        finally:
            connection.close()

@app.route('/Hod_accepted')
def Hod_accepted():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='sreekarteja09',
                                 db='faculty')
    if 'loggedin' in session:
        try:
            with connection.cursor() as cursor:
                cursor.execute("select id,username,noofdays,fromdate,todate,type,reason,status from applyleave where status='Forwarded to principal'")
                details=cursor.fetchall()
                if details:
                    return render_template('hod_accepted.html',details=details)
                else:
                    return render_template('Hodempty.html')
        finally:
            connection.close()

@app.route('/Hod_rejected')
def Hod_rejected():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='sreekarteja09',
                                 db='faculty')
    if 'loggedin' in session:
        try:
            with connection.cursor() as cursor:
                cursor.execute("select id,username,noofdays,fromdate,todate,type,reason,status from applyleave where status='Rejected' and visited=1")
                details = cursor.fetchall()
                if details:
                    return render_template('hod_rejected.html', details=details)
                else:
                    return render_template('hodempty1.html')
        finally:
            connection.close()
@app.route('/Hod_requests')
def Hod_requests():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='sreekarteja09',
                                 db='faculty')
    if 'loggedin' in session:
            try:
                with connection.cursor() as cursor:
                    cursor.execute("select id,username,noofdays,fromdate,todate,type,reason,status from applyleave where status='Pending' and visited=0")
                    detail=cursor.fetchall()
                    if detail:
                        return render_template('forwardtoprinci.html',details=detail)
                    else:
                       return render_template('hodempty3.html')
            finally:
                connection.close()

@app.route('/hod_update',methods=['GET','POST'])
def hod_update():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='sreekarteja09',
                                 db='faculty')
    if 'loggedin' in session:
        if request.method == 'POST':
            details = request.form
            id = details['ID']
            status=details['Pending']
            try:
                with connection.cursor() as cursor:
                    cursor.execute("update applyleave set status=%s, visited=1 where id=%s and visited=0 and status='Pending' order by time desc limit 1 ", (status,id))
                    connection.commit()
                    return redirect(url_for('Hod_requests'))
            finally:
                connection.close()


@app.route('/pfac_lis')
def pfac_lis():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='sreekarteja09',
                                 db='faculty')
    if 'loggedin' in session:
        try:
            with connection.cursor() as cursor:
                cursor.execute("select * from staff");
                details = cursor.fetchall()
                return render_template('pfac_list.html', details=details)
        finally:
            connection.close()


@app.route('/principal_accepted')
def principal_accepted():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='sreekarteja09',
                                 db='faculty')
    if 'loggedin' in session:
        try:
            with connection.cursor() as cursor:
                cursor.execute( "select id,username,noofdays,fromdate,todate,type,reason,status,finalstatus from applyleave where finalstatus='accepted' and visit=1")
                details = cursor.fetchall()
                if details:
                    return render_template('principal_accepted.html', details=details)
                else:
                    return render_template('principalemoty.html')
        finally:
            connection.close()


@app.route('/principal_rejected')
def principal_rejected():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='sreekarteja09',
                                 db='faculty')
    if 'loggedin' in session:
        try:
            with connection.cursor() as cursor:
                cursor.execute("select id,username,noofdays,fromdate,todate,type,reason,status,finalstatus from applyleave where finalstatus='Rejected' and visit=1 ")
                details = cursor.fetchall()
                if details:
                    return render_template('principal_rejected.html', details=details)
                else:
                    return render_template('principalempty1.html')
        finally:
            connection.close()


@app.route('/principal_requests')
def Principal_requests():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='sreekarteja09',
                                 db='faculty')
    if 'loggedin' in session:
        try:
            with connection.cursor() as cursor:
                cursor.execute("select id,username,noofdays,fromdate,todate,type,reason,status from applyleave where status='Forwarded to Principal' and visited=1 and visit=0")
                detail = cursor.fetchall()
                if detail:
                    return render_template('principal_status.html', details=detail)
                else:
                    return render_template('principalempty2.html')
        finally:
            connection.close()


@app.route('/principal_update', methods=['GET', 'POST'])
def principal_update():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='sreekarteja09',
                                 db='faculty')
    if 'loggedin' in session:
        if request.method == 'POST':
            details = request.form
            id = details['ID']
            status = details['Pending']
            try:
                with connection.cursor() as cursor:
                    cursor.execute("update applyleave set finalstatus=%s, visit=1 where id=%s and status='Forwarded to Principal' and visit=0 order by time desc limit 1", (status, id))
                    connection.commit()
                    return redirect(url_for('Principal_requests'))
            finally:
                connection.close()

@app.route('/Afac_lis')
def Afac_lis():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='sreekarteja09',
                                 db='faculty')
    if 'loggedin' in session:
        try:
            with connection.cursor() as cursor:
                cursor.execute("select * from staff");
                details = cursor.fetchall()
                return render_template('Afac_list.html', details=details)
        finally:
            connection.close()


@app.route('/logout')
def logout():
    if 'loggedin' in session:
        session.pop('username',None)
        session.pop('id',None)
        return render_template('lo.html')


if __name__=="__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
    app.run()