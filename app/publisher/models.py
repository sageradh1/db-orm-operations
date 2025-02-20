"""
Publisher model
"""

# pylint: disable=too-many-arguments

from app.extensions import db


class Publisher(db.Model):
    """
    DB entity for Publisher
    returns: SQLAlchemy DB Model Object in Publisher form
    """

    __tablename__ = "publishers"

    publisher_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    articles = db.relationship(
        "Article",
        back_populates="publisher",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    sentiments = db.relationship(
        "Sentiment",
        back_populates="publisher",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    batch_statuses = db.relationship(
        "BatchStatus",
        back_populates="publisher",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    name = db.Column(db.Text, nullable=False, unique=True)
    contact_name = db.Column(db.Text)
    contact_email = db.Column(db.Text)
    contact_phone = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    last_updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), onupdate=db.func.now()
    )

    def __init__(self, name, contact_name=None, contact_email=None, contact_phone=None):
        self.name = name
        if contact_name:
            self.contact_name = contact_name

        if contact_email:
            self.contact_email = contact_email

        if contact_phone:
            self.contact_phone = contact_phone

    def to_dict(self):
        """
        To convert class object to required python dictionary
        returns: Publisher in python dictionary
        """
        entity = {
            "publisher_id": self.publisher_id,
            "name": self.name,
            "contact_name": self.contact_name,
            "contact_email": self.contact_email,
            "contact_phone": self.contact_phone,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_updated_at": (
                self.last_updated_at.isoformat() if self.last_updated_at else None
            ),
        }
        return entity


class PublisherUtility:
    """
    Extra Utilities for Publisher
    """

    @staticmethod
    def to_dict_from_id(publisher_id):
        """
        To get Publisher object in a format suitable as a response with ID only
        Application:
            1. When Publisher object is not available right away in returnable format
            2. If Publisher is already instantiated, but to_dict() method cannot be accessed
        returns: Publisher in python dictionary
        """
        publisher = Publisher.query.get(publisher_id)

        return {
            "publisher_id": publisher.publisher_id,
            "name": publisher.name,
            "contact_name": publisher.contact_name,
            "contact_email": publisher.contact_email,
            "contact_phone": publisher.contact_phone,
            "created_at": (
                publisher.created_at.isoformat() if publisher.created_at else None
            ),
            "last_updated_at": (
                publisher.last_updated_at.isoformat()
                if publisher.last_updated_at
                else None
            ),
        }
