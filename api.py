import flask
from flask import request, jsonify
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def index():
    return render_template('/index.html')


@app.route('/add-asset', methods=['POST'])
def add_asset():
    conn = sqlite3.connect('asset.db')
    if request.method == 'POST':
      result = request.form
      id1=result['id']
      asset=result['asset']
      conn.execute("INSERT INTO assets (ID,ASSET) VALUES (' " + str(id1) +"', '"+ str(asset)+ "')");
      conn.commit()
      print ("Records created successfully")
      conn.close()
      return redirect(url_for('index'))

@app.route('/add-task', methods=['POST'])
def add_task():
    conn =sqlite3.connect('task1.db')
    if request.method == 'POST':
      result = request.form
      id1=result['id']
      task=result['task']
      disp=result['disp']
      conn.execute("INSERT INTO task (ID,TASK,DISP) VALUES (' " + str(id1) +"', '"+ str(task)+ "', '"+ str(disp)+ "')");
      conn.commit()
      print ("Records created successfully")
      conn.close()
      return redirect(url_for('index'))

@app.route('/add-worker', methods=['POST'])
def add_worker():
    conn =sqlite3.connect('worker1.db')
    if request.method == 'POST':
      result = request.form
      id1=result['id']
      worker=result['worker']
      conn.execute("INSERT INTO worker (ID,WORKER) VALUES (' " + str(id1) +"', '"+ str(worker)+ "')");
      conn.commit()
      print ("Records created successfully")
      conn.close()
      return redirect(url_for('index'))

@app.route('/allocate-task', methods=['POST'])
def api_task():
    conn =sqlite3.connect('taskset1.db')
    if request.method == 'POST':
      result = request.form
      id1=result['asset']
      id2=result['task']
      id3=result['worker']
      time=result['time']
      dtime=result['dtime']
      conn.execute("INSERT INTO taskset (IDA,IDT,IDW,TS,TD) VALUES (' " + str(id1) +"', '"+ str(id2)+"', '"+ str(id3)+"', '"+ str(time)+"', '"+ str(dtime)+ "')");
      conn.commit()
      print ("Records created successfully")
      conn.close()
      return redirect(url_for('index'))



@app.route('/get-task-for-worker', methods=['GET'])
def api_taskW():
    conn =sqlite3.connect('taskset1.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    query_parameters = request.args
    id1 = query_parameters.get('worker')
    all_assets = cur.execute('SELECT * FROM taskset WHERE IDW = '+id1+' ;').fetchall()

    return jsonify(all_assets)


@app.route('/assets/all', methods=['GET'])
def api_asset():
    conn =sqlite3.connect('asset.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_assets = cur.execute('SELECT * FROM assets;').fetchall()

    return jsonify(all_assets)




@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404




app.run()