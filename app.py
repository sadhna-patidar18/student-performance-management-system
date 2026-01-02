from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__, static_folder="static", template_folder="templates")

# ---------------- DATABASE CONNECTION ----------------
def get_db_connection():
    conn = sqlite3.connect("students.db")
    conn.row_factory = sqlite3.Row
    return conn

# ---------------- HOME PAGE ----------------
@app.route("/")
def home():
    return render_template("stud_add.html")

# ---------------- ADD STUDENT ----------------
@app.route("/add", methods=["POST"])
def add_student():
    name = request.form["name"]
    roll = request.form["roll"]

    maths = int(request.form["maths"])
    physics = int(request.form["physics"])
    chemistry = int(request.form["chemistry"])
    english = int(request.form["english"])
    computer = int(request.form["computer"])

    # Validation
    marks = [maths, physics, chemistry, english, computer]
    for m in marks:
        if m < 0 or m > 100:
            return "Error: Marks must be between 0 and 100"

    total = sum(marks)
    percentage = (total / 500) * 100
    result = "PASS" if percentage >= 40 else "FAIL"

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO students
        (name, roll, maths, physics, chemistry, english, computer, total, percentage, result)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name, roll, maths, physics, chemistry, english, computer,
        total, percentage, result
    ))
    conn.commit()
    conn.close()

    # Redirect to dashboard
    return redirect(url_for("dashboard"))

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT roll, name, total, percentage, result
        FROM students
    """)
    students = cursor.fetchall()
    conn.close()

    return render_template("dashboard.html", students=students)

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)
