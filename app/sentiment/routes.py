"""
sentiment_ns Routes for Sentiment
"""

from flask import request
from flask_restx import Namespace, Resource, fields
from sqlalchemy.exc import SQLAlchemyError

from app.article.models import Article
from app.brand.models import Brand
from app.extensions import db
from app.logger import app_logger
from app.publisher.models import Publisher

from .models import Sentiment

sentiment_ns = Namespace("sentiments", description="Sentiment related operations")

sentiment_model = sentiment_ns.model(
    "Sentiment",
    {
        "sentiment_id": fields.Integer(readonly=True),
        "publisher_id": fields.Integer(
            description="The ID of the publisher", required=True
        ),
        "article_id": fields.Integer(
            description="The ID of the article", required=True
        ),
        "brand_id": fields.Integer(description="The ID of the brand", required=True),
        "sentiment_version": fields.String(
            description="Version of the sentiment analysis"
        ),
        "link_source": fields.String(description="Source link of the sentiment"),
        "sentiment": fields.String(description="The sentiment value"),
        "summary": fields.String(description="Summary of the sentiment"),
        "is_manually_verified": fields.Boolean(
            description="Whether the sentiment is manually verified"
        ),
        "remarks": fields.String(description="Additional remarks"),
        "created_at": fields.DateTime(readonly=True),
        "last_updated_at": fields.DateTime(readonly=True),
    },
)

pagination_model = sentiment_ns.model(
    "Pagination",
    {
        "first_page_number": fields.Integer(
            description="The index of the first item on this page."
        ),
        "last_page_number": fields.Integer(
            description="The index of the last item on this page."
        ),
        "total_items": fields.Integer(description="Total number of items available."),
        "total_pages": fields.Integer(description="Total number of pages available."),
        "current_page": fields.Integer(description="The current page number."),
        "sentiments": fields.List(
            fields.Nested(sentiment_model), description="List of sentiments."
        ),
    },
)


@sentiment_ns.route("/")
class SentimentListResource(Resource):
    """
    Endpoints related to Sentiment without ID param
    """

    @sentiment_ns.marshal_list_with(pagination_model)
    def get(self):
        """Get a list of sentiments with pagination"""
        try:
            page_number = request.args.get("page", 1, type=int)
            page_size = request.args.get("page_size", 10, type=int)

            # Query sentiments in descending order by ID
            query = Sentiment.query.order_by(Sentiment.sentiment_id.desc())
            pagination = query.paginate(
                page=page_number, per_page=page_size, error_out=False
            )

            sentiments = pagination.items
            total_items = pagination.total
            total_pages = pagination.pages
            first_page_number = 1
            last_page_number = total_pages

            return {
                "first_page_number": first_page_number,
                "last_page_number": last_page_number,
                "total_items": total_items,
                "total_pages": total_pages,
                "current_page": page_number,
                "sentiments": sentiments,
            }
        except SQLAlchemyError as e:
            db.session.rollback()
            app_logger.error(f"Error while fetching sentiments: {str(e)}")
            return {
                "message": f"An error occurred while fetching the sentiment.{str(e)}"
            }, 500

    @sentiment_ns.expect(sentiment_model)
    @sentiment_ns.response(201, "Sentiment successfully created.")
    def post(self):
        """Create a new sentiment"""
        data = request.json

        try:
            # Publisher should exists before we enrich data for the brand
            publisher = Publisher.query.get(data["publisher_id"])
            if not publisher:
                return {
                    "message": f"Publisher with ID {data['publisher_id']} not found."
                }, 404

            article = Article.query.get(data["article_id"])
            if not article:
                return {
                    "message": f"Article with ID {data['article_id']} not found."
                }, 404

            brand = Brand.query.get(data["brand_id"])
            if not brand:
                return {"message": f"Brand with ID {data['brand_id']} not found."}, 404

            new_sentiment = Sentiment(
                publisher_id=data.get("publisher_id"),
                article_id=data.get("article_id"),
                brand_id=data.get("brand_id"),
                sentiment_version=data.get("sentiment_version"),
                link_source=data.get("link_source"),
                sentiment=data.get("sentiment"),
                summary=data.get("summary"),
                is_manually_verified=data.get("is_manually_verified", False),
                remarks=data.get("remarks", ""),
            )
            db.session.add(new_sentiment)
            # commiting now because new_brand_mention will require sentiment_id
            db.session.commit()

            db.session.commit()
            return {
                "message": "Sentiment successfully created.",
                "sentiment": new_sentiment.to_dict(),
            }, 201
        except SQLAlchemyError as e:
            db.session.rollback()
            app_logger.error(f"Error creating brand: {str(e)}")
            return {
                "message": "An error occurred while creating the brand.",
            }, 500


@sentiment_ns.route("/<int:sentiment_id>")
class SentimentResource(Resource):
    """
    Endpoints related to Sentiment with ID param
    """

    @sentiment_ns.response(404, "Sentiment not found.")
    def get(self, sentiment_id):
        """Get a sentiment by its ID"""
        try:

            sentiment = Sentiment.query.get(sentiment_id)
            if not sentiment:
                app_logger.info(f"Sentiment with id: {sentiment_id} not found")
                return {"message": f"Sentiment with id: {sentiment_id} not found"}, 404
            return {
                "message": "Sentiment successfully fetched.",
                "data": sentiment.to_dict(),
            }, 200
        except SQLAlchemyError as e:
            app_logger.error(f"Error getting one sentiment: {str(e)}")
            return {"message": "An error occurred while getting the sentiment."}, 500

    @sentiment_ns.expect(sentiment_model)
    @sentiment_ns.response(200, "Sentiment successfully updated.")
    @sentiment_ns.response(404, "Sentiment not found.")
    def put(self, sentiment_id):
        """Update a sentiment by its ID"""
        try:
            sentiment = Sentiment.query.get(sentiment_id)

            if not sentiment:
                return {"message": f"Sentiment with id: {sentiment_id} not found"}, 404

            data = request.json

            if data["article_id"]:

                publisher = Publisher.query.get(data["publisher_id"])
                if not publisher:
                    return {
                        "message": f"Publisher with id: {data['publisher_id']} not found"
                    }, 404
                sentiment.publisher_id = data["publisher_id"]

            if data["article_id"]:
                article = Article.query.get(data["article_id"])
                if not article:
                    return {
                        "message": f"Article with id: {data['article_id']} not found"
                    }, 404
                sentiment.article_id = data["article_id"]

            if data["brand_id"]:
                brand = Brand.query.get(data["brand_id"])
                if not brand:
                    return {
                        "message": f"Article with id: {data['brand_id']} not found"
                    }, 404
                sentiment.brand_id = data["brand_id"]

            sentiment.sentiment_version = data.get(
                "sentiment_version", sentiment.sentiment_version
            )
            sentiment.link_source = data.get("link_source", sentiment.link_source)
            sentiment.sentiment = data.get("sentiment", sentiment.sentiment)
            sentiment.summary = data.get("summary", sentiment.summary)
            sentiment.is_manually_verified = data.get(
                "is_manually_verified", sentiment.is_manually_verified
            )
            sentiment.remarks = data.get("remarks", sentiment.remarks)

            # db.session.commit()

            db.session.commit()
            return {
                "message": "Sentiment successfully updated.",
                "sentiment": sentiment.to_dict(),
            }
        except SQLAlchemyError as e:
            db.session.rollback()
            app_logger.error(
                f"Error updating sentiment with id {sentiment_id}: {str(e)}"
            )
            return {
                "message": f"An error occurred while updating the sentiment.{str(e)}"
            }, 500

    @sentiment_ns.response(204, "Sentiment successfully deleted.")
    def delete(self, sentiment_id):
        """Delete a sentiment by its ID"""
        try:
            sentiment = Sentiment.query.get(sentiment_id)

            if not sentiment:
                return {"message": f"Sentiment with id: {sentiment_id} not found"}, 404

            if sentiment.brand_mention:
                db.session.delete(sentiment.brand_mention)

            db.session.delete(sentiment)

            db.session.commit()
            return {"message": "Sentiment successfully deleted."}
        except Exception as e:
            db.session.rollback()
            app_logger.error(
                f"Error while deleting Sentiment with id {sentiment_id}: {str(e)}"
            )
            return {
                "message": f"An error occurred while deleting the Sentiment.{str(e)}"
            }, 500
