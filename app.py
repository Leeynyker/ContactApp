from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'Leey'
app.config['MYSQL_PASSWORD'] = 'andres601'
app.config['MYSQL_DB'] = 'flaskcontacts'

mysql = MySQL(app)

# Settings
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    return render_template('index.html', contacts = data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur=mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (fullname,phone,email) VALUES (%s, %s, %s)', (fullname,phone,email))
        mysql.connection.commit()
        
        flash('Se agrego {} correctamente'.format(fullname))
        
        return redirect(url_for('Index'))

@app.route('/update/<string:id>', methods=['POST'])
def update(id):
    print(request.method)
    if request.method == 'POST':
        print('Estoy aqui')
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        
        cur=mysql.connection.cursor()
        cur.execute("""
            UPDATE contacts
            SET fullname = %s,
                phone = %s,
                email = %s
            WHERE id = %s
            """, (fullname, phone, email, id))
        mysql.connection.commit()
        flash('Contacto Actualizado Correctamente ')        
        return redirect(url_for('Index'))


@app.route('/edit/<string:id>')
def get_contact(id):
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = {}'.format(id))
    data = cur.fetchall()
    print(data)
    return render_template('edit-contact.html', contact = data[0])
    

@app.route('/delete/<string:id>')
def delete(id):
    cur=mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {}'.format(id))
    mysql.connection.commit()
    flash('Se ha eliminado un contacto ')        
    return redirect(url_for('Index'))





if __name__ == '__main__':
    app.run(port = 3000, debug = True)