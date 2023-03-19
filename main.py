from flask import Flask, render_template, request, url_for, flash
from werkzeug.utils import redirect
from markupsafe import Markup

import base64

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
    user_query = request.form.get("query")

    connection = mysql.connector.connect(
        host='127.0.0.1',
        port='7888',
        database='query_db',
        user='root',
        password='mypassword'
    )
    cursor = connection.cursor()

    try:
        sql_query = f"SELECT result FROM query_results WHERE query = '{user_query}';"
        new_result = cursor.execute(sql_query)
        row = cursor.fetchone()
        connection.commit()

        query_result = ""

        # if a result is returned from the MySQL query then set query_result to the result
        if row is not None:
            query_result = row[0]

        # else SSH to the VM and execute the wiki.py script and then write the result to the database
        else:
            host = '10.211.55.3'
            port = 22
            username = 'parallels'
            password = 'studentpassword'

            con = paramiko.SSHClient()
            con.load_system_host_keys()
            con.connect(hostname=host, port=port, username=username, password=password)

            stdin, stdout, stderr = con.exec_command('python3 /home/parallels/CA1/wiki.py "' + user_query + '"')
            outerr = stderr.readlines()
            output = stdout.readlines()

            for item in output:
                query_result = query_result + item

            print(query_result)

            sql_query = "INSERT INTO query_results (query,result) VALUES (%s,%s)"
            args = (user_query, query_result)

            cursor.execute(sql_query, args)
            connection.commit()

    except Exception as e:
        connection.rollback()
        print(f"Exception raised: {e}")

    finally:
        connection.close()

    return render_template("search-result.html", query=user_query, content=query_result)


if __name__ == '__main__':
    app.run(port=8001)
