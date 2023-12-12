from flask import Flask,jsonify,render_template,request,redirect,session,url_for,sessions,Response
import mysql as sql

app = Flask(__name__)
app.secret_key = 'C@NYoUh@cktHiS'

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

@app.route('/roles')
def user_roles():
  roles_date = {
    1:"data",
    2:"nodata"
  }
  
  return jsonify(roles_data)

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

@app.route('/user')
def user():
  return render_template('user/index.html')

@app.route('/admin/logout')
def adminLogout():
   session.pop('user',None)
   return redirect(url_for('index'))

@app.route('/police/logout')
def policeLogout():
   session.pop('user',None)
   return redirect(url_for('index'))

@app.route('/police/<page>')
def police_dashboard(page):
  return render_template('police/dashboard.html',officer_name="Shubham Nishad",url=page,ps_counts=len(p_stations),c_counts=10,fir_counts=3,po_counts=5)

@app.route('/admin/<page>')
def admin_dashboard(page):
  return render_template('admin/dashboard.html',url=page,ps_counts=len(p_stations),c_counts=10,fir_counts=3,po_counts=5)


@app.route('/api/police_stations',methods=['GET'])
def api_police_stations():
  return jsonify(p_stations)

@app.route('/api/police',methods=['GET'])
def api_police():
  return jsonify(p_officers)

@app.route('/api/categories')
def api_categories():
  return jsonify(crime_categories)

if __name__ == '__main__':
  app.run(debug=True)