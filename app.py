from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import pymysql
import os

app = Flask(__name__)

# Configure MySQL
app.config["MYSQL_HOST"] = os.environ.get("DB_HOST")
app.config["MYSQL_USER"] = os.environ.get("DB_USER")
app.config["MYSQL_PASSWORD"] = os.environ.get("DB_PASSWORD")
app.config["MYSQL_DB"] = os.environ.get("DB_NAME")

mysql = MySQL(app)


@app.route("/")
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()
    cur.close()
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add_task():
    task_name = request.form["task_name"]
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO tasks (task_name) VALUES (%s)", [task_name])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for("index"))


@app.route("/update/<int:task_id>", methods=["GET", "POST"])
def update_task(task_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tasks WHERE id = %s", [task_id])
    task = cur.fetchone()

    if request.method == "POST":
        task_name = request.form["task_name"]
        cur.execute(
            "UPDATE tasks SET task_name = %s WHERE id = %s", [task_name, task_id]
        )
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("index"))

    cur.close()
    return render_template("update_task.html", task=task)


@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tasks WHERE id = %s", [task_id])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for("index"))
