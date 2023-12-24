from flask import Flask,jsonify,render_template,request,redirect,session,url_for,sessions,Response
from flask_mysqldb import MySQL
import json

app = Flask(__name__)
app.secret_key = 'C@NYoUh@cktHiS'

app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "Demon@72074"
app.config["MYSQL_DB"] = "policemngmt"

mysql = MySQL(app)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/admin',methods=['GET','POST'])
def admin():
  if request.method == "POST":
    session['user'] = 'admin'
    return redirect('admin/dashboard')
  if request.method == 'GET':
    if session.get('user') :
      if session['user'] == 'admin':
        return redirect('admin/dashboard')
      else:
        page = session['user']
        return redirect(page+'/dashboard')
    return render_template('admin/index.html')


@app.route('/police',methods=['GET','POST'])
def police():
  if request.method == "POST":
    session['user'] = 'police'
    return redirect('police/dashboard')
  if request.method == 'GET':
    if session.get('user') :
      if session['user'] == 'police':
        return redirect('police/dashboard')
      else:
        page = session['user']
        return redirect(page+'/dashboard')
    return render_template('police/index.html')
    
@app.route('/user',methods=['GET','POST'])
def user():
  if request.method == "POST":
    session['user'] = 'user'
    return redirect('user/dashboard')
  if request.method == 'GET':
    if session.get('user') :
      if session['user'] == 'user':
        return redirect('user/dashboard')
      else:
        page = session['user']
        return redirect(page+'/dashboard')
  return render_template('user/index.html')

@app.route('/admin/logout')
def adminLogout():
   session.pop('user',None)
   return redirect(url_for('index'))

@app.route('/police/logout')
def policeLogout():
   session.pop('user',None)
   return redirect(url_for('index'))

@app.route('/user/logout')
def userLogout():
   session.pop('user',None)
   return redirect(url_for('index'))

@app.route('/police/<page>')
def police_dashboard(page):
  return render_template('police/dashboard.html',url=page)

@app.route('/admin/<page>')
def admin_dashboard(page):
  return render_template('admin/dashboard.html',url=page)

@app.route('/user/<page>')
def user_dashboard(page):
  return render_template('user/dashboard.html',url=page)

def countPS():
  return len(api_police_stations())

@app.route('/api/police_stations',methods=['GET'])
def api_police_stations():
  cur = mysql.connection.cursor()
  cur.execute("""SELECT * FROM policemngmt.police_stations""")
  row_headers=[x[0] for x in cur.description]
  rv = cur.fetchall()
  p_stations=[]
  for result in rv:
    p_stations.append(dict(zip(row_headers,result)))
  cur.close()
  return jsonify(p_stations)

@app.route('/api/police',methods=['GET'])
def api_police():
  cur = mysql.connection.cursor()
  cur.execute("""SELECT * FROM policemngmt.p_officers""")
  row_headers=[x[0] for x in cur.description]
  rv = cur.fetchall()
  p_officers=[]
  for result in rv:
    p_officers.append(dict(zip(row_headers,result)))
  cur.close()
  return jsonify(p_officers)

@app.route('/api/categories')
def api_categories():
  cur = mysql.connection.cursor()
  cur.execute("""SELECT * FROM policemngmt.crime_categories""")
  row_headers=[x[0] for x in cur.description]
  rv = cur.fetchall()
  crime_categories=[]
  for result in rv:
    crime_categories.append(dict(zip(row_headers,result)))
  cur.close()
  return jsonify(crime_categories)

@app.route('/api/roles')
def user_roles():
  cur = mysql.connection.cursor()
  cur.execute("""SELECT * FROM policemngmt.user_roles""")
  row_headers=[x[0] for x in cur.description]
  rv = cur.fetchall()
  json_data=[]
  for result in rv:
    json_data.append(dict(zip(row_headers,result)))
  cur.close()
  return jsonify(json_data)





if __name__ == '__main__':
  app.run(debug=True)