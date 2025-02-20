"""
API Routes for Publisher
"""

from flask import request
from flask_restx import Namespace, Resource, fields
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db
from app.logger import app_logger

from .models import Publisher, PublisherUtility

publisher_ns = Namespace(
    "publishers", description="Publisher related operations", validate=True
)

publisher_model = publisher_ns.model(
    "Publisher",
    {
        "publisher_id": fields.Integer(readonly=True, attribute="publisher_id"),
        "name": fields.String(
            required=True, unique=True, description="The name of the publisher"
        ),
        "contact_name": fields.String(
            description="Contact name of the publisher", attribute="contact_name"
        ),
        "contact_email": fields.String(
            description="Contact email of the publisher", attribute="contact_email"
        ),
        "contact_phone": fields.String(
            description="Contact phone number of the publisher",
            attribute="contact_phone",
        ),
        "created_at": fields.DateTime(readonly=True, attribute="created_at"),
        "last_updated_at": fields.DateTime(readonly=True, attribute="last_updated_at"),
    },
)

pagination_model = publisher_ns.model(
    "Pagination",
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
        "publishers": fields.List(
            fields.Nested(publisher_model), description="List of publishers."
        ),
    },
)


@publisher_ns.route("/")
class PublisherResourceNoParams(Resource):
    """
    Endpoints related to Publisher without id param
    """

    @publisher_ns.marshal_with(pagination_model)
    def get(self):
        """Get a list of publishers with pagination"""
        try:
            page_number = request.args.get("page", 1, type=int)
            page_size = request.args.get("page_size", 10, type=int)

            # Query publishers in descending order by ID
            query = Publisher.query.order_by(Publisher.publisher_id.desc())
            pagination = query.paginate(
                page=page_number, per_page=page_size, error_out=False
            )

            publishers = pagination.items
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
                "publishers": publishers,
            }
        except Exception as e:
            db.session.rollback()
            app_logger.error(f"Error while fetching publishers: {str(e)}")
            return {
                "message": f"An error occurred while fetching the publisher.{str(e)}"
            }, 500

    @publisher_ns.expect(publisher_model)
    @publisher_ns.response(201, "Publisher successfully created.")
    @publisher_ns.response(400, "Validation Error.")
    @publisher_ns.response(500, "Internal Server Error.")
    def post(self):
        """Create a new publisher"""
        data = request.json

        try:
            existing_publisher = Publisher.query.filter_by(name=data["name"]).first()
            if existing_publisher:
                return {"message": "A publisher with this name already exists."}, 409

            new_publisher = Publisher(
                name=data["name"],
                contact_name=data.get("contact_name"),
                contact_email=data.get("contact_email"),
                contact_phone=data.get("contact_phone"),
            )
            db.session.add(new_publisher)
            db.session.commit()
            app_logger.info("A new publisher successfully created!")
            return {
                "message": "Publisher successfully created.",
                "data": new_publisher.to_dict(),
            }, 201
        except SQLAlchemyError as e:
            db.session.rollback()
            app_logger.error(f"Error creating publisher: {str(e)}")
            return {"message": "An error occurred while creating the publisher."}, 500


@publisher_ns.route("/<int:publisher_id>")
class PublisherResourceWithParam(Resource):
    """
    Endpoints related to Publisher with id param
    """

    @publisher_ns.response(404, "Publisher not found.")
    def get(self, publisher_id):
        """Get a publisher by its ID"""
        try:
            publisher = Publisher.query.get(publisher_id)

            if not publisher:
                app_logger.info(f"Publisher with id: {publisher_id} not found")
                return {"message": f"Publisher with id: {publisher_id} not found"}, 404

            return {
                "message": "Publisher successfully fetched.",
                "data": publisher.to_dict(),
            }, 200
        except Exception as e:
            app_logger.error(f"Error getting one publisher: {str(e)}")
            return {"message": "An error occurred while getting the publisher."}, 500

    @publisher_ns.response(204, "Publisher successfully updated.")
    @publisher_ns.response(400, "Validation Error.")
    @publisher_ns.response(500, "Internal Server Error.")
    def put(self, publisher_id):
        """Update an existing publisher"""
        publisher = Publisher.query.get(publisher_id)
        data = request.json

        try:
            if not publisher:
                app_logger.info(f"Publisher with id: {publisher_id} not found")
                return {"message": f"Publisher with id: {publisher_id} not found"}, 404

            publisher.name = data.get("name", publisher.name)
            publisher.contact_name = data.get("contact_name", publisher.contact_name)
            publisher.contact_email = data.get("contact_email", publisher.contact_email)
            publisher.contact_phone = data.get("contact_phone", publisher.contact_phone)

            db.session.commit()

            return {
                "message": "Publisher successfully updated.",
                "data": PublisherUtility().to_dict_from_id(publisher_id=publisher_id),
            }, 200
        except Exception as e:
            db.session.rollback()
            app_logger.error(f"Error updating publisher {publisher_id}: {str(e)}")
            return {
                "message": f"An error occurred while updating the publisher.{str(e)}"
            }, 500

    @publisher_ns.response(200, "Publisher successfully deleted.")
    @publisher_ns.response(404, "Publisher not found.")
    def delete(self, publisher_id):
        """Delete a Publisher by its ID"""
        try:
            publisher = Publisher.query.get(publisher_id)

            if not publisher:
                app_logger.info(f"Publisher with id: {publisher_id} not found")
                return {"message": f"Publisher with id: {publisher_id} not found"}, 404

            articles = publisher.articles
            for article in articles:
                db.session.delete(article)
            db.session.delete(publisher)

            db.session.commit()
            return {"message": "Publisher successfully deleted."}
        except Exception as e:
            db.session.rollback()
            app_logger.error(
                f"Error while deleting publisher with id {publisher_id}: {str(e)}"
            )
            return {
                "message": f"An error occurred while deleting the publisher.{str(e)}"
            }, 500
