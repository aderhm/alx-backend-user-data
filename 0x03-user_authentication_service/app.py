#!/usr/bin/env python3
""" Flask app module
"""

from auth import Auth
from flask import Flask, abort, jsonify, redirect, request


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
        sid = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", sid)
        return response
    abort(401)


@app.route("/sessions", methods=["DELETE"])
def logout():
    """ Log a user out
    """
    sid = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(sid)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", methods=["GET"])
def profile():
    """ Get the user profile
    """
    sid = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(sid)
    if user:
        return jsonify({"email": user.email}), 200
    abort(403)


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token():
    """ Get reset password token
    """
    email = request.form.get("email")
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({
            "email": email,
            "reset_token": token
        }), 200
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"])
def update_password():
    """ Update password
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"})
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
