import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DB = "students.db"


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            email TEXT NOT NULL)""")


@app.route("/", methods=["GET", "POST"])
def index():
    errors = []
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        department = request.form.get("department", "").strip()
        email = request.form.get("email", "").strip()
        if not name:
            errors.append("Name is required.")
        if not department:
            errors.append("Department is required.")
        if "@" not in email or "." not in email:
            errors.append("Enter a valid email.")
        if not errors:
            with get_db() as conn:
                conn.execute("INSERT INTO students (name, department, email) VALUES (?, ?, ?)",
                             (name, department, email))
            return redirect(url_for("index"))
    with get_db() as conn:
        students = conn.execute("SELECT * FROM students").fetchall()
    return render_template("index.html", students=students, errors=errors)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
