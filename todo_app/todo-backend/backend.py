from flask import Flask, request, jsonify

app = Flask(__name__)
todos = []

@app.route("/api/todos", methods=["GET"])
def get_todos():
    return jsonify(todos)

@app.route("/api/todos", methods=["POST"])
def add_todo():
    data = request.get_json()
    todo = data.get("todo", "").strip()
    if not todo:
        return jsonify({"error": "Todo cannot be empty"}), 400
    if len(todo) > 140:
        return jsonify({"error": "Todo too long"}), 400
    todos.append(todo)
    return jsonify({"success": True, "todo": todo}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
