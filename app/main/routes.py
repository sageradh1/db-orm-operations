"""
API Routes for Core Functions
"""

import os

from flask import jsonify

from app.logger import app_logger

from . import main


@main.route("/health-check", methods=["GET"])
def index():
    """Health check route"""
    app_logger.info("Health-check")
    return jsonify({"status": 200, "message": "success"})


@main.route("/", methods=["GET"])
def main_index():
    """Base route"""
    app_logger.info("Base route")
    # return jsonify({"status": 200, "message": "success"})

    return jsonify({"status": 200, "message": os.getenv("SQLALCHEMY_SCHEMA")})
