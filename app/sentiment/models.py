import enum

from app.extensions import db


class LicensabilityEnum(enum.Enum):
    unlikely = "unlikely"
    veryunlikely = "veryunlikely"
    likely = "likely"
    verylikely = "verylikely"
    other = "other"


class SentimentEnum(enum.Enum):
    negative = "negative"
    neutral = "neutral"
    positive = "positive"
    other = "other"


class UrlSourceEnum(enum.Enum):
    parsed = "parsed"
    generated = "generated"
    google_url_tool = "google_url_tool"
    apollo = "apollo"
    notfound = "notfound"
    other = "other"


class Sentiment(db.Model):
    __tablename__ = "sentiments"

    sentiment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    publisher_id = db.Column(
        db.Integer, db.ForeignKey("publishers.publisher_id", ondelete="CASCADE")
    )
    publisher = db.relationship("Publisher", back_populates="sentiments")

    article_id = db.Column(
        db.Integer, db.ForeignKey("articles.article_id", ondelete="CASCADE")
    )
    article = db.relationship("Article", back_populates="sentiments")

    brand_id = db.Column(
        db.Integer,
        db.ForeignKey("brands.brand_id", ondelete="CASCADE"),
        nullable=False,
    )
    brand = db.relationship("Brand", back_populates="sentiments")

    batch_id = db.Column(
        db.Text, db.ForeignKey("batch_statuses.batch_id"), nullable=True
    )
    batch = db.relationship("BatchStatus", backref="sentiments")

    sentiment_version = db.Column(db.Text)
    link_source = db.Column(db.Enum(UrlSourceEnum), nullable=True)
    sentiment = db.Column(db.Enum(SentimentEnum), nullable=True)
    summary = db.Column(db.Text)
    licensability = db.Column(db.Enum(LicensabilityEnum), nullable=True)
    is_manually_verified = db.Column(db.Boolean, default=False)
    remarks = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    last_updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        onupdate=db.func.now(),
        nullable=False,
    )

    def __init__(
        self,
        publisher_id=None,
        article_id=None,
        brand_id=None,
        sentiment_version=None,
        link_source=None,
        sentiment=None,
        summary=None,
        licensability=None,
        is_manually_verified=False,
        remarks=None,
    ):
        if publisher_id:
            self.publisher_id = publisher_id
        if article_id:
            self.article_id = article_id
        if brand_id:
            self.brand_id = brand_id
        if sentiment_version:
            self.sentiment_version = sentiment_version
        if link_source:
            self.link_source = link_source
        if sentiment:
            self.sentiment = sentiment
        if summary:
            self.summary = summary
        if licensability:
            self.licensability = licensability
        self.is_manually_verified = is_manually_verified
        if remarks:
            self.remarks = remarks

    def to_dict(self):
        return {
            "sentiment_id": self.sentiment_id,
            "publisher_id": self.publisher_id,
            "article_id": self.article_id,
            "brand_id": self.brand_id,
            "sentiment_version": self.sentiment_version,
            "link_source": self.link_source,
            "sentiment": self.sentiment,
            "licensability": self.licensability,
            "summary": self.summary,
            "is_manually_verified": self.is_manually_verified,
            "remarks": self.remarks,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_updated_at": (
                self.last_updated_at.isoformat() if self.last_updated_at else None
            ),
        }
