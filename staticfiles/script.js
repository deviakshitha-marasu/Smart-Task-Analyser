async function analyzeTasks() {
    let rawInput = document.getElementById("taskInput").value;

    try {
        let tasks = JSON.parse(rawInput);

        let response = await fetch("/api/tasks/analyze/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(tasks)
        });

        let data = await response.json();
        displayResults(data.tasks);

    } catch (err) {
        alert("Invalid JSON input!");
        console.error(err);
    }
}

function displayResults(tasks) {
    const container = document.getElementById("results");
    container.innerHTML = "";

    tasks.forEach(task => {
        let card = document.createElement("div");
        card.className = "task-card";

        card.innerHTML = `
            <h3>${task.title}</h3>
            <p><strong>Due:</strong> ${task.due_date}</p>
            <p><strong>Importance:</strong> ${task.importance}</p>
            <p><strong>Estimated Hours:</strong> ${task.estimated_hours}</p>
            <p><strong>Score:</strong> ${task.score}</p>
        `;

        container.appendChild(card);
    });
}
