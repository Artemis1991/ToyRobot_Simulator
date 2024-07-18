document.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById('command').focus();
});

function sendCommand() {
    event.preventDefault();
    const commandInput = document.getElementById('command');
    const command = commandInput.value.toUpperCase();
    if (command.trim() === '') return;

    appendToTerminal(`> ${command}`);

    fetch('/command', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ command })
    })
    .then(response => response.json())
    .then(data => {
        if (data.result) {
            appendToTerminal(data.result);
        }
         if (data.error) {
            showError(data.error);

        }
        updateGrid(data.robot);
    });

    commandInput.value = '';
}

function appendToTerminal(text) {
    const terminalOutput = document.getElementById('terminal-output');
    terminalOutput.innerText += text + '\n';
    terminalOutput.scrollTop = terminalOutput.scrollHeight;
}

function updateGrid(robot) {
    const cells = document.querySelectorAll('.cell');
    cells.forEach(cell => cell.innerHTML = '');

    if (robot.x !== null && robot.y !== null) {
        const cell = document.getElementById(`cell-${robot.x}-${robot.y}`);
        const img = document.createElement('img');
        img.src = '/static/robot.png';
        img.id = 'robot';
        img.classList.add('robot', robot.direction.toLowerCase());
        cell.appendChild(img);
    }
}

function toUpperCase() {
    const commandInput = document.getElementById('command');
    commandInput.value = commandInput.value.toUpperCase();
}
function showError(message) {
    const errorContainer = document.getElementById('error-container');
    errorContainer.innerText = message;
    setTimeout(() => {
        errorContainer.innerText = '';
    }, 2000);
    updateGrid(data.robot);
}
function resetSimulator() {
    fetch('/command', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ command: 'RESET' })
    })
    .then(response => response.json())
    .then(data => {
        appendToTerminal('> RESET');
        updateGrid(data.robot);
    });
}
