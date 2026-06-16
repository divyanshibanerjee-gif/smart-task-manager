from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    send_file,
    redirect,
    session
)

import sqlite3
import csv

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

app = Flask(__name__)

app.secret_key = "my_secret_key"


# ======================
# REGISTER
# ======================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        email = request.form["email"]

        password = generate_password_hash(
            request.form["password"]
        )

        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                INSERT INTO users
                (email, password)
                VALUES (?, ?)
                """,
                (email, password)
            )

            conn.commit()

            return redirect("/login")

        except:

            return "User already exists!"

        finally:

            conn.close()

    return render_template("register.html")
# ======================
# LOGIN
# ======================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, password
            FROM users
            WHERE email = ?
            """,
            (email,)
        )

        user = cursor.fetchone()

        conn.close()

        if user and check_password_hash(
            user[1],
            password
        ):

            session["user_id"] = user[0]

            return redirect("/")

        return "Invalid email or password"

    return render_template(
        "login.html"
    )

# ======================
# LOGOUT
# ======================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


# ======================
# HOME
# ======================

@app.route("/")
def home():

    if "user_id" not in session:

        return redirect("/login")

    return render_template(
        "index.html"
    )


# ======================
# ADD TASK
# ======================

@app.route("/add_task", methods=["POST"])
def add_task():

    print("ADD TASK ROUTE HIT")

    if "user_id" not in session:
        print("NO USER IN SESSION")
        return jsonify({"error": "Login required"}), 401

    data = request.get_json()

    print("DATA:", data)
    print("USER ID:", session["user_id"])

    task = data["task"]
    priority = data["priority"]
    category = data["category"]
    due_date = data["dueDate"]

    user_id = session["user_id"]

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO tasks
        (task, priority, category, due_date, user_id)
        VALUES (?, ?, ?, ?, ?)
        """,
        (task, priority, category, due_date, user_id)
    )

    conn.commit()

    print("TASK INSERTED")

    conn.close()

    return jsonify({"message": "Task added"})
# ======================
# GET TASKS
# ======================

@app.route("/get_tasks")
def get_tasks():

    if "user_id" not in session:
        return jsonify([])

    user_id = session["user_id"]

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            task,
            completed,
            priority,
            category,
            due_date
        FROM tasks
        WHERE user_id = ?
        """,
        (user_id,)
    )

    rows = cursor.fetchall()

    conn.close()

    tasks = []

    for row in rows:

        tasks.append({

            "id": row[0],
            "task": row[1],
            "completed": row[2],
            "priority": row[3],
            "category": row[4],
            "dueDate": row[5]

        })

    return jsonify(tasks)


# ======================
# EDIT TASK
# ======================

@app.route("/edit_task/<int:task_id>", methods=["PUT"])
def edit_task(task_id):

    data = request.get_json()

    new_task = data["task"]

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE tasks
        SET task = ?
        WHERE id = ?
        """,
        (
            new_task,
            task_id
        )
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Task updated"
    })


# ======================
# COMPLETE / UNDO
# ======================

@app.route("/toggle_complete/<int:task_id>", methods=["PUT"])
def toggle_complete(task_id):

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE tasks
        SET completed =
        CASE
            WHEN completed = 0 THEN 1
            ELSE 0
        END
        WHERE id = ?
        """,
        (task_id,)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Task updated"
    })


# ======================
# DELETE TASK
# ======================

@app.route("/delete_task/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM tasks
        WHERE id = ?
        """,
        (task_id,)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Task deleted"
    })


# ======================
# EXPORT CSV
# ======================

@app.route("/export_csv")
def export_csv():

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            task,
            priority,
            category,
            due_date,
            completed
        FROM tasks
        WHERE user_id = ?
        """,
        (user_id,)
    )

    rows = cursor.fetchall()

    conn.close()

    with open(
        "tasks_export.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Task",
            "Priority",
            "Category",
            "Due Date",
            "Completed"
        ])

        writer.writerows(rows)

    return send_file(
        "tasks_export.csv",
        as_attachment=True
    )


# ======================
# RUN APP
# ======================

if __name__ == "__main__":
    app.run(debug=True)

