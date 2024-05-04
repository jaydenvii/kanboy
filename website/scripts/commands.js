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

}

var command_example = {
    
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
                ${command}
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