var kanban_list = ["kanban", "kanbanadd", "kanbanmove", "kanbanclear", "kanbanlistboards", "kanbanrenameboard", "kanbanaddboard", "kanbanswitchboard"];
var pomodoro_list = ["pomodoro"];
var streaking_list = ["kanbangetstreak", "kanbanaddstreak"];

var commands_div = document.getElementById("command-list-div");

var all_tab = document.getElementById("all-tab");
var kanban_tab = document.getElementById("kanban-tab");
var pomodoro_tab = document.getElementById("pomodoro-tab");
var streaking_tab = document.getElementById("streaking-tab");

var tabs_list = [all_tab, kanban_tab, pomodoro_tab, streaking_tab];

var command_description = {
    "kanban": "Open the kanban board",
    "kanbanadd": "Add a task to the kanban board",
    "kanbanmove": "Move a task in the kanban board",
    "kanbanclear": "Clear the kanban board",
    "kanbanlistboards": "List all kanban boards",
    "kanbanrenameboard": "Rename a kanban board",
    "kanbanaddboard": "Add a new kanban board",
    "kanbanswitchboard": "Switch to a different kanban board",
    "pomodoro": "Start a pomodoro timer",
    "kanbangetstreak": "Get the current streak",
    "kanbanaddstreak": "Add to the current streak"
}

var command_example = {
    "kanban": "kanban",
    "kanbanadd": "kanbanadd <task>",
    "kanbanmove": "kanbanmove <task> <column>",
    "kanbanclear": "kanbanclear",
    "kanbanlistboards": "kanbanlistboards",
    "kanbanrenameboard": "kanbanrenameboard <old> <new>",
    "kanbanaddboard": "kanbanaddboard <name>",
    "kanbanswitchboard": "kanbanswitchboard <name>",
    "pomodoro": "pomodoro",
    "kanbangetstreak": "kanbangetstreak",
    "kanbanaddstreak": "kanbanaddstreak"
}

function loadAllCommands() {
    for (var i = 0; i < tabs_list.length; i++) {
        tabs_list[i].classList.remove("is-active");
    }
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
    }
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
    }
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
    }
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

function createCommandModal(command) {
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
                    <h2>Example</h2>
                    <p>${command_example[command]}</p>
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