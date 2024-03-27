from flask import Flask, jsonify, request
from datetime import datetime
from db_init import *


app = Flask(__name__)


@app.route("/bar")
def home():
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    return current_time

@app.route("/todo_list", strict_slashes = False)
def list():
    filterDone = request.args.get("filterDone") == "true"
    try:
        statement = "SELECT taskID, task, finished FROM todo_list" + (" WHERE finished = 'false'" if filterDone else "")
        print(statement)
        getAllTasksQuery = dbCursor.execute(statement)
        toDoRows = getAllTasksQuery.fetchall()
        # to create dictionaries(objects) of tuples:
        rowsOfDictionary = []
        for oneRow in toDoRows:
            my_dict = {} 
            my_dict["taskID"] = oneRow[0]
            my_dict["task"] = oneRow[1]
            my_dict["finished"] = oneRow[2] == 'true'
            rowsOfDictionary.append(my_dict)
        return jsonify(rowsOfDictionary)
    except sql.ProgrammingError as e:
        print(f"You did wrong: {e}")
    except sql.Error as er:
        print(f"Too bad! {er}")

@app.route("/todo_list/<taskID>", methods=["POST"])
def statusChange(taskID):
    newStatusValue = request.get_data(as_text=True)
    print(f"{taskID}, {newStatusValue}")
    dbCursor.execute("UPDATE todo_list SET finished = ? WHERE taskID = ?", (newStatusValue, taskID))
    todo.commit()
    return ("", 204)

@app.route("/todo_task", methods = ["POST"])
def addNewTask():
    newTaskValue = request.get_data(as_text=True)
    dbCursor.execute("INSERT INTO todo_list (task, finished) VALUES (?, 'false')", (newTaskValue,))
    todo.commit()
    return ("", 204)

# @app.route("/remove_row", methods = ["POST"])
@app.route("/delete_task", methods = ["POST"])
def deleteTask():
    valueOfRow = request.get_data(as_text=True)
    dbCursor.execute("DELETE FROM todo_list WHERE task = ?", (valueOfRow,))
    todo.commit()
    return("", 204)

if __name__ == '__main__':
    app.run(threaded=False, processes=1, port=10000, host="0.0.0.0")
    

