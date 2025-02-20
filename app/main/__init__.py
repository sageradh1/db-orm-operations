"""
Entry point for the module
"""

from flask import Blueprint

main = Blueprint("main", __name__)

# pylint: disable=R0401,C0413
from . import routes
