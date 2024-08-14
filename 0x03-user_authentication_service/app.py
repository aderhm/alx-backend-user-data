#!/usr/bin/env python3
""" Flask app module
"""

from auth import Auth
from flask import Flask, abort, jsonify, request


AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=["GET"])
def welcome():
    """ Return a welcome message
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """ Register a new user
    """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify({
            "email": email,
            "message": "user created"
        })
    except ValueError:
        return jsonify({
            "message": "email already registered"
            }), 400


@app.route("/sessions", methods=["POST"])
def login():
    """ Log a user in
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if AUTH.valid_login(email, password):
        AUTH.create_session(email)
        return jsonify({
            "email": email,
            "message": "logged in"
        })
    abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
