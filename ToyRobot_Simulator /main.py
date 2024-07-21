from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


class Robot:
    def __init__(self):
        self.x = None
        self.y = None
        self.direction = None
        self.directions = ['NORTH', 'EAST', 'SOUTH', 'WEST']

    def place(self, x, y, direction):
        if direction in self.directions:
            self.x = x
            self.y = y
            self.direction = direction

    def move(self, table):
        if self.direction == 'NORTH' and table.is_valid_position(self.x, self.y + 1):
            self.y += 1
        elif self.direction == 'EAST' and table.is_valid_position(self.x + 1, self.y):
            self.x += 1
        elif self.direction == 'SOUTH' and table.is_valid_position(self.x, self.y - 1):
            self.y -= 1
        elif self.direction == 'WEST' and table.is_valid_position(self.x - 1, self.y):
            self.x -= 1
        else:
            return "Movement not allowed. Robot will fall off the table."
        return None

    def left(self):
        self.direction = self.directions[(self.directions.index(self.direction) - 1) % 4]

    def right(self):
        self.direction = self.directions[(self.directions.index(self.direction) + 1) % 4]

    def report(self):
        return f"{self.x}, {self.y},{self.direction}"

    def reset(self):
        self.x = None
        self.y = None
        self.direction = None


class Table:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def is_valid_position(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height


class Simulator:
    def __init__(self):
        self.robot = Robot()
        self.table = Table(5, 5)

    def execute_command(self, command):
        parts = command.split()
        if parts[0] == 'PLACE' and len(parts) == 2:
            params = parts[1].split(',')
            if len(params) == 3:
                try:
                    x, y = int(params[0]), int(params[1])
                    direction = params[2]
                    if self.table.is_valid_position(x, y):
                        self.robot.place(x, y, direction)
                except ValueError:
                    pass
        elif parts[0] == 'MOVE':
            if self.robot.x is None or self.robot.y is None or self.robot.direction is None:
                return {"result": "The robot is not yet placed on the table. Please command 'PLACE X,Y,F'"}
            error_message = self.robot.move(self.table)
            if error_message:
                return {"error": error_message}
            'return self.robot.move(self.table)'
        elif parts[0] == 'LEFT':
            if self.robot.x is None or self.robot.y is None or self.robot.direction is None:
                return {"result": "The robot is not placed on the table. Place it with 'PLACE X,Y,F'"}
            self.robot.left()
        elif parts[0] == 'RIGHT':
            if self.robot.x is None or self.robot.y is None or self.robot.direction is None:
                return {"result": "please place the robot on the table with 'PLACE X,Y,F'"}
            self.robot.right()
        elif parts[0] == 'REPORT':
            if self.robot.x is None or self.robot.y is None or self.robot.direction is None:
                return {"result": "The robot is not yet placed on the table. Please command 'PLACE X,Y,F'"}
            return {"result": self.robot.report()}
        elif parts[0] == 'RESET':
            self.robot.reset()
        return None


simulator = Simulator()


@app.route('/')
def index():
    return render_template('index.html', robot=simulator.robot)


@app.route('/command', methods=['POST'])
def command():
    command = request.json.get('command')
    result = simulator.execute_command(command)
    if result is None:
        result = {'robot': simulator.robot.__dict__}
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
