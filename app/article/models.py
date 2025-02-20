# from flask import current_app

from app.extensions import db


class Article(db.Model):
    __tablename__ = "articles"

    article_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    publisher_id = db.Column(
        db.Integer,
        db.ForeignKey("publishers.publisher_id", ondelete="CASCADE"),
        nullable=False,
    )
    publisher = db.relationship("Publisher", back_populates="articles")

    brand_mentions = db.relationship(
        "BrandMention",
        back_populates="article",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    sentiments = db.relationship(
        "Sentiment",
        back_populates="article",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    url = db.Column(db.Text, nullable=False, unique=True)
    in_article_tags = db.Column(db.Text)
    out_article_tags = db.Column(db.Text)
    in_article_date = db.Column(db.DateTime)
    out_article_date = db.Column(db.DateTime)
    links = db.Column(db.Text)
    article_content = db.Column(db.Text)
    article_format = db.Column(db.Text)
    extraction_version = db.Column(db.Text)
    remarks = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    last_updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), onupdate=db.func.now()
    )

    def __init__(
        self,
        url,
        publisher_id=None,
        in_article_tags=None,
        out_article_tags=None,
        in_article_date=None,
        out_article_date=None,
        links=None,
        article_content=None,
        article_format=None,
        extraction_version=None,
        remarks=None,
    ):
        self.url = url
        if publisher_id:
            self.publisher_id = publisher_id
        if in_article_tags:
            self.in_article_tags = in_article_tags
        if out_article_tags:
            self.out_article_tags = out_article_tags
        if in_article_date:
            self.in_article_date = in_article_date
        if out_article_date:
            self.out_article_date = out_article_date
        if links:
            self.links = links
        if article_content:
            self.article_content = article_content
        if article_format:
            self.article_format = article_format
        if extraction_version:
            self.extraction_version = extraction_version
        if remarks:
            self.remarks = remarks

    def to_dict(self):
        return {
            "article_id": self.article_id,
            "publisher_id": self.publisher_id,
            "url": self.url,
            "in_article_tags": self.in_article_tags,
            "out_article_tags": self.out_article_tags,
            "in_article_date": (
                self.in_article_date.isoformat() if self.in_article_date else None
            ),
            "out_article_date": (
                self.out_article_date.isoformat() if self.out_article_date else None
            ),
            "links": self.links,
            "article_content": self.article_content,
            "article_format": self.article_format,
            "extraction_version": self.extraction_version,
            "remarks": self.remarks,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_updated_at": (
                self.last_updated_at.isoformat() if self.last_updated_at else None
            ),
        }
