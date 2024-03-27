import sqlite3 as sql

def db_access():
    try:
        with sql.connect("todo.db") as todo:
            dbCursor = todo.cursor()
            return todo, dbCursor
    except sql.OperationalError as e:
        print(f"error: {e}")

# if __name__ == "__main__":
    # db_access()

todo, dbCursor = db_access()

def create_list():
    dbCursor.execute(
    """
    CREATE TABLE "todo_list" (
        "taskID" INTEGER NOT NULL,
        "task" TEXT,
        "finished" BOOLEAN,
        PRIMARY KEY("taskID" AUTOINCREMENT)
    )
    """
    )
# if __name__ == "__main__":
    # create_list()

def insert_task():
    try:
        task_todo = input("Enter task: ")
        task_finished = input("If finished enter true, if not - false: ")
        dbCursor.execute("INSERT INTO todo_list VALUES(NULL,?,?)",(task_todo,task_finished))
        todo.commit()
        print(f"{task_todo} added")
    except sql.Error as er:
        print(f"this error is {er}")

if __name__ == "__main__":
    insert_task()