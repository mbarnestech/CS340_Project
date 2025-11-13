"""
Citation: This file was generated based on user interaction with Microsoft Copilot on November 5, 2025. It has been lightly edited for clarity and to finish meeting assignment requirements.

Prompt 1: Can you create a website, front end and backend, to display each table in DDL.sql and do CRUD operations on them? The setup for the webpage and mysql database access should be the same as in app.py. Each table should be a separate page, and there should be a home page. The code should be in Python using Flask and Jinja.

Prompt 2: Generate a single-file version

Prompt 3: hi! with the file you gave me, could you update  @app.route('/<table>' to include an option for selecting a single row of data (using a select statement) and a way to update a single row based on any field in the table?

Prompt 4: add dropdowns for field selection and allow selection from any field in the table.

Prompt 5: please remove the drop down and value field from the Actions column, but keep the Select button. If a user clicks Select, that row should be selected and shown just as if the user had used the Select Record section to select a record.

Prompt 6: oh it was better before. go back to the previous version and just remove the dropdown, value field, and select button from the actions column

Prompt 7: Select Record is still showing up wrong.  please update the Select Record section to how it was after I requested 'add dropdowns for field selection and allow selection from any field in the table.'

Prompt 8: please provide me with a .txt file containing all prompts i have given here and a citation.
"""

from flask import Flask, render_template, render_template_string, json, redirect
from flask_mysqldb import MySQL
from flask import request
from env import *

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'USERNAME'
app.config['MYSQL_PASSWORD'] = 'PASSWORD'
app.config['MYSQL_DB'] = 'DATABASENAME'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"


mysql = MySQL(app)


# Home page
@app.route('/')
def home():
    return render_template_string('''
        <h1>Welcome to the Neighborhood Lending Library</h1>
        <ul>
            <li><a href="/Users">Users</a></li>
            <li><a href="/Resources">Resources</a></li>
            <li><a href="/Loans">Loans</a></li>
            <li><a href="/Locations">Locations</a></li>
            <li><a href="/ResourceLocations">ResourceLocations</a></li>
        </ul>
    ''')



# Generic CRUD page generator with select and update
@app.route('/<table>', methods=['GET', 'POST'])
def table_view(table):
    cur = mysql.connection.cursor()
    message = ""
    selected_row = None

    if table == "Users":
            message = "This is the Users page. On this page you can create, read, edit, and delete records in the Users table."
    elif table == "Resources":
            message = "This is the Resources page. On this page you can create, read, edit, and delete records in the Resources table."
    elif table == "Loans":
            message = "This is the Loans page. On this page you can create, read, edit, and delete records in the Loans table."
    elif table == "Locations":
        message = "This is the Locations page. On this page you can create, read, edit, and delete records in the Locations table."
    elif table == "ResourceLocations":
        message = "This is the ResourceLocations page. On this page you can create, read, edit, and delete records in the ResourceLocations table."

    cur.execute(f"SELECT * FROM {table}")
    rows = cur.fetchall()
    columns = rows[0].keys() if rows else []

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'delete':
            pk = request.form.get('pk')
            cur.execute(f"DELETE FROM {table} WHERE {pk.split('=')[0]} = %s", (pk.split('=')[1],))
            mysql.connection.commit()
            message = "Row deleted successfully."

        elif action == 'insert':
            columns = request.form.getlist('column')
            values = request.form.getlist('value')
            col_str = ', '.join(columns)
            val_str = ', '.join(['%s'] * len(values))
            cur.execute(f"INSERT INTO {table} ({col_str}) VALUES ({val_str})", tuple(values))
            mysql.connection.commit()
            message = "Row inserted successfully."

        elif action == 'select':
            field = request.form.get('field')
            value = request.form.get('value')
            cur.execute(f"SELECT * FROM {table} WHERE {field} = %s", (value,))
            selected_row = cur.fetchone()
            message = "Row selected."

        elif action == 'update':
            pk = request.form.get('pk')
            columns = request.form.getlist('column')
            values = request.form.getlist('value')
            set_clause = ', '.join([f"{col} = %s" for col in columns])
            cur.execute(f"UPDATE {table} SET {set_clause} WHERE {pk.split('=')[0]} = %s", tuple(values + [pk.split('=')[1]]))
            mysql.connection.commit()
            message = "Row updated successfully."

        cur.execute(f"SELECT * FROM {table}")
        rows = cur.fetchall()

    return render_template_string('''
        <h1>{{ table }} Table</h1>
        <a href="/">Home</a>
        <p>{{ message }}</p>
        <table border="1">
            <tr>{% for col in columns %}<th>{{ col }}</th>{% endfor %}<th>Actions</th></tr>
            {% for row in rows %}
            <tr>
                {% for col in columns %}<td>{{ row[col] }}</td>{% endfor %}
                <td>
                    <form method="post">
                        <input type="hidden" name="action" value="delete">
                        <input type="hidden" name="pk" value="{{ columns[0] }}={{ row[columns[0]] }}">
                        <input type="submit" value="Delete">
                    </form>
                </td>
            </tr>
            {% endfor %}
        </table>

        <h2>Add New Record</h2>
        <form method="post">
            <input type="hidden" name="action" value="insert">
            {% for col in columns %}
                <label>{{ col }}: <input name="value" required></label>
                <input type="hidden" name="column" value="{{ col }}"><br>
            {% endfor %}
            <input type="submit" value="Add">
        </form>

        <h2>Select Record</h2>
        <form method="post">
            <input type="hidden" name="action" value="select">
            <label>Field:
                <select name="field">
                    {% for col in columns %}<option value="{{ col }}">{{ col }}</option>{% endfor %}
                </select>
            </label>
            <label>Value: <input name="value" required></label>
            <input type="submit" value="Select">
        </form>

        {% if selected_row %}
        <h2>Selected Record (required prior to Updating Record)</h2>
        <table border="1">
            <tr>{% for col in columns %}<th>{{ col }}</th>{% endfor %}</tr>
            <tr>{% for col in columns %}<td>{{ selected_row[col] }}</td>{% endfor %}</tr>
        </table>

        <h2>Update Selected Record</h2>
        <form method="post">
            <input type="hidden" name="action" value="update">
            <input type="hidden" name="pk" value="{{ columns[0] }}={{ selected_row[columns[0]] }}">
            {% for col in columns %}
                <label>{{ col }}: <input name="value" value="{{ selected_row[col] }}" required></label>
                <input type="hidden" name="column" value="{{ col }}"><br>
            {% endfor %}
            <input type="submit" value="Update">
        </form>
        {% endif %}
    ''', table=table, rows=rows, columns=columns, message=message, selected_row=selected_row)



# Listener
if __name__ == "__main__":

    #Start the app to run on a port of your choosing
    app.run(port=5284, debug=True)
