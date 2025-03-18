from flask import Flask, render_template
import psycopg2

app = Flask(__name__)

# Database connection details
db_config = {
    'dbname': 'your_dbname',
    'user': 'your_username',
    'password': 'your_password',
    'host': 'your_rds_endpoint',
    'port': '5432'
}

@app.route('/')
def index():
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()
    cur.execute("SELECT * FROM your_table")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
