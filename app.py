"""
Flask Backend for Dharam Jai Vardhan Reddy's Portfolio Website
Handles serving the frontend, API endpoints for contact form submissions,
project retrieval, and live portfolio data configuration.
"""

import os
import re
import json
from flask import Flask, render_template, request, jsonify, redirect, url_for
from database import init_db, save_contact_message, get_all_projects, get_contact_messages

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "portfolio-dev-secret-key-2028")

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")


def load_portfolio_data():
    """Loads editable portfolio configuration from portfolio_data.json."""
    data_path = os.path.join(os.path.dirname(__file__), "portfolio_data.json")
    if os.path.exists(data_path):
        try:
            with open(data_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            app.logger.error(f"Error reading portfolio_data.json: {e}")
    return {}


@app.before_request
def setup_database_if_needed():
    """Ensure database tables exist before processing the first request."""
    if not hasattr(app, "_db_initialized"):
        try:
            init_db()
            app._db_initialized = True
        except Exception as e:
            app.logger.error(f"Failed to auto-initialize database: {e}")


@app.route("/")
def index():
    """Renders the main full-screen scroll-snap portfolio page."""
    data = load_portfolio_data()
    projects = get_all_projects() or data.get("projects", [])
    status = request.args.get("status")
    return render_template("index.html", data=data, projects=projects, status=status)


@app.route("/api/portfolio-data", methods=["GET"])
def get_portfolio_data():
    """Returns the complete editable portfolio data as JSON."""
    return jsonify({"success": True, "data": load_portfolio_data()}), 200


@app.route("/api/projects", methods=["GET"])
def list_projects():
    """Returns all featured projects as JSON."""
    try:
        data = load_portfolio_data()
        projects = data.get("projects") or get_all_projects()
        return jsonify({"success": True, "projects": projects}), 200
    except Exception as e:
        app.logger.error(f"Error fetching projects: {e}")
        return jsonify({"success": False, "error": "Unable to retrieve projects"}), 500


@app.route("/api/contact", methods=["POST"])
def submit_contact():
    """
    Receives contact form submissions.
    Supports both modern JSON (AJAX fetch) and standard x-www-form-urlencoded (traditional HTML form).
    Validates input and safely inserts into database using parameterized queries to prevent SQL injection.
    """
    if request.is_json:
        data = request.get_json() or {}
    else:
        data = request.form.to_dict()

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    subject = data.get("subject", "").strip()
    message = data.get("message", "").strip()

    # Input Validation
    errors = []
    if not name or len(name) < 2:
        errors.append("Please provide a valid name (at least 2 characters).")
    elif len(name) > 100:
        errors.append("Name must not exceed 100 characters.")

    if not email or not EMAIL_REGEX.match(email):
        errors.append("Please provide a valid email address.")
    elif len(email) > 255:
        errors.append("Email must not exceed 255 characters.")

    if not subject or len(subject) < 3:
        errors.append("Subject is required (at least 3 characters).")
    elif len(subject) > 200:
        errors.append("Subject must not exceed 200 characters.")

    if not message or len(message) < 10:
        errors.append("Message must be at least 10 characters long.")
    elif len(message) > 5000:
        errors.append("Message must not exceed 5000 characters.")

    if errors:
        if request.is_json or request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({"success": False, "error": " ".join(errors)}), 400
        return redirect(url_for("index", status="error", _anchor="contact"))

    try:
        message_id = save_contact_message(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        app.logger.info(f"New contact message received from {email} (ID: {message_id})")

        if request.is_json or request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({
                "success": True,
                "message": "Thank you! Your inquiry has been delivered directly to Dharam's SQL database.",
                "id": message_id
            }), 201
        
        return redirect(url_for("index", status="success", _anchor="contact"))

    except Exception as e:
        app.logger.error(f"Database error while saving contact message: {e}")
        if request.is_json or request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({
                "success": False,
                "error": "A server error occurred while sending your message. Please try again."
            }), 500
        return redirect(url_for("index", status="server_error", _anchor="contact"))


@app.route("/api/messages", methods=["GET"])
def view_messages():
    """Optional endpoint to view messages for admin/testing."""
    try:
        messages = get_contact_messages(limit=50)
        return jsonify({"success": True, "count": len(messages), "messages": messages}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    print(f"[*] Portfolio Server running at http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)
