console.log("SCRIPT LOADED");

let currentFilter = "all";

// Add Task
async function addTask() {

    let taskInput =
        document.getElementById("taskInput");

    let task =
        taskInput.value;

    let priority =
        document.getElementById("priorityInput").value;

    let category =
        document.getElementById("categoryInput").value;

    let dueDate =
        document.getElementById("dueDateInput").value;

    if (task.trim() === "") {
        alert("Enter a task");
        return;
    }

    await fetch("/add_task", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            task: task,
            priority: priority,
            category: category,
            dueDate: dueDate
        })
    });

    taskInput.value = "";

    loadTasks();
}


// Load Tasks
async function loadTasks() {

    let response =
        await fetch("/get_tasks");

    let tasks =
        await response.json();

    // Sorting

    let sortType =
        document.getElementById(
            "sortSelect"
        ).value;

    if (sortType === "priority") {

        const priorityOrder = {
            High: 1,
            Medium: 2,
            Low: 3
        };

        tasks.sort((a, b) =>
            priorityOrder[a.priority] -
            priorityOrder[b.priority]
        );
    }

    else if (sortType === "duedate") {

        tasks.sort((a, b) => {

            if (!a.dueDate) return 1;
            if (!b.dueDate) return -1;

            return a.dueDate.localeCompare(
                b.dueDate
            );

        });
    }

    else {

        tasks.sort((a, b) =>
            b.id - a.id
        );
    }

    // Dashboard

    let total =
        tasks.length;

    let completed =
        tasks.filter(
            task => task.completed === 1
        ).length;

    let remaining =
        total - completed;

    let percentage = 0;

    if (total > 0) {

        percentage =
            Math.round(
                (completed / total) * 100
            );

    }

    document.getElementById(
        "totalTasks"
    ).textContent = total;

    document.getElementById(
        "completedTasks"
    ).textContent = completed;

    document.getElementById(
        "remainingTasks"
    ).textContent = remaining;

    document.getElementById(
        "progressBar"
    ).style.width =
        percentage + "%";

    document.getElementById(
        "progressText"
    ).textContent =
        percentage + "% Completed";

    // Celebration

    let celebration =
        document.getElementById(
            "celebrationMessage"
        );

    if (
        total > 0 &&
        completed === total
    ) {

        celebration.innerHTML =
            "🎉 Congratulations! All tasks completed!";

    }
    else {

        celebration.innerHTML = "";

    }

    // Task List

    let taskList =
        document.getElementById(
            "taskList"
        );

    taskList.innerHTML = "";

    tasks.forEach(task => {

        let today =
            new Date()
            .toISOString()
            .split("T")[0];

        let overdue =
            task.dueDate &&
            task.dueDate < today &&
            !task.completed;

        // Filters

        if (
            currentFilter === "pending" &&
            task.completed
        ) {
            return;
        }

        if (
            currentFilter === "completed" &&
            !task.completed
        ) {
            return;
        }

        if (
            currentFilter === "high" &&
            task.priority !== "High"
        ) {
            return;
        }

        if (
            currentFilter === "overdue" &&
            !overdue
        ) {
            return;
        }

        let priorityColor = "";

        if (task.priority === "High") {
            priorityColor = "red";
        }
        else if (
            task.priority === "Medium"
        ) {
            priorityColor = "orange";
        }
        else {
            priorityColor = "green";
        }

        let categoryEmoji = "";

        if (task.category === "Study") {
            categoryEmoji = "📚";
        }
        else if (
            task.category === "Work"
        ) {
            categoryEmoji = "💼";
        }
        else if (
            task.category === "Health"
        ) {
            categoryEmoji = "🏃";
        }
        else {
            categoryEmoji = "🏠";
        }

        let li =
            document.createElement("li");

        li.innerHTML = `

            <div class="task-info">

                <div class="category">
                    ${categoryEmoji}
                    ${task.category}
                </div>

                <h3
                    class="task-title"
                    style="
                        text-decoration:
                        ${task.completed ? 'line-through' : 'none'};

                        color:
                        ${overdue ? '#ff9f43' : 'white'};
                    "
                >
                    ${task.task}
                </h3>

                <div class="task-meta">

                    <span
                        class="priority-badge"
                        style="
                            background:
                            ${priorityColor};
                        "
                    >
                        ${task.priority}
                    </span>

                    <span class="due-date">
                        📅
                        ${task.dueDate || "No Due Date"}
                    </span>

                </div>

            </div>

            <div class="task-actions">

                <button
                    onclick="editTask(
                        ${task.id},
                        '${task.task}'
                    )"
                >
                    Edit
                </button>

                <button
                    onclick="
                        toggleComplete(
                            ${task.id}
                        )
                    "
                >
                    ${
                        task.completed
                        ? "Undo"
                        : "Complete"
                    }
                </button>

                <button
                    onclick="
                        deleteTask(
                            ${task.id}
                        )
                    "
                >
                    Delete
                </button>

            </div>

        `;

        taskList.appendChild(li);

    });

}


// Edit Task
async function editTask(
    taskId,
    currentTask
) {

    let newTask =
        prompt(
            "Edit Task",
            currentTask
        );

    if (
        newTask === null ||
        newTask.trim() === ""
    ) {
        return;
    }

    await fetch(
        `/edit_task/${taskId}`,
        {
            method: "PUT",
            headers: {
                "Content-Type":
                "application/json"
            },
            body: JSON.stringify({
                task: newTask
            })
        }
    );

    loadTasks();
}


// Complete Task
async function toggleComplete(
    taskId
) {

    await fetch(
        `/toggle_complete/${taskId}`,
        {
            method: "PUT"
        }
    );

    loadTasks();
}


// Delete Task
async function deleteTask(
    taskId
) {

    let confirmDelete =
        confirm(
            "Delete this task?"
        );

    if (!confirmDelete) {
        return;
    }

    await fetch(
        `/delete_task/${taskId}`,
        {
            method: "DELETE"
        }
    );

    loadTasks();
}


// Search Tasks
function searchTasks() {

    let searchText =
        document
        .getElementById(
            "searchInput"
        )
        .value
        .toLowerCase();

    let tasks =
        document.querySelectorAll(
            "#taskList li"
        );

    tasks.forEach(task => {

        let text =
            task.textContent
            .toLowerCase();

        if (
            text.includes(
                searchText
            )
        ) {
            task.style.display =
                "";
        }
        else {
            task.style.display =
                "none";
        }

    });

}


// Filters

function showAll() {
    currentFilter = "all";
    loadTasks();
}

function showPending() {
    currentFilter = "pending";
    loadTasks();
}

function showCompleted() {
    currentFilter = "completed";
    loadTasks();
}

function showHighPriority() {
    currentFilter = "high";
    loadTasks();
}

function showOverdue() {
    currentFilter = "overdue";
    loadTasks();
}


// Start App
loadTasks();

function exportCSV() {

    window.location.href =
        "/export_csv";

}