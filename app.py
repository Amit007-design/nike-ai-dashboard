
from flask import Flask, request, redirect, session, render_template_string
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = "nike_secret_key"

USERNAME = "admin"
PASSWORD = "nike123"

login_page = '''
<h2>Nike AI Dashboard Login</h2>
<form method="POST">
Username: <input name="username"><br><br>
Password: <input name="password" type="password"><br><br>
<button type="submit">Login</button>
</form>
'''

dashboard_page = '''
<h1>Nike AI Sales Dashboard</h1>
<p>Total Revenue: {{revenue}}</p>
<p>Total Orders: {{orders}}</p>
<a href="/logout">Logout</a>
'''

@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == USERNAME and request.form["password"] == PASSWORD:
            session["user"] = USERNAME
            return redirect("/dashboard")
    return login_page

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    data = pd.read_csv("nike_sales_dataset.csv")
    return render_template_string(dashboard_page,
                                  revenue=round(data['Revenue'].sum(),2),
                                  orders=len(data))

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
