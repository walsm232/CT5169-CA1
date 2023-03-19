<h1> <div align="center"> CT5169 Fundamentals of Cloud Computing  </div> </h1>

<div align="center"> <img src="static/home.png"> </div>

## Project Description
The goal of this assignment was to create a distributed cloud computing application. The main aspects are:
- A host machine which runs a Flask webserver. The website should provide a search bar which allows the user to search for Wikipedia results.
- Virtualization software is used (_Parallels Desktop Pro_) on the host machine to run a virtual machine (VM) running Ubuntu OS.
- The VM runs a MySQL database as a Docker container and exposes it on port 6603.
- The VM has a Python script, named _wiki.py_, which takes a query as an argument. It uses this query to search and parse Wikipedia pages for information relating to it. This is able to be executed from the host machine through SSH using Paramiko.
- The result is returned to the host machine and rendered neatly as HTML.
- If it is the first time a given query is run then the result to the MySQL database. If the same query is run at any other point it will pull the result from the database instead of following the full process of searching and parsing Wikipedia, which improves overall performance.




## Built With
- Flask
- Python
- Docker
- MySQL
- HTML
- CSS
- jQuery
- FontAwesome
