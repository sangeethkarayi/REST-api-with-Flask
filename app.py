from flask import Flask, request, jsonify

app = Flask(__name__)

users = [
    {
        "id": 1,
        "name": "Ada Lovelace",
        "email": "ada@example.com"
    },
    {
        "id": 2,
        "name": "Grace Hopper",
        "email": "grace@example.com"
    }
]
next_user_id = 3 

@app.route('/users', methods=['GET'])
def get_users():
    """Returns a list of all users."""
    return jsonify(users)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Returns a single user if found, otherwise a 404 error."""
    user = next((user for user in users if user['id'] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404


@app.route('/users', methods=['POST'])
def create_user():
    """Creates a new user."""
    global next_user_id
    if not request.json or not 'name' in request.json or not 'email' in request.json:
        return jsonify({"error": "Missing name or email in request body"}), 400

    new_user = {
        'id': next_user_id,
        'name': request.json['name'],
        'email': request.json['email']
    }
    users.append(new_user)
    next_user_id += 1
    return jsonify(new_user), 201 

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Updates an existing user's data."""
    user = next((user for user in users if user['id'] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    if not request.json:
        return jsonify({"error": "Invalid request body"}), 400

    user['name'] = request.json.get('name', user['name'])
    user['email'] = request.json.get('email', user['email'])
    
    return jsonify(user)

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a user."""
    global users
    user = next((user for user in users if user['id'] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    users = [u for u in users if u['id'] != user_id]
    return jsonify({"message": "User deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)