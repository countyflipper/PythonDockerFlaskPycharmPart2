from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'dbMLB'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'MLB Project'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblMLB')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, mlb=result)


@app.route('/view/<int:mlb_id>', methods=['GET'])
def record_view(mlb_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblMLB WHERE id=%s', mlb_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', mlb=result[0])


@app.route('/edit/<int:mlb_id>', methods=['GET'])
def form_edit_get(mlb_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblMLB WHERE id=%s', mlb_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', mlb=result[0])


@app.route('/edit/<int:mlb_id>', methods=['POST'])
def form_update_post(mlb_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('fldName'), request.form.get('fldTeam'), request.form.get('fldPosition'),
                 request.form.get('fldHeight_inches'), request.form.get('fldWeight_lbs'),
                 request.form.get('fldAge'), mlb_id)
    sql_update_query = """UPDATE tblMLB t SET t.fldName = %s, t.fldTeam = %s, t.fldPosition = %s, t.fldHeight_inches = 
    %s, t.fldWeight_lbs = %s, t.fldAge = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/mlb/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New MLB Form')


@app.route('/mlb/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('fldName'), request.form.get('fldTeam'), request.form.get('fldPosition'),
                 request.form.get('fldHeight_inches'), request.form.get('fldWeight_lbs'),
                 request.form.get('fldAge'))
    sql_insert_query = """INSERT INTO tblMLB (fldName,fldTeam,fldPosition,fldHeight_inches,fldWeight_lbs,fldAge) VALUES (%s, %s,%s, %s,%s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/delete/<int:mlb_id>', methods=['POST'])
def form_delete_post(mlb_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM tblMLB WHERE id = %s """
    cursor.execute(sql_delete_query, mlb_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/mlb', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblMLB')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/mlb/<int:mlb_id>', methods=['GET'])
def api_retrieve(mlb_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblMLB WHERE id=%s', mlb_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/mlb/<int:mlb_id>', methods=['PUT'])
def api_edit(mlb_id) -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (content['fldName'], content['fldTeam'], content['fldPosition'],
                 content['fldHeight_inches'], content['fldWeight_lbs'],
                 content['fldAge'],mlb_id)
    sql_update_query = """UPDATE tblMLB t SET t.fldName = %s, t.fldTeam = %s, t.fldPosition = %s, t.fldHeight_inches = 
        %s, t.fldWeight_lbs = %s, t.fldAge = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp

@app.route('/api/v1/mlb', methods=['POST'])
def api_add() -> str:

    content = request.json

    cursor = mysql.get_db().cursor()
    inputData = (content['fldName'], content['fldTeam'], content['fldPosition'],
                 content['fldHeight_inches'], content['fldWeight_lbs'],
                 content['fldAge'])
    sql_insert_query = """INSERT INTO tblMLB (fldName,fldTeam,fldPosition,fldHeight_inches,fldWeight_lbs,fldAge) VALUES (%s, %s,%s, %s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp

@app.route('/api/v1/mlb/<int:mlb_id>', methods=['DELETE'])
def api_delete(mlb_id) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM tblMLB WHERE id = %s """
    cursor.execute(sql_delete_query, mlb_id)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)