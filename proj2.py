from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'webItems'

mysql = MySQL(app)
print("Connected to Database\n")

##homepage
@app.route('/', methods = ['GET', 'POST'])
def homepage():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if request.method == 'POST' and 'sortType' in request.form and 'search' in request.form:
        sortType = int(request.form['sortType'])
        search = request.form['search']

        if search != "":
            if(sortType == 0):
                sql = "SELECT * FROM items WHERE name = %s ORDER BY id ASC"
                sqlInput = (search, )
            elif(sortType == 1):
                sql = "SELECT * FROM items WHERE name = %s ORDER BY id DESC"
                sqlInput = (search, )
            elif(sortType == 2):
                sql = "SELECT * FROM items WHERE name = %s ORDER BY name ASC"
                sqlInput = (search, )
            elif(sortType == 3):
                sql = "SELECT * FROM items WHERE name = %s ORDER BY name DESC"
                sqlInput = (search, )
            cursor.execute(sql, sqlInput)
        else:
            if(sortType == 0):
                sql = "SELECT * FROM items ORDER BY id ASC"
            elif(sortType == 1):
                sql = "SELECT * FROM items ORDER BY id DESC"
            elif(sortType == 2):
                sql = "SELECT * FROM items ORDER BY name ASC"
            elif(sortType == 3):
                sql = "SELECT * FROM items ORDER BY name DESC"
            cursor.execute(sql)
        
        
        items = cursor.fetchall()

        if items:
            cursor.close()
            return render_template('homepage.html', items = items)
        
    cursor.close()

    return render_template('homepage.html')

##add
@app.route('/add', methods = ['GET', 'POST'])
def addpage():
    feedback = ""
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if request.method == 'POST' and 'name' in request.form and 'desc' in request.form and 'image' in request.form:
        mooseName = request.form['name']
        mooseDesc = request.form['desc']
        mooseImage = request.form['image']

        if mooseName != "" and mooseDesc != "" and mooseImage != "":
            sql = "INSERT INTO items (name, description, image) VALUES (%s,%s,%s)"
            sqlInput = (mooseName, mooseDesc, mooseImage)
            cursor.execute(sql, sqlInput)
            feedback = "Moose Successfully Added"
        else:
            feedback = "Moose Unsuccessfully Added"

    mysql.connection.commit()
    cursor.close()

    return render_template('addpage.html')

##delete
@app.route('/delete', methods = ['GET', 'POST'])
def deletepage():
    feedback = ""
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if request.method == 'POST' and 'id' in request.form:
        mooseId = request.form['id']

        if mooseId != "":
            sql = "DELETE FROM items WHERE id = %s"
            sqlInput = (mooseId, )
            cursor.execute(sql, sqlInput)
            feedback = "Moose Successfully Deleted"
        else:
            feedback = "Moose Unsuccessfully Deleted"

    mysql.connection.commit()##commits to database any modifications to website
    cursor.close()

    return render_template('deletepage.html')

##edit
@app.route('/edit', methods = ['GET', 'POST'])
def editpage():
    feedback = ""
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if request.method == 'POST' and 'id' in request.form and 'name' in request.form and 'desc' in request.form and 'image' in request.form:
        mooseId = request.form['id']
        mooseName = request.form['name']
        mooseDesc = request.form['desc']
        mooseImage = request.form['image']

        if mooseId != "" and mooseName != "" and mooseDesc != "" and mooseImage != "":
            sql = "UPDATE items SET name = %s, description = %s, image = %s WHERE id = %s"
            sqlInput = (mooseName, mooseDesc, mooseImage, mooseId)
            cursor.execute(sql, sqlInput)
            feedback = "Moose Successfully Edited"
        else:
            feedback = "Moose Unsuccessfully Deleted"

    mysql.connection.commit()##commits to database any modifications to website
    cursor.close()

    return render_template('editpage.html')

if __name__ == '__main__':
    app.run()