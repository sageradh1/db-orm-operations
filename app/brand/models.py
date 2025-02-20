"""
Brand model
"""

# pylint: disable=too-many-arguments

import enum

from app.extensions import db


class FixedEntityTypeEnum(enum.Enum):
    product = "product"
    person = "person"
    company = "company"
    event = "event"
    government = "government"
    educational = "educational"
    ngo = "ngo"
    other = "other"


class Brand(db.Model):
    """
    DB entity for Brand
    returns: SQLAlchemy DB Model Object in Brand form
    """

    __tablename__ = "brands"

    brand_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    sentiments = db.relationship(
        "Sentiment",
        back_populates="brand",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    name = db.Column(db.Text)
    website = db.Column(db.Text, unique=True, nullable=False)
    contact_name = db.Column(db.Text)
    contact_email = db.Column(db.Text)
    contact_phone = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    last_updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), onupdate=db.func.now()
    )

    entity_type = db.Column(db.Text)
    fixed_entity_type = db.Column(db.Enum(FixedEntityTypeEnum), nullable=True)
    apollo_enrichment = db.Column(db.JSON)

    def __init__(
        self,
        name,
        website=None,
        contact_name=None,
        contact_email=None,
        contact_phone=None,
        entity_type=None,
        fixed_entity_type=None,
        apollo_enrichment=None,
    ):
        self.name = name
        if website:
            self.website = website

        if contact_name:
            self.contact_name = contact_name

        if contact_email:
            self.contact_email = contact_email

        if contact_phone:
            self.contact_phone = contact_phone

        if entity_type:
            self.entity_type = entity_type

        if fixed_entity_type:
            self.fixed_entity_type = fixed_entity_type

        if apollo_enrichment:
            self.apollo_enrichment = apollo_enrichment

    def to_dict(self):
        """
        To convert class object to required python dictionary
        returns: Brand in python dictionary
        """
        return {
            "brand_id": self.brand_id,
            "name": self.name,
            "website": self.website,
            "contact_name": self.contact_name,
            "contact_email": self.contact_email,
            "contact_phone": self.contact_phone,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_updated_at": (
                self.last_updated_at.isoformat() if self.last_updated_at else None
            ),
            "entity_type": self.entity_type,
            "fixed_entity_type": self.fixed_entity_type,
            "apollo_enrichment": self.apollo_enrichment,    
        }


class BrandUtility:
    """
    Extra Utilities for Brand
    """

    @staticmethod
    def to_dict_from_id(brand_id):
        """
        To get Brand object in a format suitable as a response with ID only
        Application:
            1. When Brand object is not available right away in returnable format
            2. If Brand is already instantiated, but to_dict() method cannot be accessed
        returns: Brand in python dictionary
        """
        brand = Brand.query.get(brand_id)

        print("contact", brand.contact_name)
        return {
            "brand_id": brand.brand_id,
            "name": brand.name,
            "website": brand.website,
            "contact_name": brand.contact_name,
            "contact_email": brand.contact_email,
            "contact_phone": brand.contact_phone,
            "created_at": (brand.created_at.isoformat() if brand.created_at else None),
            "last_updated_at": (
                brand.last_updated_at.isoformat() if brand.last_updated_at else None
            ),
            "entity_type": brand.entity_type,
            "fixed_entity_type": brand.fixed_entity_type,
            "apollo_enrichment": brand.apollo_enrichment,
        }
