from flask import Flask, render_template, request
import mysql.connector
import paramiko


app = Flask(__name__)
app.config['ENV'] = "Development"
app.config['DEBUG'] = True


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/search', methods=['POST'])
def search():
    user_query = request.form.get("query")

    # connect to MySQL server running on the virtual machine
    # port, database, user, and password may need to be updated depending on your situation / configuration
    connection = mysql.connector.connect(
        host='127.0.0.1',
        port='7888',
        database='query_db',
        user='root',
        password='mypassword'
    )
    cursor = connection.cursor()

    query_result = ""

    try:
        # use the user's query to attempt to search for an existing result in the table
        sql_query = f"SELECT result FROM query_results WHERE query = '{user_query}';"
        cursor.execute(sql_query)
        row = cursor.fetchone()
        connection.commit()

        # if a result is returned from the SQL query then set query_result to the result
        if row is not None:
            query_result = row[0]
        else:
            query_result = search_wikipedia(user_query)
            write_result_to_database(user_query, query_result, connection)

    # catch all exceptions, rollback SQL transaction, and print exception
    except Exception as e:
        connection.rollback()
        print(f"Exception raised: {e}")

    # close the SQL connection
    finally:
        connection.close()

    return render_template("search-result.html", query=user_query, content=query_result)


def search_wikipedia(user_query):
    # SSH to the virtual machine
    # hostname, username, and password may need to be updated depending on your situation / configuration
    con = paramiko.SSHClient()
    con.load_system_host_keys()
    con.connect(
        hostname='127.0.0.1',
        port=2233,
        username='parallels',
        password='studentpassword',
        banner_timeout=100,
        auth_timeout=100,
        timeout=100,
    )

    # execute the Python script and pass the user query as an argument
    # must ensure that the wiki.py file exists and the path is correct on the VM
    stdin, stdout, stderr = con.exec_command('python3 /home/parallels/CA1/wiki.py "' + user_query + '"')
    outerr = stderr.readlines()
    output = stdout.readlines()

    query_result = ""
    for item in output:
        query_result = query_result + item

    return query_result


def write_result_to_database(user_query, query_result, connection):
    cursor = connection.cursor()

    # write the query and result to the table for future access (like a cache)
    sql_query = "INSERT INTO query_results (query,result) VALUES (%s,%s)"
    args = (user_query, query_result)
    cursor.execute(sql_query, args)
    connection.commit()


if __name__ == '__main__':
    app.run(port=8001)
