"""
API Routes for BatchStatus
"""

from flask_restx import Namespace

from .models import BatchStatus

# from app.extensions import db


batch_status_ns = Namespace(
    "batch_statuses", description="Batch status related operations"
)
