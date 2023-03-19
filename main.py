from flask import Flask, render_template, request, url_for, flash
from werkzeug.utils import redirect
from markupsafe import Markup

import mysql.connector
import paramiko
from mysql.connector import Error


app = Flask(__name__)
app.config['ENV'] = "Development"
app.config['DEBUG'] = True


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/search', methods=['POST'])
def search():
    query = request.form.get("query")

    host = '10.211.55.3'
    port = 22
    username = 'parallels'
    password = 'studentpassword'

    con = paramiko.SSHClient()
    con.load_system_host_keys()
    con.connect(hostname=host, port=port, username=username, password=password)

    stdin, stdout, stderr = con.exec_command('python3 /home/parallels/CA1/wiki.py "' + query + '"')

    outerr = stderr.readlines()
    print("ERRORS: ", outerr)

    output = stdout.readlines()
    print("output:", output)

    query_result = ""
    for item in output:
        query_result = query_result + item

    return render_template("search-result.html", query=query, content=query_result)


# @app.route('/signupaction', methods=['POST'])
# def signupaction():
#     username = request.form.get("username")
#     password = request.form.get("password")
#     bio = request.form.get("bio")
#     print(username, password, bio)
#     try:
#         connection = mysql.connector.connect(host='127.0.0.1',
#                                              port='7703',
#                                              database='MYDB',
#                                              user='root',
#                                              password='mypassword')
#         if connection.is_connected():
#             myquery = "INSERT INTO USER (Username,Password,Bio) VALUES ('" \
#                       + username + "','" + password + "','" + bio + "');"
#             cursor = connection.cursor()
#             result = cursor.execute(myquery)
#             connection.commit()
#     except Error as e:
#         print("Error while connecting to MySQL", e)
#     finally:
#         if connection.is_connected():
#             cursor.close()
#             connection.close()
#     return render_template("home.html")


if __name__ == '__main__':
    app.run(port=8001)
