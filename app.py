from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = 'tasks.json'

def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            try:
                data = json.load(file)
                # Ensure all keys are integers
                return {int(k): v for k, v in data.items()}
            except json.JSONDecodeError:
                return {}
    return {}

def save_tasks(tasks):
    with open(DATA_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

tasks = load_tasks()

@app.route('/tasks', methods=['POST'])
def add_task():
    task_id = max(tasks.keys(), default=0) + 1
    task_data = request.json
    tasks[task_id] = task_data
    save_tasks(tasks)
    return jsonify({'message': 'Task added', 'task_id': task_id}), 201

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def remove_task(task_id):
    if task_id in tasks:
        del tasks[task_id]
        save_tasks(tasks)
        return jsonify({'message': 'Task removed'}), 200
    else:
        return jsonify({'message': 'Task not found'}), 404

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def edit_task(task_id):
    if task_id in tasks:
        task_data = request.json
        tasks[task_id] = task_data
        save_tasks(tasks)
        return jsonify({'message': 'Task updated'}), 200
    else:
        return jsonify({'message': 'Task not found'}), 404

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks), 200

if __name__ == '__main__':
    app.run(debug=True)
