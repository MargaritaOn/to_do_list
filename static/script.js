async function showTime() {
    let response = await fetch("http://localhost:2000/bar");
    let time = await response.text();
    let watch = document.getElementById("clock");
    watch.innerHTML = time;
}
showTime();

async function toDo(filterDone) {
    let response = await fetch("http://localhost:2000/todo_list" + (filterDone === true ? "?filterDone=true" : ""));
    let taskList = await response.json();
    let rowCont = document.getElementById("list");
    while (rowCont.firstChild) {
        rowCont.removeChild(rowCont.lastChild);
    }
    for (let data of taskList) {
        let row = document.createElement("div");
        row.classList.add("taskRow");
        let isDone = document.createElement("input");
        isDone.type = "checkbox";
        if (data.finished) {
            isDone.checked = true;
        }
        isDone.addEventListener("click", click)
        function click(event) {
            // event.preventDefault();
            // isDone.checked = !isDone.checked;
            let statusChangeResponse = fetch(`http://localhost:2000/todo_list/${data.taskID}`, { method: "POST", body: isDone.checked });

        };
        let delBtn = document.createElement("button");
        delBtn.type = "button";
        delBtn.classList.add("mybtn", "delbtn");
        delBtn.textContent = "delete";
        delBtn.addEventListener("click", (e) => {
            fetch(`http://localhost:2000/delete_task`, {method: "POST", body: data.task});
            toDo(!showAll);
        })
        let taskCell = document.createElement("div");
        taskCell.innerHTML = data.task;
        row.append(taskCell);
        let checkDel = document.createElement("div");
        checkDel.append(isDone);
        checkDel.append(delBtn);
        row.append(checkDel);
        rowCont.appendChild(row);
        let sep = document.createElement("div");
        sep.classList.add("separator");
        rowCont.append(sep);
        // row.addEventListener("dblclick", (event) => {
        //     let removeRow = fetch(`http://localhost:5000/remove_row`, {method: "POST", body: data.task})
        //     toDo(!showAll)
        // });
    }
}

let showAll = true;
document.getElementById("btn").addEventListener("click", clickButton);
function clickButton() {
    if (showAll) {
        document.getElementById("btn").innerHTML = "Show all";
        toDo(true)
        showAll = false
    }
    else {
        document.getElementById("btn").innerHTML = "Show not<br>finished";
        toDo(false)
        showAll = true
    }
}

toDo(false);

let addTask = document.getElementById("input");
let inputText = document.getElementById("task");
addTask.addEventListener("submit", (e) => {
    e.preventDefault();
    console.log(inputText);
    let taskToAdd = fetch("http://localhost:2000/todo_task", {method: "POST", body: inputText.value});
    toDo(!showAll);
    inputText.value = "";
})

