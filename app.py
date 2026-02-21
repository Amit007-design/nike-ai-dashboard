from flask import Flask, request, redirect, session, render_template_string, url_for
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = "nike_secret_key"

USERNAME = "admin"
PASSWORD = "nike123"

def load_data():
    return pd.read_csv("nike_sales_dataset.csv")

LOGIN_HTML = """
<!doctype html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Nike GOD MODE Dashboard • Login</title>
<style>
body{margin:0;font-family:Arial,sans-serif;background:radial-gradient(circle at 20% 20%,#1f2937,#020617 60%);color:#e5e7eb;display:flex;align-items:center;justify-content:center;min-height:100vh}
.card{width:min(440px,92vw);background:rgba(15,23,42,.9);backdrop-filter:blur(8px);border:1px solid #334155;border-radius:20px;padding:28px;box-shadow:0 20px 60px rgba(0,0,0,.45)}
h1{margin:0 0 6px;font-size:26px} p{margin:0 0 16px;color:#94a3b8}
label{display:block;margin:10px 0 6px;font-size:13px;color:#cbd5e1}
input{width:100%;padding:12px;border-radius:10px;border:1px solid #334155;background:#020617;color:#fff}
button{margin-top:14px;width:100%;padding:12px;border:none;border-radius:10px;background:linear-gradient(90deg,#22c55e,#16a34a);color:#052e16;font-weight:800}
.err{background:#7f1d1d;border:1px solid #ef4444;padding:8px;border-radius:8px;margin-bottom:10px}
.small{font-size:12px;color:#94a3b8;margin-top:10px}
</style>
</head>
<body>
<div class="card">
<h1>👟 Nike GOD MODE</h1>
<p>Executive AI Dashboard Login</p>
{% if error %}<div class="err">{{error}}</div>{% endif %}
<form method="POST">
<label>Username</label><input name="username" required>
<label>Password</label><input type="password" name="password" required>
<button type="submit">Enter Dashboard</button>
</form>
<div class="small">Demo: admin / nike123</div>
</div>
</body>
</html>
"""

DASH_HTML = """
<!doctype html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Nike GOD MODE Corporate Dashboard</title>
<style>
:root{--bg:#020617;--panel:#0f172a;--line:#1f2937;--text:#e5e7eb;--muted:#94a3b8;--green:#22c55e}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font-family:Arial,sans-serif}
.top{display:flex;justify-content:space-between;align-items:center;padding:14px 18px;background:#030712;border-bottom:1px solid var(--line);position:sticky;top:0;z-index:5}
.brand{font-weight:800}
.logout{color:#fecaca;text-decoration:none;border:1px solid #7f1d1d;padding:7px 10px;border-radius:9px}
.wrap{max-width:1250px;margin:16px auto;padding:0 12px}
.hero{background:linear-gradient(120deg,#0f172a,#111827);border:1px solid var(--line);border-radius:16px;padding:16px;margin-bottom:12px}
.hero h2{margin:0 0 6px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:14px}
.label{font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.6px}
.kpi{font-size:28px;font-weight:800;margin-top:6px}
.row{display:grid;grid-template-columns:1.2fr .8fr;gap:12px;margin-top:12px}
@media(max-width:900px){.row{grid-template-columns:1fr}}
.table{width:100%;border-collapse:collapse;font-size:14px}
.table th,.table td{padding:9px;border-bottom:1px solid var(--line);text-align:left}
.bar{height:10px;background:#0b1220;border:1px solid var(--line);border-radius:999px;overflow:hidden}
.fill{height:100%;background:linear-gradient(90deg,#22c55e,#16a34a)}
.badge{display:inline-block;padding:4px 8px;border-radius:999px;background:#052e16;color:#86efac;font-size:12px}
.footer{text-align:center;color:#64748b;font-size:12px;margin:14px 0}
</style>
</head>
<body>
<div class="top">
<div class="brand">👟 Nike GOD MODE • Corporate Analytics</div>
<a class="logout" href="{{ url_for('logout') }}">Logout</a>
</div>
<div class="wrap">
<div class="hero">
<h2>Executive Summary</h2>
<div style="color:#94a3b8">Live KPI overview generated from your sales dataset.</div>
</div>

<div class="grid">
<div class="card"><div class="label">Total Revenue</div><div class="kpi">₹ {{ "{:,.2f}".format(total_revenue) }}</div></div>
<div class="card"><div class="label">Total Orders</div><div class="kpi">{{ total_orders }}</div></div>
<div class="card"><div class="label">Average Order Value</div><div class="kpi">₹ {{ "{:,.2f}".format(avg_order) }}</div></div>
<div class="card"><div class="label">Top Category</div><div class="kpi" style="font-size:20px">{{ top_category }}</div></div>
</div>

<div class="row">
<div class="card">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px"><b>Category Revenue Table</b><span class="badge">Board View</span></div>
<table class="table">
<thead><tr><th>Category</th><th>Orders</th><th>Revenue (₹)</th></tr></thead>
<tbody>
{% for r in category_rows %}
<tr><td>{{r['Product_Category']}}</td><td>{{r['Orders']}}</td><td>{{ "{:,.2f}".format(r['Revenue']) }}</td></tr>
{% endfor %}
</tbody>
</table>
</div>

<div class="card">
<b>Revenue Share</b>
{% for r in category_rows %}
<div style="display:flex;justify-content:space-between;font-size:13px;margin:8px 0 4px"><span>{{r['Product_Category']}}</span><span>{{ "{:.1f}".format(r['Share']) }}%</span></div>
<div class="bar"><div class="fill" style="width: {{r['Share']}}%"></div></div>
{% endfor %}
</div>
</div>

<div class="footer">GOD MODE UI • Flask + Pandas • Render Cloud</div>
</div>
</body>
</html>
"""

@app.route("/", methods=["GET","POST"])
def login():
    if request.method=="POST":
        if request.form.get("username")==USERNAME and request.form.get("password")==PASSWORD:
            session["user"]=USERNAME
            return redirect(url_for("dashboard"))
        return render_template_string(LOGIN_HTML, error="Invalid username or password")
    return render_template_string(LOGIN_HTML, error=None)

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    df = load_data()
    total_revenue=float(df["Revenue"].sum())
    total_orders=int(len(df))
    avg_order=float(df["Revenue"].mean())
    cat=df.groupby("Product_Category").agg(Orders=("Order_ID","count"),Revenue=("Revenue","sum")).reset_index().sort_values("Revenue",ascending=False)
    top_category=cat.iloc[0]["Product_Category"] if len(cat) else "N/A"
    cat["Share"]=cat["Revenue"]/cat["Revenue"].sum()*100 if len(cat) else 0
    rows=cat.to_dict(orient="records")
    return render_template_string(DASH_HTML,total_revenue=total_revenue,total_orders=total_orders,avg_order=avg_order,top_category=top_category,category_rows=rows)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__=="__main__":
    port=int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0",port=port)
