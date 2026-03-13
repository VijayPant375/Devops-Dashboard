"""
DevOps Dashboard - Flask Web Application
Academic Project: Dockerized Web Application Deployment with Automated CI/CD
"""

import os
import socket
import platform
import datetime
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# App metadata
APP_VERSION = "1.1.0"
APP_NAME = "DevOps Dashboard"


def get_system_info():
    """Collect runtime environment info to display in dashboard."""
    return {
        "hostname": socket.gethostname(),
        "platform": platform.system(),
        "python_version": platform.python_version(),
        "container_id": socket.gethostname(),  # In Docker, hostname = container ID
        "timestamp": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "environment": os.environ.get("APP_ENV", "production"),
        "version": APP_VERSION,
    }


@app.route("/")
def index():
    """Render the main dashboard page."""
    info = get_system_info()
    return render_template("index.html", info=info, app_name=APP_NAME)


@app.route("/health")
def health():
    """Health check endpoint — used by Docker and load balancers."""
    return jsonify({
        "status": "healthy",
        "version": APP_VERSION,
        "timestamp": datetime.datetime.utcnow().isoformat(),
    }), 200


@app.route("/api/info")
def api_info():
    """REST API endpoint returning system info as JSON."""
    return jsonify(get_system_info()), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("APP_ENV", "production") == "development"
    app.run(host="0.0.0.0", port=port, debug=debug)
