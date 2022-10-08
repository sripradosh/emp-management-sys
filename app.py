from flask import Flask, render_template, request, url_for, session, redirect, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "register"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)


@app.route("/", methods=['GET', 'POST'])
def index():
    if 'alogin' in request.form:
        if request.method == 'POST':
            aname = request.form["aname"]
            apass = request.form["apass"]
            try:
                cur = mysql.connection.cursor()
                cur.execute("select * from admin where aname = %s and apass = %s", [aname, apass])
                res = cur.fetchone()
                if res:
                    session["aname"] = res["aname"]
                    session["aid"] = res["aid"]
                    return redirect(url_for('admin_home'))
                else:
                    return render_template("index.html")
            except Exception as e:
                print(e)
            finally:
                mysql.connection.commit()
                cur.close()
    elif 'registration' in request.form:
        if request.method == 'POST':
            name = request.form["name"]
            password = request.form["password"]
            number = request.form["number"]
            email = request.form["email"]
            address = request.form["address"]
            department = request.form["department"]
            cur = mysql.connection.cursor()
            cur.execute('insert into users (name,password,number,email,address,department) values (%s,%s,%s,%s,%s,%s)',
                        [name, password, number, email, address, department])
            mysql.connection.commit()
        return render_template("index.html")

    elif 'ulogin' in request.form:
        if request.method == 'POST':
            name = request.form["uname"]
            password = request.form["upassword"]
            try:
                cur = mysql.connection.cursor()
                cur.execute("select * from users where name = %s and password = %s", [name, password])
                res = cur.fetchone()
                if res:
                    session["name"] = res["name"]
                    session["eid"] = res["eid"]
                    return redirect(url_for('user_home'))
                else:
                    return render_template("index.html")
            except Exception as e:
                print(e)
            finally:
                mysql.connection.commit()
                cur.close()
    return render_template("index.html")

@app.route("/user_profile")
def user_profile():
    cur = mysql.connection.cursor()
    id = session["eid"]
    qry = "select * from users where eid=%s"
    cur.execute(qry, [id])
    data = cur.fetchone()
    cur.close()
    count = cur.rowcount
    if count == 0:
        flash("Users Not Found...!!!!", "danger")
    else:
        return render_template("user_profile.html", res=data)


@app.route("/update_user", methods=['GET', 'POST'])
def update_user():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        number = request.form['number']
        email = request.form['email']
        address = request.form['address']
        department = request.form['department']
        eid = session['eid']
        cur = mysql.connection.cursor()
        cur.execute("update users set name=%s,password=%s,number=%s,email=%s,address=%s,department=%s where eid=%s",
                    [name, password, number, email, address, department, eid])
        mysql.connection.commit()
        flash('User Update Successfully', 'success')
        return redirect(url_for('user_profile'))
    return render_template("user_profile.html")

@app.route("/view_users")
def view_users():
    cur = mysql.connection.cursor()
    qry = "select * from users"
    cur.execute(qry)
    data = cur.fetchall()
    cur.close()
    count = cur.rowcount
    if count == 0:
        flash("Users Not Found...!!!!", "danger")
    return render_template("view_users.html", res=data)

@app.route("/delete_users/<string:id>", methods=['GET', 'POST'])
def delete_users(id):
    cur = mysql.connection.cursor()
    cur.execute("delete from users where eid=%s", [id])
    mysql.connection.commit()
    flash("Users Deleted Successfully", "danger")
    return redirect(url_for("view_users"))


@app.route("/admin_home")
def admin_home():
    return render_template("admin_home.html")


@app.route("/user_home")
def user_home():
    return render_template("user_home.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.secret_key = '123'
    app.run(debug=True)