"""
API Routes for EnrichmentSimWeb
"""

from collections import defaultdict

from flask import request
from flask_restx import Namespace, Resource, fields
from sqlalchemy.exc import SQLAlchemyError

from app.brand.models import Brand
from app.extensions import db
from app.logger import app_logger
from app.utility.utils import camel_to_snake

from .models import EnrichmentSimWeb
from .utils import EnrichmentSimWebUtility

enrichment_sim_web_ns = Namespace(
    "enrichmentsSim_web",
    description="EnrichmentSimWeb related operations",
    validate=True,
)

enrichment_sim_web_model = enrichment_sim_web_ns.model(
    "EnrichmentSimWeb",
    # not adding all the attributes here because mapping of keys is handled where needed
    {
        "enrichment_sim_web_id": fields.Integer(
            readonly=True, attribute="enrichment_sim_web_id"
        ),
        "brand_id": fields.Integer(
            required=True,
            description="The name of the enrichment_sim_web",
            attribute="brand_id",
        ),
        "enrichment_status": fields.String(
            attribute="enrichment_status",
        ),
        "rank": fields.Integer(attribute="rank"),
        "ppc_spend": fields.Float(
            attribute="ppc_spend",
        ),
        "created_at": fields.DateTime(readonly=True, attribute="created_at"),
        "last_updated_at": fields.DateTime(readonly=True, attribute="updatedAt"),
    },
)


pagination_model = enrichment_sim_web_ns.model(
    "EnrichmentSimWeb Pagination",
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
        "enrichment_sim_webs": fields.List(
            fields.Nested(enrichment_sim_web_model),
            description="List of enrichment_sim_webs.",
        ),
    },
)


@enrichment_sim_web_ns.route("/")
class EnrichmentSimWebResourceNoParams(Resource):
    """
    Endpoints related to EnrichmentSimWeb without id param
    """

    # @enrichment_sim_web_ns.marshal_with(pagination_model)
    def get(self):
        """Get a list of enrichment_sim_webs with pagination"""
        try:
            page_number = request.args.get("page", 1, type=int)
            page_size = request.args.get("page_size", 10, type=int)

            # Query enrichment_sim_webs in descending order by ID
            query = EnrichmentSimWeb.query.order_by(
                EnrichmentSimWeb.enrichment_sim_web_id.desc()
            )
            pagination = query.paginate(
                page=page_number, per_page=page_size, error_out=False
            )

            enrichment_sim_webs = pagination.items
            enrichment_sim_webs = [item.to_dict() for item in enrichment_sim_webs]
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
                "enrichment_sim_webs": enrichment_sim_webs,
            }
        except Exception as e:
            db.session.rollback()
            app_logger.error(f"Error while fetching enrichment_sim_webs: {str(e)}")
            return {
                "message": f"An error occurred while fetching the enrichment_sim_web.{str(e)}"
            }, 500

    @enrichment_sim_web_ns.expect(enrichment_sim_web_model)
    @enrichment_sim_web_ns.response(201, "EnrichmentSimWeb successfully created.")
    @enrichment_sim_web_ns.response(400, "Validation Error.")
    @enrichment_sim_web_ns.response(500, "Internal Server Error.")
    def post(self):
        """Create a new enrichment_sim_web"""
        data = request.json

        try:
            # Brand should exists before we enrich data for the brand
            brand = Brand.query.filter_by(website=data["website"]).first()
            if not brand:
                return {"message": f"Brand with ID {data['website']} not found."}, 404

            # If Enrichment exists, we should update it not create it
            existing_enrichment_sim_web = EnrichmentSimWeb.query.filter_by(
                website=data["website"]
            ).first()
            if existing_enrichment_sim_web:
                return {
                    "message": "A enrichment_sim_web with this website already exists. Please update the relevant enrichment entry."
                }, 409

            initialization_attrs = (
                EnrichmentSimWebUtility().get_initialization_attributes()
            )

            enrichment_data = defaultdict(dict)

            for x in initialization_attrs:
                # to check conversion of keys
                # camel_to_snake_list.append([x, camel_to_snake(x)])
                if x in data.keys():
                    enrichment_data[f"{x}"] = data[f"{x}"]

            new_enrichment_sim_web = EnrichmentSimWeb(enrichment_data=enrichment_data)
            db.session.add(new_enrichment_sim_web)
            db.session.commit()
            app_logger.info("A new EnrichmentSimWeb entry successfully created!")
            return {
                "message": "EnrichmentSimWeb entry successfully created.",
                "data": new_enrichment_sim_web.to_dict(),
            }, 201
        except SQLAlchemyError as e:
            db.session.rollback()
            app_logger.error(f"Error creating enrichment_sim_web: {str(e)}")
            return {
                "message": f"An error occurred while creating the enrichment_sim_web.{str(e)}"
            }, 500

@enrichment_sim_web_ns.route("/bulk")
class EnrichmentSimWebBulkResource(Resource):
    @enrichment_sim_web_ns.expect([enrichment_sim_web_model])
    @enrichment_sim_web_ns.response(201, "EnrichmentSimWeb entries successfully created.")
    @enrichment_sim_web_ns.response(400, "Validation Error.")
    @enrichment_sim_web_ns.response(500, "Internal Server Error.")
    def post(self):
        """Create multiple new enrichment_sim_webs in bulk"""
        try:
            data = request.json

            if not isinstance(data, list):
                return {"message": "Input data should be a list of enrichment_sim_webs."}, 400
            
            # Limit the number of enrichment_sim_webs that can be submitted in a single request
            MAX_ENRICHMENT_SIM_WEBS = 100
            if len(data) > MAX_ENRICHMENT_SIM_WEBS:
                return {
                    "message": f"You can submit a maximum of {MAX_ENRICHMENT_SIM_WEBS} enrichment_sim_webs at a time."
                }, 400

            new_enrichment_sim_webs = []
            for item_data in data:
                # Check if the brand exists
                brand = Brand.query.filter_by(website=item_data["website"]).first()
                if not brand:
                    return {"message": f"Brand with ID {item_data['website']} not found."}, 404

                # Check if enrichment already exists
                existing_enrichment_sim_web = EnrichmentSimWeb.query.filter_by(
                    website=item_data["website"]
                ).first()
                if existing_enrichment_sim_web:
                    return {
                        "message": f"An enrichment_sim_web with website {item_data['website']} already exists. Please update the relevant entry."
                    }, 409

                initialization_attrs = EnrichmentSimWebUtility().get_initialization_attributes()
                enrichment_data = defaultdict(dict)

                for x in initialization_attrs:
                    if x in item_data.keys():
                        enrichment_data[f"{x}"] = item_data[f"{x}"]

                new_enrichment_sim_web = EnrichmentSimWeb(enrichment_data=enrichment_data)
                new_enrichment_sim_webs.append(new_enrichment_sim_web)

            db.session.bulk_save_objects(new_enrichment_sim_webs)
            db.session.commit()

            return {
                "message": f"{len(new_enrichment_sim_webs)} enrichment_sim_web entries successfully created.",
                "enrichment_sim_webs": [item.to_dict() for item in new_enrichment_sim_webs],
            }, 201

        except SQLAlchemyError as e:
            db.session.rollback()
            app_logger.error(f"Error creating enrichment_sim_web entries: {str(e)}")
            return {"message": f"An error occurred while creating new enrichment_sim_web entries.  {str(e)}"}, 500


@enrichment_sim_web_ns.route("/<int:enrichment_sim_web_id>")
class EnrichmentSimWebResourceWithParam(Resource):
    """
    Endpoints related to EnrichmentSimWeb with id param
    """

    # @enrichment_sim_web_ns.marshal_with(enrichment_sim_web_model)
    @enrichment_sim_web_ns.response(404, "EnrichmentSimWeb not found.")
    def get(self, enrichment_sim_web_id):
        """Get a enrichment_sim_web by its ID"""
        try:
            enrichment_sim_web: EnrichmentSimWeb = EnrichmentSimWeb.query.get(
                enrichment_sim_web_id
            )

            if not enrichment_sim_web:
                app_logger.info(
                    f"EnrichmentSimWeb with id: {enrichment_sim_web_id} not found"
                )
                return {
                    "message": f"EnrichmentSimWeb with id: {enrichment_sim_web_id} not found"
                }, 404

            return {
                "message": "EnrichmentSimWeb successfully fetched.",
                "data": enrichment_sim_web.to_dict(),
            }, 200
        except Exception as e:
            app_logger.error(f"Error getting one enrichment_sim_web: {str(e)}")
            return {
                "message": "An error occurred while getting the enrichment_sim_web."
            }, 500

    @enrichment_sim_web_ns.response(204, "EnrichmentSimWeb successfully updated.")
    @enrichment_sim_web_ns.response(400, "Validation Error.")
    @enrichment_sim_web_ns.response(500, "Internal Server Error.")
    def put(self, enrichment_sim_web_id):
        """Update an existing enrichment_sim_web"""
        enrichment_sim_web = EnrichmentSimWeb.query.get(enrichment_sim_web_id)
        data = request.json

        try:
            if not enrichment_sim_web:
                app_logger.error(
                    f"EnrichmentSimWeb with id: {enrichment_sim_web_id} not found"
                )
                return {
                    "message": f"EnrichmentSimWeb with id: {enrichment_sim_web_id} not found"
                }, 404

            # New Brand with the brand_id should exists before update the brand
            brand = Brand.query.filter_by(brand_id=data["brand_id"]).first()
            if not brand:
                return {"message": f"Brand with ID {data['brand_id']} not found."}, 404

            if (
                "created_at" in data
                or "last_updated_at" in data
                or "enrichment_sim_web_id" in data
            ):
                return {
                    "message": "Fields like created_at, last_updated_at and enrichment_sim_web_id cannot be changed."
                }, 403

            initialization_attrs = (
                EnrichmentSimWebUtility().get_initialization_attributes()
            )

            for x in initialization_attrs:
                if x in data.keys():
                    setattr(enrichment_sim_web, x, data[camel_to_snake(x)])

            db.session.commit()

            return {
                "message": "EnrichmentSimWeb successfully updated.",
                "data": enrichment_sim_web.to_dict(),
            }, 200
        except Exception as e:
            db.session.rollback()
            app_logger.error(
                f"Error updating enrichment_sim_web {enrichment_sim_web_id}: {str(e)}"
            )
            return {
                "message": f"An error occurred while updating the enrichment_sim_web.{str(e)}"
            }, 500

    @enrichment_sim_web_ns.response(200, "EnrichmentSimWeb successfully deleted.")
    @enrichment_sim_web_ns.response(404, "EnrichmentSimWeb not found.")
    def delete(self, enrichment_sim_web_id):
        """Delete a EnrichmentSimWeb by its ID"""
        try:
            enrichment_sim_web = EnrichmentSimWeb.query.get(enrichment_sim_web_id)

            if not enrichment_sim_web:
                app_logger.info(
                    f"EnrichmentSimWeb with id: {enrichment_sim_web_id} not found"
                )
                return {
                    "message": f"EnrichmentSimWeb with id: {enrichment_sim_web_id} not found"
                }, 404

            db.session.delete(enrichment_sim_web)
            db.session.commit()
            return {"message": "EnrichmentSimWeb successfully deleted."}
        except Exception as e:
            db.session.rollback()
            app_logger.error(
                f"Error while deleting enrichment_sim_web with id {enrichment_sim_web_id}: {str(e)}"
            )
            return {
                "message": f"An error occurred while deleting the enrichment_sim_web.{str(e)}"
            }, 500
