from flask import Flask, render_template, url_for, request, redirect, json
from flaskext.mysql import MySQL

from models import HelloWorld

app = Flask(__name__)
mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'MysqlX321'
app.config['MYSQL_DATABASE_DB'] = 'flask-learn'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

def openDb():
    global conn, cursor
    conn = mysql.connect()
    cursor = conn.cursor()

# For closing the Database
def closeDb():
    global conn, cursor
    cursor.close()
    conn.close()


# Basic Routing
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nama = request.form['nama']
        email = request.form['email']
        return render_template('display.html', namas=nama, emails=email)
    return render_template('home.html')


@app.route('/about')
def about():
    model = HelloWorld()
    return render_template('about.html', model=model)


@app.route('/contact')
def contact():
    model = HelloWorld()
    return render_template('contact.html', model=model)


# CRUD Methods
@app.route('/view')
def view():
    openDb()
    container = []
    sql = "SELECT * FROM barang"
    cursor.execute(sql)
    results = cursor.fetchall()
    for data in results:
        container.append(data)
    closeDb()
    return render_template('view.html', container=container)


@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        nama = request.form['nama']
        harga = request.form['harga']
        stok = request.form['stok']
        openDb()
        sql = "INSERT INTO barang (nama_barang, harga,stok) VALUES (%s, %s, %s)"
        val = (nama, harga, stok)
        cursor.execute(sql, val)
        conn.commit()
        closeDb()
        return redirect(url_for('view'))
    else:
        return render_template('insert.html')


@app.route('/edit/<id_barang>', methods=['GET', 'POST'])
def edit(id_barang):
    openDb()
    cursor.execute('SELECT * FROM barang WHERE id_barang=%s', (id_barang))
    data = cursor.fetchone()
    if request.method == 'POST':
        id_barang = request.form['id_barang']
        nama = request.form['nama']
        harga = request.form['harga']
        stok = request.form['stok']
        sql = "UPDATE barang SET nama_barang=%s, harga=%s, stok=%s WHERE id_barang=%s"
        val = (nama, harga, stok, id_barang)
        cursor.execute(sql, val)
        conn.commit()
        closeDb()
        return redirect(url_for('view'))
    else:
        closeDb()
        return render_template('edit.html', data=data)


@app.route('/delete/<id_barang>', methods=['GET', 'POST'])
def delete(id_barang):
    openDb()
    cursor.execute('DELETE FROM barang WHERE id_barang=%s', (id_barang,))
    conn.commit()
    closeDb()
    return redirect(url_for('view'))
    

if __name__ == '__main__':
    app.run(debug=True)