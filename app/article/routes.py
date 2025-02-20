from datetime import datetime

from flask import jsonify, request
from flask_restx import Namespace, Resource, fields
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db
from app.logger import app_logger
from app.publisher.models import Publisher

from .models import Article

article_ns = Namespace("articles", description="Article related operations")

article_model = article_ns.model(
    "Article",
    {
        "article_id": fields.Integer(readonly=True),
        "publisher_id": fields.Integer(
            description="The publisher ID associated with the article", required=True
        ),
        "url": fields.String(required=True, description="The URL of the article"),
        "in_article_tags": fields.String(description="Tags used inside the article"),
        "out_article_tags": fields.String(description="Tags used outside the article"),
        "in_article_date": fields.DateTime(
            description="Date when the article was included"
        ),
        "out_article_date": fields.DateTime(
            description="Date when the article was removed"
        ),
        "links": fields.String(description="_additional links related to the article"),
        "article_content": fields.String(description="Content of the article"),
        "article_format": fields.String(description="Format of the article"),
        "extraction_version": fields.String(
            description="Version of the extraction process"
        ),
        "remarks": fields.String(description="_additional remarks about the article"),
        "created_at": fields.DateTime(readonly=True),
        "last_updated_at": fields.DateTime(readonly=True),
    },
)

pagination_model = article_ns.model(
    "Article Pagination",
    {
        "first_page_number": fields.Integer(
            description="The index of the first item on this page."
        ),
        "last_page_number": fields.Integer(
            description="The index of the last item on this page."
        ),
        "total_items": fields.Integer(description="_total number of items available."),
        "total_pages": fields.Integer(description="_total number of pages available."),
        "current_page": fields.Integer(description="The current page number."),
        "articles": fields.List(
            fields.Nested(article_model), description="List of articles."
        ),
    },
)


@article_ns.route("/")
class ArticleListResource(Resource):
    @article_ns.marshal_list_with(pagination_model)
    def get(self):
        """Get a list of articles with pagination"""
        try:
            page_number = request.args.get("page", 1, type=int)
            page_size = request.args.get("page_size", 10, type=int)

            # Query articles in descending order by ID
            query = Article.query.order_by(Article.article_id.desc())
            pagination = query.paginate(
                page=page_number, per_page=page_size, error_out=False
            )

            articles = pagination.items
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
                "articles": articles,
            }
        except Exception as e:
            db.session.rollback()
            app_logger.error(f"Error while fetching articles: {str(e)}")
            return {
                "message": f"An error occurred while fetching the article.{str(e)}"
            }, 500

    @article_ns.expect(article_model)
    @article_ns.response(201, "Article successfully created.")
    def post(self):
        """Create a new article"""
        try:
            data = request.json

            in_article_date = None
            out_article_date = None

            if data.get("in_article_date") not in (None, ""):
                in_article_date = datetime.strptime(
                    data["in_article_date"], "%Y-%m-%dT%H:%M:%S"
                )

            if data.get("out_article_date") not in (None, ""):
                out_article_date = datetime.strptime(
                    data["out_article_date"], "%Y-%m-%dT%H:%M:%S"
                )
            

            publisher_id = data.get("publisher_id")
            publisher = Publisher.query.get(publisher_id)

            if not publisher:
                app_logger.info(f"Publisher with id: {publisher_id} not found")
                return {"message": f"Publisher with id: {publisher_id} not found"}, 404

            article = Article.query.filter_by(url=data["url"]).first()
            if article:
                return {
                    "message": f"Another with the same url: {data['url']} exists."
                }, 409

            new_article = Article(
                url=data["url"],
                publisher_id=publisher_id,
                in_article_tags=data.get("in_article_tags", ""),
                out_article_tags=data.get("out_article_tags", ""),
                in_article_date=in_article_date,
                out_article_date=out_article_date,
                links=data.get("links", ""),
                article_content=data.get("article_content", ""),
                article_format=data.get("article_format", ""),
                extraction_version=data.get("extraction_version", ""),
                remarks=data.get("remarks", ""),
            )
            db.session.add(new_article)
            db.session.commit()
            return {
                "message": "Article successfully created.",
                "article": new_article.to_dict(),
            }, 201

        except SQLAlchemyError as e:
            db.session.rollback()
            app_logger.error(f"Error creating article: {str(e)}")
            return {"message": f"An error occurred while creating a new article.  {str(e)}"}, 500

@article_ns.route("/bulk")
class ArticleBulkResource(Resource):
    @article_ns.expect([article_model])
    @article_ns.response(201, "Articles successfully created.")
    @article_ns.response(400, "Validation Error.")
    @article_ns.response(500, "Internal Server Error.")
    def post(self):
        """Create multiple new articles in bulk"""
        try:
            data = request.json

            if not isinstance(data, list):
                return {"message": "Input data should be a list of articles."}, 400
            
            # Limit the number of articles that can be submitted in a single request
            MAX_ARTICLES = 1000
            if len(data) > MAX_ARTICLES:
                return {
                    "message": f"You can submit a maximum of {MAX_ARTICLES} articles at a time."
                }, 400

            new_articles = []
            for article_data in data:
                in_article_date = None
                out_article_date = None

                if article_data.get("in_article_date") not in (None, ""):
                    in_article_date = datetime.strptime(
                        article_data["in_article_date"], "%Y-%m-%dT%H:%M:%S"
                    )

                if article_data.get("out_article_date") not in (None, ""):
                    out_article_date = datetime.strptime(
                        article_data["out_article_date"], "%Y-%m-%dT%H:%M:%S"
                    )

                publisher_id = article_data.get("publisher_id")
                publisher = Publisher.query.get(publisher_id)

                if not publisher:
                    app_logger.info(f"Publisher with id: {publisher_id} not found")
                    return {"message": f"Publisher with id: {publisher_id} not found"}, 404

                article = Article.query.filter_by(url=article_data["url"]).first()
                if article:
                    return {
                        "message": f"Another article with the same URL: {article_data['url']} exists."
                    }, 409

                new_article = Article(
                    url=article_data["url"],
                    publisher_id=publisher_id,
                    in_article_tags=article_data.get("in_article_tags", ""),
                    out_article_tags=article_data.get("out_article_tags", ""),
                    in_article_date=in_article_date,
                    out_article_date=out_article_date,
                    links=article_data.get("links", ""),
                    article_content=article_data.get("article_content", ""),
                    article_format=article_data.get("article_format", ""),
                    extraction_version=article_data.get("extraction_version", ""),
                    remarks=article_data.get("remarks", ""),
                )
                new_articles.append(new_article)

            db.session.bulk_save_objects(new_articles)
            db.session.commit()

            return {
                "message": f"{len(new_articles)} articles successfully created.",
                "articles": [article.to_dict() for article in new_articles],
            }, 201

        except SQLAlchemyError as e:
            db.session.rollback()
            app_logger.error(f"Error creating articles: {str(e)}")
            return {"message": f"An error occurred while creating new articles. {str(e)}"}, 500


@article_ns.route("/<int:article_id>")
class ArticleResource(Resource):
    @article_ns.response(404, "Article not found.")
    def get(self, article_id):
        """Get an article by its ID"""
        try:

            article = Article.query.get(article_id)

            if not article:
                app_logger.info(f"Article with id: {article_id} not found")
                return {"message": f"Article with id: {article_id} not found"}, 404

            return {
                "message": "Article successfully fetched.",
                "data": article.to_dict(),
            }, 200
        except Exception as e:
            app_logger.error(f"Error getting one article: {str(e)}")
            return {"message": "An error occurred while getting the article."}, 500

    @article_ns.expect(article_model)
    @article_ns.response(200, "Article successfully updated.")
    def put(self, article_id):
        """Update an article by its ID"""
        try:
            article = Article.query.get(article_id)

            if not article:
                app_logger.info(f"Article with id: {article_id} not found")
                return {"message": f"Article with id: {article_id} not found"}, 404

            data = request.json

            article_existing_url = Article.query.filter_by(url=data["url"]).first()

            if (
                article_existing_url
                and article_existing_url.article_id != article.article_id
            ):
                return {
                    "message": f"Article with url: {data['url']} already exists"
                }, 409

            if data["publisher_id"]:
                publisher = Publisher.query.get(data["publisher_id"])
                if not publisher:
                    app_logger.info(
                        f"Publisher with id: {data['publisher_id']} not found"
                    )
                    return {
                        "message": f"Publisher with id: {data['publisher_id']} not found"
                    }, 404

            for key, value in data.items():
                if key == "in_article_date":
                    value = datetime.strptime(data["in_article_date"], "%Y-%m-%d")
                elif key == "out_article_date":
                    value = datetime.strptime(data["in_article_date"], "%Y-%m-%d")
                setattr(article, key, value)

            db.session.commit()
            return {
                "message": "Article successfully updated.",
                "article": article.to_dict(),
            }
        except Exception as e:
            db.session.rollback()
            app_logger.error(f"Error updating article with id {article_id}: {str(e)}")
            return {
                "message": f"An error occurred while updating the article.{str(e)}"
            }, 500

    @article_ns.response(200, "Article successfully deleted.")
    @article_ns.response(404, "Article not found.")
    def delete(self, article_id):
        """Delete an article by its ID"""
        try:
            article = Article.query.get(article_id)

            if not article:
                return {"message": f"Article with id: {article_id} not found"}, 404

            db.session.delete(article)

            db.session.commit()
            return {"message": "Article successfully deleted."}
        except Exception as e:
            db.session.rollback()
            app_logger.error(
                f"Error while deleting article with id {article_id}: {str(e)}"
            )
            return {
                "message": f"An error occurred while deleting the article.{str(e)}"
            }, 500
