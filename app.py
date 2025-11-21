""" 
The code on this page is an adaptation of the code found on the following CS340 Canvas Pages:
    - Web Application Technology: https://canvas.oregonstate.edu/courses/2017561/pages/exploration-web-application-technology-2?module_item_id=25645131
    - Implementing CUD operations in your app: https://canvas.oregonstate.edu/courses/2017561/pages/exploration-implementing-cud-operations-in-your-app?module_item_id=25645149
"""

# ########################################
# ########## SETUP

from flask import Flask, render_template, request, redirect
from database.db_connector import *
from env import *

# Database credentials
host = 'classmysql.engr.oregonstate.edu'    
user = MYSQL_USER
password = MYSQL_PASSWORD
db = MYSQL_DB

PORT = PORT_NUM

app = Flask(__name__)

# ########################################
# ########## ROUTE HANDLERS

# READ ROUTES
@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            reset()
            return render_template('homeAfterReset.j2') 
        except Exception as e:
            print(f"Error rendering page: {e}")
            return "An error occurred while rendering the page.", 500

    else:
        try:
            return render_template("home.j2")

        except Exception as e:
            print(f"Error rendering page: {e}")
            return "An error occurred while rendering the page.", 500

@app.route("/users", methods=['GET'])
def users():
    
    dbConnection = connectDB(host, user, password, db)  # Open our database connection

    message = "On this page you can view records in the Users table."
    try:
        # Create and execute our query
        query1 = "SELECT * FROM Users;"
        users = query(dbConnection, query1).fetchall()
        headers = ["First Name", "Last Name", "Email", "Phone", "Delete"]

        # Render the users.j2 file, and also send the renderer an object containing the users information
        return render_template(
            "users.j2", headers=headers, users=users, message=message
        )
    
    except Exception as e:
        print(f"Error executing queries: {e}")
        return (
            "An error occurred while executing the database queries.",
            500,
        )
    finally:
        # Close the DB connection, if it exists
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()

@app.route("/loans", methods=['GET'])
def loans():
    
    dbConnection = connectDB(host, user, password, db)  # Open our database connection

    message = "On this page you can view and delete records in the Loans table."
    try:
        # Create and execute our query
        query1 = "SELECT l.loanID, l.startDate, l.dueDate, r.resourceName, u.firstName, u.lastName FROM Loans l JOIN Users u on l.userID = u.userID JOIN Resources r on l.resourceID = r.resourceID;"
     
        loans = query(dbConnection, query1).fetchall()
        print(loans)
        headers = ["Start Date", "Due Date", "Resource Name", "Lender First Name", "Lender Last Name", "Delete"]

        # Render the loans.j2 file, and also send the renderer an object containing the loan's information
        return render_template(
            "loans.j2", headers=headers, loans=loans, message=message
        )
    
    except Exception as e:
        print(f"Error executing queries: {e}")
        return (
            "An error occurred while executing the database queries.",
            500,
        )
    finally:
        # Close the DB connection, if it exists
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()


@app.route("/resources", methods=['GET'])
def resources():
    
    dbConnection = connectDB(host, user, password, db)  # Open our database connection

    message = "On this page you can view and delete records in the Resources table."
    try:
        # Create and execute our query
        query1 = "SELECT r.resourceID, r.resourceName, r.resourceDescription, u.firstName, u.lastName FROM Resources r JOIN Users u on r.userID = u.userID ;"
     
        resources = query(dbConnection, query1).fetchall()
        print(resources)
        headers = ["Resource Name", "Resource Description", "Owner First Name", "Owner Last Name", "Edit", "Delete"]

        userQuery = "SELECT userID, CONCAT(firstName, ' ', lastName) AS name FROM Users;"
        users = query(dbConnection, userQuery).fetchall()

        # Render the resources.j2 file, and also send the renderer an object containing the resource's information
        return render_template(
            "resources.j2", headers=headers, resources=resources, message=message, users=users
        )
    
    except Exception as e:
        print(f"Error executing queries: {e}")
        return (
            "An error occurred while executing the database queries.",
            500,
        )
    finally:
        # Close the DB connection, if it exists
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()

@app.route("/resourceLocations", methods=['GET'])
def resourceLocations():
    
    dbConnection = connectDB(host, user, password, db)  # Open our database connection

    message = "On this page you can view and delete records in the ResourceLocations table."
    try:
        # Create and execute our query
        query1 = "SELECT rl.resourceLocationsID, r.resourceName, l.locationName FROM ResourceLocations rl JOIN Resources r on rl.resourceID = r.resourceID JOIN Locations l on rl.locationID = l.locationID;"
     
        resourceLocations = query(dbConnection, query1).fetchall()
        print(resourceLocations)
        headers = ["Resource Name", "Location Name", "Edit", "Delete"]

        resourceQuery = "SELECT resourceID as id, resourceName AS name FROM Resources;"
        resources = query(dbConnection, resourceQuery).fetchall()

        locationQuery = "SELECT locationID as id, locationName AS name FROM Locations;"
        locations = query(dbConnection, locationQuery).fetchall()

        # Render the resourceLocations.j2 file, and also send the renderer an object containing the resourceLocation's information
        return render_template(
            "resourceLocations.j2", headers=headers, resourceLocations=resourceLocations, message=message, resources = resources, locations = locations
        )
    
    except Exception as e:
        print(f"Error executing queries: {e}")
        return (
            "An error occurred while executing the database queries.",
            500,
        )
    finally:
        # Close the DB connection, if it exists
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()

@app.route("/locations", methods=['GET'])
def locations():
    
    dbConnection = connectDB(host, user, password, db)  # Open our database connection

    message = "On this page you can view and delete records in the Locations table."
    try:
        # Create and execute our query
        query1 = "SELECT * FROM Locations;"
     
        locations = query(dbConnection, query1).fetchall()
        print(locations)
        headers = ["Location Name", "Location Description", "Delete"]

        # Render the locations.j2 file, and also send the renderer an object containing the location's information
        return render_template(
            "locations.j2", headers=headers, locations=locations, message=message
        )
    
    except Exception as e:
        print(f"Error executing queries: {e}")
        return (
            "An error occurred while executing the database queries.",
            500,
        )
    finally:
        # Close the DB connection, if it exists
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()


@app.route("/delete", methods=['POST'])
def delete():
    """
    deletes a row from a specified table by ID
    """

    dbConnection = connectDB(host, user, password, db)  # Open our database connection

    table = request.form["table"]
    id = request.form["id"]
    name = request.form["name"]
    print(table,id,name)

    try:
        cursor = dbConnection.cursor()

        # Create and execute our queries
        # Using parameterized queries (Prevents SQL injection attacks)
        query = f"CALL sp_delete_{table[:-1]}(%s);"
        cursor.execute(query, (id,))

        dbConnection.commit()  # commit the transaction

        print(f"DELETE row from {table} with ID {id}: {name}")

        # Redirect the user to the updated webpage
        return redirect(f"/{table}")

    except Exception as e:
        print(f"Error executing queries: {e}")
        return (
            "An error occurred while executing the database queries.",
            500,
        )

    finally:
        # Close the DB connection, if it exists
        if "dbConnection" in locals() and dbConnection:
            dbConnection.close()


def reset():
    """
    Resets to starter tables / starter info.
    """
    dbConnection = connectDB(host, user, password, db)  # Open our database connection
    cursor = dbConnection.cursor()

    # Create and execute our queries
    # Using parameterized queries (Prevents SQL injection attacks)
    query = "CALL sp_reset();"
    cursor.execute(query,)
    dbConnection.commit()  # commit the transaction
    
    # Close the DB connection, if it exists
    if "dbConnection" in locals() and dbConnection:
        dbConnection.close()

# ########################################
# ########## LISTENER

if __name__ == "__main__":
    app.run(port=PORT, debug=True)
