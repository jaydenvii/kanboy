var kanban_list = ["kanban", "kanbanadd", "kanbanmove", "kanbanclear", "kanbanremove", "kanbanlistboards", "kanbanrenameboard", "kanbanrecolourboard", "kanbanaddboard", "kanbanswitchboard"];
var pomodoro_list = ["pomodoro", "leaderboard"];
var streaking_list = ["getstreaks", "streak", "addnewstreak", "removestreak", "clearstreak"];
var ai_list = ["kanboy"];

var commands_div = document.getElementById("command-list-div");

var all_tab = document.getElementById("all-tab");
var kanban_tab = document.getElementById("kanban-tab");
var pomodoro_tab = document.getElementById("pomodoro-tab");
var streaking_tab = document.getElementById("streaking-tab");
var ai_tab = document.getElementById("ai-tab");

var tabs_list = [all_tab, kanban_tab, pomodoro_tab, streaking_tab, ai_tab];

var command_description = {
    "kanban": "Displays the current Kanban board with tasks categorized into \"TODO\", \"DOING\", and \"DONE\".",
    "kanbanadd": "Adds a task to the current Kanban board with a specified priority level.",
    "kanbanmove": "Moves a task from one column to another on the current Kanban board.",
    "kanbanclear": "Clears the \"DONE\" column on the current Kanban board.",
    "kanbanremove": "Removes a task from a specified column on the current Kanban board.",
    "kanbanlistboards": "Lists all available Kanban boards along with their IDs.",
    "kanbanrenameboard": "Renames a Kanban board with the specified board number.",
    "kanbanrecolourboard": "Changes the color of a Kanban board with the specified board number.",
    "kanbanaddboard": "Adds a new Kanban board with the specified name and color.",
    "kanbanswitchboard": "Switches to a different Kanban board specified by its number.",
    "getstreaks": "Displays the streaks for various tasks.",
    "streak": "Increments the streak for a specified task.",
    "addnewstreak": "Adds a new task with an initial streak count of 0.",
    "removestreak": "Removes a task and its streak from the streak list.",
    "clearstreak": "Resets the streak for a specified task to 0.",
    "pomodoro": "Starts a Pomodoro timer for a specified duration.",
    "kanboy": "Interacts with an AI assistant to get responses to various prompts.",
    "leaderboard": "Displays the leaderboard showing users with the highest scores."
};

var command_params = {
    "kanban": [],
    "kanbanadd": ["task: The task description", "priority: Priority level (\"HIGH\", \"MEDIUM\", or \"LOW\")"],
    "kanbanmove": ["move_from: The column from which the task will be moved", "task_number: The number of the task to be moved", "move_to: The column to which the task will be moved"],
    "kanbanclear": [],
    "kanbanremove": ["remove_from: The column from which the task will be removed", "task_number: The number of the task to be removed"],
    "kanbanlistboards": [],
    "kanbanrenameboard": ["board_number: The number of the board to be renamed", "new_name: The new name for the board"],
    "kanbanrecolourboard": ["board_number: The number of the board to be recolored", "colour: The new color for the board"],
    "kanbanaddboard": ["name: The name of the new board", "colour: The color of the new board"],
    "kanbanswitchboard": ["number: The number of the board to switch to"],
    "getstreaks": [],
    "streak": ["options: The task for which the streak will be incremented"],
    "addnewstreak": ["task: The name of the new task"],
    "removestreak": ["options: The task to be removed"],
    "clearstreak": ["options: The task for which the streak will be reset"],
    "pomodoro": ["time: The duration of the Pomodoro timer", "unit: The unit of time (\"minutes\" or \"seconds\")"],
    "kanboy": ["prompt: The prompt to be responded to by the AI"],
    "leaderboard": [],
};

var command_example = {
    "kanban": "/kanban",
    "kanbanadd": "/kanbanadd \"Implement user authentication\" priority=HIGH",
    "kanbanmove": "/kanbanmove move_from=TODO task_number=3 move_to=DOING",
    "kanbanclear": "/kanbanclear",
    "kanbanremove": "/kanbanremove remove_from=DOING task_number=2",
    "kanbanlistboards": "/kanbanlistboards",
    "kanbanrenameboard": "/kanbanrenameboard board_number=2 new_name=\"Project X Development\"",
    "kanbanrecolourboard": "/kanbanrecolourboard board_number=3 colour=GREEN",
    "kanbanaddboard": "/kanbanaddboard name=\"Project Y Tasks\" colour=BLUE",
    "kanbanswitchboard": "/kanbanswitchboard number=2",
    "getstreaks": "/getstreaks",
    "streak": "/streak options=\"Exercise\"",
    "addnewstreak": "/addnewstreak task=\"Meditation\"",
    "removestreak": "/removestreak options=\"Reading\"",
    "clearstreak": "/clearstreak options=\"Coding\"",
    "pomodoro": "/pomodoro time=25 unit=minutes",
    "kanboy": "/kanboy prompt=\"What is the meaning of life?\"",
    "leaderboard": "/leaderboard"
};

function loadAllCommands() {
    for (var i = 0; i < tabs_list.length; i++) {
        tabs_list[i].classList.remove("is-active");
        tabs_list[i].classList.add("is-not-active");
    }
    all_tab.classList.remove("is-not-active");
    all_tab.classList.add("is-active");
    var full_list = kanban_list.concat(pomodoro_list).concat(streaking_list);
    commands_div.innerHTML = "";
    for (var i = 0; i < full_list.length; i++) {
        var command = full_list[i];
        var command_div = document.createElement("div");
        command_div.innerHTML = createCommandModal(command);
        commands_div.appendChild(command_div);
    }
    window.document.dispatchEvent(new Event("DOMContentLoaded", {
        bubbles: true,
        cancelable: true
    }));
}

function loadKanbanCommands() {
    for (var i = 0; i < tabs_list.length; i++) {
        tabs_list[i].classList.remove("is-active");
        tabs_list[i].classList.add("is-not-active");
    }
    kanban_tab.classList.remove("is-not-active");
    kanban_tab.classList.add("is-active");
    commands_div.innerHTML = "";
    for (var i = 0; i < kanban_list.length; i++) {
        var command = kanban_list[i];
        var command_div = document.createElement("div");
        command_div.innerHTML = createCommandModal(command);
        commands_div.appendChild(command_div);
    }
    window.document.dispatchEvent(new Event("DOMContentLoaded", {
        bubbles: true,
        cancelable: true
    }));
}

function loadPomodoroCommands() {
    for (var i = 0; i < tabs_list.length; i++) {
        tabs_list[i].classList.remove("is-active");
        tabs_list[i].classList.add("is-not-active");
    }
    pomodoro_tab.classList.remove("is-not-active");
    pomodoro_tab.classList.add("is-active");
    commands_div.innerHTML = "";
    for (var i = 0; i < pomodoro_list.length; i++) {
        var command = pomodoro_list[i];
        var command_div = document.createElement("div");
        command_div.innerHTML = createCommandModal(command);
        commands_div.appendChild(command_div);
    }
    window.document.dispatchEvent(new Event("DOMContentLoaded", {
        bubbles: true,
        cancelable: true
    }));
}

function loadStreakingCommands() {
    for (var i = 0; i < tabs_list.length; i++) {
        tabs_list[i].classList.remove("is-active");
        tabs_list[i].classList.add("is-not-active");
    }
    streaking_tab.classList.remove("is-not-active");
    streaking_tab.classList.add("is-active");
    commands_div.innerHTML = "";
    for (var i = 0; i < streaking_list.length; i++) {
        var command = streaking_list[i];
        var command_div = document.createElement("div");
        command_div.innerHTML = createCommandModal(command);
        commands_div.appendChild(command_div);
    }
    window.document.dispatchEvent(new Event("DOMContentLoaded", {
        bubbles: true,
        cancelable: true
    }));
}

function loadAICommands() {
    for (var i = 0; i < tabs_list.length; i++) {
        tabs_list[i].classList.remove("is-active");
        tabs_list[i].classList.add("is-not-active");
    }
    ai_tab.classList.remove("is-not-active");
    ai_tab.classList.add("is-active");
    commands_div.innerHTML = "";
    for (var i = 0; i < ai_list.length; i++) {
        var command = ai_list[i];
        var command_div = document.createElement("div");
        command_div.innerHTML = createCommandModal(command);
        commands_div.appendChild(command_div);
    }
    window.document.dispatchEvent(new Event("DOMContentLoaded", {
        bubbles: true,
        cancelable: true
    }));
}

function createCommandModal(command) {
    let = paramHTML = "";
    if (command_params[command].length > 0) {
        paramHTML = `
        <h2>Parameters</h2>
        <ul>
            ${command_params[command].map(param => `<li>${param}</li>`).join("")}
        </ul>
        `
    }

    const modalHTML = `
        <div id="modal-${command}" class="modal">
        <div class="modal-background"></div>
        <div class="modal-card">
            <header class="modal-card-head">
            <p class="modal-card-title">${command}</p>
            <button class="delete" aria-label="close"></button>
            </header>
            <section class="modal-card-body">
                <div class="content">
                    <h2>Description</h2>
                    <p>${command_description[command]}</p>
                    ${paramHTML}
                    <h2>Example</h2>
                    <code class="content size-is-2">${command_example[command]}</code>
                </div>
            </section>
        </div>
        </div>

        <a class="panel-block js-modal-trigger" data-target="modal-${command}">
        ${command}
        </a>
    `;
    return modalHTML;
}

function getDocHTML(command) {

}

loadAllCommands();