"""
A program demonstrating how to connect to a SQL Server 2000 database and retrieving some results
from a query.

Author: Kun Deng

"""

import collections # Used for a list structure
import datetime # Used for parsing datetimes
import json # Used for parsing the connection string info
import sys # Used to retrieve the command line arguments

import pyodbc # Used to connect to the SQL Server 2000 database


# Model representing the [JobMessageQueue] table
class JobMessageQueue:

    # The constructor
    def __init__(self, rec_id = "", user_id = "", message = "", occurred = "", cleared = "", job_key = ""):
      self.rec_id = rec_id
      self.user_id = user_id
      self.message = message
      self.occurred = occurred
      self.cleared = cleared
      self.job_key = job_key


    rec_id = 0
    user_id = ""
    message = ""
    occurred = ""
    cleared = ""
    job_key = ""


# Model representing the connection string json file
class ConnectionString:

    # The constructor
    def __init__(self, driver = "", server = "", database = "", username = "", password = ""):
        self.driver = driver
        self.server = server
        self.database = database
        self.username = username
        self.password = password


    # The SQL Native Client driver can communicate with SQL Server 2000
    driver = "SQL Native Client"
    server = ""
    database = ""
    username = ""
    password = ""


# Retrieves queued messages of a given user
def retrieve_queued_messages(conn_string, user):
    messages = collections.defaultdict(JobMessageQueue)

    # Opens a connection to the database 
    conn = pyodbc.connect(conn_string)
    # Creates a cursor object. From this object one can make queries against
    # the database
    curs = conn.cursor()

    i = 0

    # Iterates through each row returned from the query and adds the record
    # to our user-defined dictionary messages
    for row in curs.execute("SELECT * FROM [JobMessageQueue] WHERE UserID = ?", user):
        message = JobMessageQueue(row.Rec_id, row.UserID, row.Message, row.Occurred)
        message.cleared = row.Cleared
        message.job_key = row.JobKey

        messages[i] = message
        i += 1
    
    conn.close()

    return messages


# Parsed the json file as a connection string object
def parse_connection_string(path):
    file = open(path, "r")

    json_obj = json.loads(file.read())

    file.close()

    conn_string = ConnectionString()
    conn_string.driver = json_obj["driver"]
    conn_string.server = json_obj["server"]
    conn_string.database = json_obj["database"]
    conn_string.username = json_obj["username"]
    conn_string.password = json_obj["password"]

    return conn_string


# Returns the connection string object as a string. Conforming to the connection string
# format to connect to the SQL Server 2000 database
def connection_string_obj_to_string(conn_string_obj):
    conn_string = f"Driver={conn_string_obj.driver}; Server={conn_string_obj.server}; "
    conn_string = conn_string + f"Database={conn_string_obj.database}; "
    conn_string = conn_string + f"UiD={conn_string_obj.username}; "
    conn_string = conn_string + f"PwD={conn_string_obj.password};"

    return conn_string


def print_queued_message(message):
    print("\nRec Id: %d" % message.rec_id)
    print("User Id: %s" % message.user_id)
    print("Message: %s" % message.message)
    print("Occurred: %s" % message.occurred)
    print("Cleared: %s" % message.cleared)
    print("Job Key: %s\n" % message.job_key)


def print_queued_messages(messages):
    for message in messages.items():
        print_queued_message(message[1])


def main():
    print("In the main function")

    if len(sys.argv) < 2:
        print("Include path to the connection string file")
        sys.exit(-1)

    connection_str_path = sys.argv[1]

    conn_string_obj = parse_connection_string(connection_str_path)
    conn_string = connection_string_obj_to_string(conn_string_obj)

    print("Connection string is %s" % (conn_string))

    messages = retrieve_queued_messages(conn_string, "kdeng")

    print_queued_messages(messages)



# Checking if the main function has been declared, if so that is where the program starts
if __name__ == "__main__":
    main()
