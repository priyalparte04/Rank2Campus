from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)


# =========================
# MySQL Connection
# =========================
def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="priyal@1204",
        database="rank2campus"
    )
    return connection


# =========================
# Home
# =========================
@app.route("/")
def home():
    return render_template("home.html")


# =========================
# About
# =========================
@app.route("/about")
def about():
    return render_template("about.html")


# =========================
# Register
# =========================
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        try:

            connection = get_db_connection()
            cursor = connection.cursor()

            query = """
                INSERT INTO users (name, email, password)
                VALUES (%s, %s, %s)
            """

            cursor.execute(query, (name, email, password))

            connection.commit()

            cursor.close()
            connection.close()

            # After registration go to login page
            return redirect(url_for("login"))

        except mysql.connector.Error as e:

            return f"Registration Error: {e}"

    return render_template("register.html")


# =========================
# Login
# =========================
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        try:

            connection = get_db_connection()
            cursor = connection.cursor()

            query = """
                SELECT * FROM users
                WHERE email = %s AND password = %s
            """

            cursor.execute(query, (email, password))

            user = cursor.fetchone()

            cursor.close()
            connection.close()

            if user:

                # After login go to dashboard
                return redirect(url_for("dashboard"))

            else:

                return "Invalid email or password."

        except mysql.connector.Error as e:

            return f"Login Error: {e}"

    return render_template("login.html")


# =========================
# Dashboard
# =========================
@app.route("/dashboard")
def dashboard():

    return render_template("dashboard.html")


# =========================
# CET
# =========================
@app.route("/cet", methods=["GET", "POST"])
def cet():

    if request.method == "POST":

        name = request.form["name"]
        percentile = float(request.form["percentile"])
        category = request.form["category"]
        city = request.form["city"]

        try:

            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)

            query = """
                SELECT
                    colleges.college_name,
                    colleges.city,
                    colleges.state,
                    colleges.description,
                    branches.branch_name,
                    cutoffs.cutoff_value,
                    cutoffs.admission_year
                FROM cutoffs

                JOIN colleges
                    ON cutoffs.college_id = colleges.college_id

                JOIN branches
                    ON cutoffs.branch_id = branches.branch_id

                WHERE cutoffs.exam_id = 1
                AND cutoffs.category = %s
                AND cutoffs.cutoff_value <= %s
                AND cutoffs.admission_year = 2026
                AND (
    %s = 'Any'
    OR colleges.city = %s
    OR (
        %s = 'PCMC'
        AND (
            colleges.city = 'Pimpri-Chinchwad'
            OR colleges.city = 'Ravet, Pimpri-Chinchwad'
            OR colleges.city = 'Akurdi, Pimpri-Chinchwad'
            OR colleges.city = 'Talegaon'
        )
    )
)

                ORDER BY cutoffs.cutoff_value DESC
            """

            cursor.execute(
                query,
                (category, percentile, city, city, city)
            )

            colleges = cursor.fetchall()

            cursor.close()
            connection.close()

            return render_template(
                "recommendations.html",
                name=name,
                percentile=percentile,
                category=category,
                city=city,
                colleges=colleges,
                exam="CET"
            )

        except mysql.connector.Error as e:

            return f"Recommendation Error: {e}"

    return render_template("cet.html")

# =========================
# JEE
# =========================
@app.route("/jee", methods=["GET", "POST"])
def jee():

    if request.method == "POST":

        name = request.form["name"]
        percentile = float(request.form["percentile"])
        category = request.form["category"]
        city = request.form["city"]

        print("JEE:", name, percentile, category, city)

        try:

            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)

            query = """
                SELECT
                    colleges.college_name,
                    colleges.city,
                    colleges.state,
                    colleges.description,
                    branches.branch_name,
                    cutoffs.cutoff_value,
                    cutoffs.admission_year
                FROM cutoffs

                JOIN colleges
                    ON cutoffs.college_id = colleges.college_id

                JOIN branches
                    ON cutoffs.branch_id = branches.branch_id

                WHERE cutoffs.exam_id = 2
                AND cutoffs.category = %s
                AND cutoffs.cutoff_value <= %s
                AND cutoffs.admission_year = 2026

                AND (
                    %s = 'Any'
                    OR colleges.city = %s
                    OR (
                        %s = 'PCMC'
                        AND (
                            colleges.city = 'Pimpri-Chinchwad'
                            OR colleges.city = 'Ravet, Pimpri-Chinchwad'
                            OR colleges.city = 'Akurdi, Pimpri-Chinchwad'
                            OR colleges.city = 'Talegaon'
                        )
                    )
                )

                ORDER BY cutoffs.cutoff_value DESC
            """

            cursor.execute(
                query,
                (category, percentile, city, city, city)
            )

            colleges = cursor.fetchall()

            cursor.close()
            connection.close()

            return render_template(
                "recommendations.html",
                name=name,
                percentile=percentile,
                category=category,
                city=city,
                colleges=colleges,
                exam="JEE"
            )

        except mysql.connector.Error as e:

            return f"JEE Recommendation Error: {e}"

    return render_template("jee.html")

# =========================
# Test Database
# =========================
@app.route("/test-db")
def test_database():

    try:

        connection = get_db_connection()

        cursor = connection.cursor()

        cursor.execute("SELECT DATABASE()")

        database_name = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        return f"Database Connected Successfully: {database_name}"

    except Exception as e:

        return f"Database Connection Error: {e}"


# =========================
# Run Application
# =========================
if __name__ == "__main__":

    app.run(debug=True)