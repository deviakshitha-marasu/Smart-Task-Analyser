let taskArray = [];
let editIndex = null;

function addTask() {
    const name = document.getElementById("taskName").value.trim();
    const dueDate = document.getElementById("dueDate").value;
    const importance = document.getElementById("importance").value;
    const hours = parseFloat(document.getElementById("hours").value);

    if (!name) {
        alert("Task name is required.");
        return;
    }

    const task = {
        title: name,
        due_date: dueDate,
        importance: parseInt(importance),
        estimated_hours: hours
    };

    if (editIndex !== null) {
        taskArray[editIndex] = task;
        editIndex = null;
        document.getElementById("addBtn").innerText = "+ Add Task";
    } else {
        taskArray.push(task);
    }

    updateTaskList();

    document.getElementById("taskName").value = "";
    document.getElementById("dueDate").value = "";
    document.getElementById("hours").value = "1";
}

function updateTaskList() {
    const table = document.getElementById("taskTableBody");
    table.innerHTML = "";

    taskArray.forEach((task, index) => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${task.title}</td>
            <td>${task.due_date || "N/A"}</td>
            <td>${task.importance}</td>
            <td>${task.estimated_hours}</td>
            <td class="actions">
                <span class="edit-btn" onclick="editTask(${index})">✎ Edit</span>
                <span class="delete-btn" onclick="removeTask(${index})">🗑 Delete</span>
            </td>
        `;

        table.appendChild(row);
    });
}

function editTask(index) {
    const t = taskArray[index];
    editIndex = index;

    document.getElementById("taskName").value = t.title;
    document.getElementById("dueDate").value = t.due_date;
    document.getElementById("importance").value = t.importance;
    document.getElementById("hours").value = t.estimated_hours;

    document.getElementById("addBtn").innerText = "Update Task";
}

function removeTask(index) {
    taskArray.splice(index, 1);
    updateTaskList();
}

async function analyzeTasks() {
    if (taskArray.length === 0) {
        alert("Add at least one task!");
        return;
    }

    try {
        const response = await fetch("/api/tasks/analyze/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(taskArray)
        });

        const data = await response.json();
        displayResults(data.tasks);

    } catch (err) {
        console.error(err);
        alert("Error connecting to backend.");
    }
}

function displayResults(tasks) {
    const results = document.getElementById("results");
    const suggestions = document.getElementById("suggestions");

    results.innerHTML = "";
    suggestions.innerHTML = "";

    if (tasks.length > 0) {
        const first = tasks[0];
        suggestions.innerHTML = `
            <div class="card top">
                <h3>${first.title}</h3>
                <p><strong>Due:</strong> ${first.due_date || "N/A"}</p>
                <p><strong>Score:</strong> ${first.score}</p>
            </div>`;
    }

    tasks.forEach(t => {
        const div = document.createElement("div");
        div.className = "task-card";

        let barClass =
            t.importance >= 5 ? "priority-high" :
            t.importance === 3 || t.importance === 4 ? "priority-medium" :
            "priority-low";

        div.innerHTML = `
            <div class="priority-bar ${barClass}"></div>
            <div class="title">${t.title}</div>
            <div class="meta"><strong>Due:</strong> ${t.due_date || "N/A"}</div>
            <div class="meta"><strong>Importance:</strong> ${t.importance}</div>
            <div class="meta"><strong>Hours:</strong> ${t.estimated_hours}</div>
            <div class="meta"><strong>Score:</strong> ${t.score}</div>
        `;

        results.appendChild(div);
    });
}
