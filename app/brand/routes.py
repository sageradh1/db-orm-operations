"""
API Routes for Brand
"""

from flask import request
from flask_restx import Namespace, Resource, fields
from sqlalchemy.exc import SQLAlchemyError

from app.enrichment_simweb.models import EnrichmentSimWeb
from app.extensions import db
from app.logger import app_logger
from app.sentiment.models import Sentiment
from app.utility.utils import is_valid_website

from .models import Brand, BrandUtility

brand_ns = Namespace("brands", description="Brand related operations", validate=True)

brand_model = brand_ns.model(
    "Brand",
    {
        "brand_id": fields.Integer(readonly=True, attribute="brand_id"),
        "name": fields.String(
            required=True,
            description="The name of the brand",
            attribute="name",
        ),
        "website": fields.String(
            description="The website of the brand", unique=True, attribute="website"
        ),
        "contact_name": fields.String(
            description="Contact name of the brand", attribute="contact_name"
        ),
        "contact_email": fields.String(
            description="Contact email of the brand", attribute="contact_email"
        ),
        "contact_phone": fields.String(
            description="Contact phone number of the brand", attribute="contact_phone"
        ),
        "created_at": fields.DateTime(readonly=True, attribute="created_at"),
        "last_updated_at": fields.DateTime(readonly=True, attribute="last_updated_at"),
    },
)


pagination_model = brand_ns.model(
    "Brand Pagination",
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
        "brands": fields.List(
            fields.Nested(brand_model), description="List of brands."
        ),
    },
)


@brand_ns.route("/")
class BrandResourceNoParams(Resource):
    """
    Endpoints related to Brand without id param
    """

    @brand_ns.marshal_with(pagination_model)
    def get(self):
        """Get a list of brands with pagination"""
        try:
            page_number = request.args.get("page", 1, type=int)
            page_size = request.args.get("page_size", 10, type=int)

            # Query brands in descending order by ID
            query = Brand.query.order_by(Brand.brand_id.desc())
            pagination = query.paginate(
                page=page_number, per_page=page_size, error_out=False
            )

            brands = pagination.items
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
                "brands": brands,
            }
        except Exception as e:
            db.session.rollback()
            app_logger.error(f"Error while fetching brands: {str(e)}")
            return {
                "message": f"An error occurred while fetching the brand.{str(e)}"
            }, 500

    @brand_ns.expect(brand_model)
    @brand_ns.response(201, "Brand successfully created.")
    @brand_ns.response(400, "Validation Error.")
    @brand_ns.response(500, "Internal Server Error.")
    def post(self):
        """Create a new brand"""
        data = request.json

        try:
            # Validate website format
            if not is_valid_website(data["website"]):
                return {
                    "message": f"Website format is invalid: {data['website']}."
                }, 400
            existing_brand = Brand.query.filter_by(website=data["website"]).first()
            if existing_brand:
                return {"message": "A brand with this website already exists."}, 409

            new_brand = Brand(
                website=data["website"],
                name=data.get("name"),
                contact_name=data.get("contact_name"),
                contact_email=data.get("contact_email"),
                contact_phone=data.get("contact_phone"),
            )
            db.session.add(new_brand)
            db.session.commit()
            app_logger.info("A new brand successfully created!")
            return {
                "message": "Brand successfully created.",
                "data": new_brand.to_dict(),
            }, 201
        except SQLAlchemyError as e:
            db.session.rollback()
            app_logger.error(f"Error creating brand: {str(e)}")
            return {
                "message": f"An error occurred while creating the brand.  {str(e)}"
            }, 500


@brand_ns.route("/bulk")
class BrandBulkResource(Resource):
    @brand_ns.expect([brand_model])
    @brand_ns.response(201, "Brands successfully created.")
    @brand_ns.response(400, "Validation Error.")
    @brand_ns.response(500, "Internal Server Error.")
    def post(self):
        """Create multiple new brands in bulk"""
        try:
            data = request.json

            if not isinstance(data, list):
                return {"message": "Input data should be a list of brands."}, 400

            # Limit the number of brands that can be submitted in a single request
            MAX_BRANDS = 1000
            if len(data) > MAX_BRANDS:
                return {
                    "message": f"You can submit a maximum of {MAX_BRANDS} brands at a time."
                }, 400

            new_brands = []
            for brand_data in data:
                # Validate website format
                if not is_valid_website(brand_data["website"]):
                    return {
                        "message": f"Website format is invalid: {brand_data['website']}."
                    }, 400

                existing_brand = Brand.query.filter_by(
                    website=brand_data["website"]
                ).first()
                if existing_brand:
                    return {
                        "message": f"A brand with this website already exists: {brand_data['website']}."
                    }, 409

                new_brand = Brand(
                    website=brand_data["website"],
                    name=brand_data.get("name"),
                    contact_name=brand_data.get("contact_name"),
                    contact_email=brand_data.get("contact_email"),
                    contact_phone=brand_data.get("contact_phone"),
                )
                new_brands.append(new_brand)

            db.session.bulk_save_objects(new_brands)
            db.session.commit()

            return {
                "message": f"{len(new_brands)} brands successfully created.",
                "brands": [brand.to_dict() for brand in new_brands],
            }, 201

        except SQLAlchemyError as e:
            db.session.rollback()
            app_logger.error(f"Error creating brands: {str(e)}")
            return {
                "message": f"An error occurred while creating new brands.  {str(e)}"
            }, 500


@brand_ns.route("/<int:brand_id>")
class BrandResourceWithParam(Resource):
    """
    Endpoints related to Brand with id param
    """

    # @brand_ns.marshal_with(brand_model)
    @brand_ns.response(404, "Brand not found.")
    def get(self, brand_id):
        """Get a brand by its ID"""
        try:
            brand = Brand.query.get(brand_id)

            if not brand:
                app_logger.info(f"Brand with id: {brand_id} not found")
                return {"message": f"Brand with id: {brand_id} not found"}, 404

            return {
                "message": "Brand successfully fetched.",
                "data": brand.to_dict(),
            }, 200
        except Exception as e:
            app_logger.error(f"Error getting one brand: {str(e)}")
            return {"message": "An error occurred while getting the brand."}, 500

    @brand_ns.response(204, "Brand successfully updated.")
    @brand_ns.response(400, "Validation Error.")
    @brand_ns.response(500, "Internal Server Error.")
    def put(self, brand_id):
        """Update an existing brand"""
        brand = Brand.query.get(brand_id)
        data = request.json

        try:
            if not brand:
                app_logger.info(f"Brand with id: {brand_id} not found")
                return {"message": f"Brand with id: {brand_id} not found"}, 404

            brand.name = data.get("name", brand.name)
            brand.contact_name = data.get("contact_name", brand.contact_name)
            brand.contact_email = data.get("contact_email", brand.contact_email)
            brand.contact_phone = data.get("contact_phone", brand.contact_phone)

            data_website = data.get("website", None)
            # Conditions such as no brand website or same brand website
            if data_website is None or data_website == brand.name:
                db.session.commit()
                return {
                    "message": "Brand successfully updated.",
                    "data": BrandUtility().to_dict_from_id(brand_id=brand_id),
                }, 200

            # This is the condition when data_website != brand.name:
            # We check if there is already a brand with new brand website
            already_existing_brand_with_new_website = Brand.query.filter_by(
                website=data_website
            ).first()
            associated_sentiments = Sentiment.query.filter_by(
                brand_id=brand.brand_id
            ).all()

            associated_enrichment = EnrichmentSimWeb.query.filter_by(
                brand_id=brand.brand_id
            ).first()

            if already_existing_brand_with_new_website:
                print("Already")
                for each_sentiment in associated_sentiments:
                    each_sentiment.brand_id = (
                        already_existing_brand_with_new_website.brand_id
                    )

                print("Already each_sentiment")

                new_associated_enrichment = EnrichmentSimWeb.query.filter_by(
                    brand_id=already_existing_brand_with_new_website.brand_id
                ).first()

                # if we have existing enrichment for the existing brand, we dont need to do anything
                if new_associated_enrichment:
                    pass

                # but if we dont have existing enrichment, we check if we can provide the enrichment from the brand about to be deleted
                # and associate with the one which will remain
                else:
                    if associated_enrichment:
                        associated_enrichment.brand_id = (
                            already_existing_brand_with_new_website.brand_id
                        )
                db.session.delete(brand)
                db.session.commit()

                print("Now showing results")
                return {
                    "message": "Brand, Sentiments, and Enrichments successfully updated.",
                    "Deleted Brand": brand.to_dict(),
                    "Already Existing Brand": already_existing_brand_with_new_website.to_dict(),
                    "Updated Sentiments": [
                        each_sentiment.to_dict()
                        for each_sentiment in associated_sentiments
                    ],
                }, 200

            else:
                print("Not Already")
                # we create new entry
                if not is_valid_website(data_website):
                    return {
                        "message": f"Website format is invalid: {data_website}."
                    }, 400

                print("Creating new brand")
                new_brand = Brand(
                    website=data_website,
                    name=data.get("name", brand.name),
                    contact_name=data.get("contact_name", brand.contact_name),
                    contact_email=data.get("contact_email", brand.contact_email),
                    contact_phone=data.get("contact_phone", brand.contact_phone),
                )
                db.session.add(new_brand)
                db.session.commit()

                print("Not Already created brand")

                for each_sentiment in associated_sentiments:
                    each_sentiment.brand_id = new_brand.brand_id
                print("Not Already each_sentiment")

                # if we have existing enrichment for the existing brand, we can associate the
                if associated_enrichment:
                    associated_enrichment.brand_id = new_brand.brand_id
                print("Not Already associated_enrichment")

                db.session.delete(brand)
                print("Not Already delete")

                db.session.commit()

                print("Now showing results")
                return {
                    "message": "Brand, Sentiments and Enrichments successfully updated.",
                    "Deleted Brand": brand.to_dict(),
                    "Newly created Brand": new_brand.to_dict(),
                    "Updated Sentiments": [
                        each_sentiment.to_dict()
                        for each_sentiment in associated_sentiments
                    ],
                }, 200

        except Exception as e:
            db.session.rollback()
            app_logger.error(f"Error updating brand {brand_id}: {str(e)}")
            return {
                "message": f"An error occurred while updating the brand.{str(e)}"
            }, 500

    @brand_ns.response(200, "Brand successfully deleted.")
    @brand_ns.response(404, "Brand not found.")
    def delete(self, brand_id):
        """Delete a Brand by its ID"""
        try:
            brand = Brand.query.get(brand_id)

            if not brand:
                app_logger.info(f"Brand with id: {brand_id} not found")
                return {"message": f"Brand with id: {brand_id} not found"}, 404

            db.session.delete(brand)
            db.session.commit()
            return {"message": "Brand successfully deleted."}
        except Exception as e:
            db.session.rollback()
            app_logger.error(f"Error while deleting brand with id {brand_id}: {str(e)}")
            return {
                "message": f"An error occurred while deleting the brand.{str(e)}"
            }, 500
