"""
BatchStatus model
"""

# pylint: disable=too-many-arguments

from app.extensions import db


class BatchStatus(db.Model):
    """
    DB entity for BatchStatus
    returns: SQLAlchemy DB Model Object in BatchStatus form
    """

    __tablename__ = "batch_statuses"

    batch_id = db.Column(db.Text, primary_key=True)

    publisher_id = db.Column(
        db.Integer,
        db.ForeignKey("publishers.publisher_id", ondelete="CASCADE"),
        nullable=False,
    )
    publisher = db.relationship("Publisher", back_populates="batch_statuses")

    sentiments = db.relationship("Sentiment", backref="batch_status", lazy=True)

    object_type = db.Column(db.Text)
    endpoint = db.Column(db.Text)
    errors = db.Column(db.Text)
    input_file_id = db.Column(db.Text)
    completion_window = db.Column(db.Text)
    status = db.Column(db.Text)
    output_file_id = db.Column(db.Text)
    error_file_id = db.Column(db.Text)
    in_progress_at = db.Column(db.DateTime, nullable=True)
    expires_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    failed_at = db.Column(db.DateTime, nullable=True)
    expired_at = db.Column(db.DateTime, nullable=True)
    request_total = db.Column(db.Integer)
    request_completed = db.Column(db.Integer)
    request_failed = db.Column(db.Integer)
    set_metadata = db.Column(db.JSON, nullable=True)
    batch_type = db.Column(db.Text)
    are_results_uploaded = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    last_updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), onupdate=db.func.now()
    )

    def __init__(
        self,
        publisher_id,
        object_type=None,
        endpoint=None,
        errors=None,
        input_file_id=None,
        completion_window=None,
        status=None,
        output_file_id=None,
        error_file_id=None,
        in_progress_at=None,
        expires_at=None,
        completed_at=None,
        failed_at=None,
        expired_at=None,
        request_total=None,
        request_completed=None,
        request_failed=None,
        set_metadata=None,
        batch_type=None,
        are_results_uploaded=None,
    ):
        if publisher_id:
            self.publisher_id = publisher_id
        if object_type:
            self.object_type = object_type
        if endpoint:
            self.endpoint = endpoint
        if errors:
            self.errors = errors
        if input_file_id:
            self.input_file_id = input_file_id
        if completion_window:
            self.completion_window = completion_window
        if status:
            self.status = status
        if output_file_id:
            self.output_file_id = output_file_id
        if error_file_id:
            self.error_file_id = error_file_id
        if in_progress_at:
            self.in_progress_at = in_progress_at
        if expires_at:
            self.expires_at = expires_at
        if completed_at:
            self.completed_at = completed_at
        if failed_at:
            self.failed_at = failed_at
        if expired_at:
            self.expired_at = expired_at
        if request_total:
            self.request_total = request_total
        if request_completed:
            self.request_completed = request_completed
        if request_failed:
            self.request_failed = request_failed
        if set_metadata:
            self.set_metadata = set_metadata
        if batch_type:
            self.batch_type = batch_type
        if are_results_uploaded:
            self.are_results_uploaded = are_results_uploaded
