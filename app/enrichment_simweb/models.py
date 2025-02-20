"""
Enrichment model
"""

# pylint: disable=too-many-arguments


from decimal import Decimal

from app.enrichment_simweb.utils import EnrichmentSimWebUtility
from app.extensions import db
from app.utility.utils import camel_to_snake


class EnrichmentSimWeb(db.Model):
    """
    DB entity for Enrichment Table for SimilarWeb data
    returns: SQLAlchemy DB Model Object in EnrichmentSimWeb form
    Consideration: Any changes in fields here might require change in utilities
    """

    __tablename__ = "enrichments_simweb"

    enrichment_sim_web_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    brand_id = db.Column(
        db.Integer,
        db.ForeignKey("brands.brand_id", ondelete="CASCADE"),
        nullable=False,
    )
    # to ensure cascade delete happens properly
    brand = db.relationship(
        "Brand", backref=db.backref(__tablename__, passive_deletes=True)
    )

    enrichment_status = db.Column(db.Text, nullable=True)
    rank = db.Column(db.BigInteger, nullable=True)
    industry = db.Column(db.Text, nullable=True)
    ppc_spend = db.Column(db.Numeric, nullable=True)
    company_name = db.Column(db.Text, nullable=True)
    annual_revenue = db.Column(db.Text, nullable=True)
    online_revenue = db.Column(db.Text, nullable=True)
    employees = db.Column(db.Text, nullable=True)
    hq_country = db.Column(db.Text, nullable=True)
    hq_state = db.Column(db.Text, nullable=True)
    hq_city = db.Column(db.Text, nullable=True)
    hq_address = db.Column(db.Text, nullable=True)
    hq_postal_code = db.Column(db.Text, nullable=True)
    phone_number = db.Column(db.Text, nullable=True)
    email_address = db.Column(db.Text, nullable=True)
    total_funding = db.Column(db.Text, nullable=True)
    monthly_transactions = db.Column(db.Text, nullable=True)
    company_linkedin_url = db.Column(db.Text, nullable=True)
    top_country = db.Column(db.Text, nullable=True)
    monthly_visits = db.Column(db.Text, nullable=True)
    average_monthly_visits = db.Column(db.Text, nullable=True)
    mom_traffic_change = db.Column(db.Numeric, nullable=True)
    yoy_traffic_change = db.Column(db.Numeric, nullable=True)
    two_years_visits_trend = db.Column(db.Text, nullable=True)
    unique_visitors = db.Column(db.Text, nullable=True)
    mom_unique_visitors_change = db.Column(db.Numeric, nullable=True)
    yoy_unique_visitors_change = db.Column(db.Numeric, nullable=True)
    two_years_unique_visitors_trend = db.Column(db.Text, nullable=True)
    desktop_traffic_share = db.Column(db.Numeric, nullable=True)
    mobile_traffic_share = db.Column(db.Numeric, nullable=True)
    two_years_page_views_trend = db.Column(db.Text, nullable=True)
    monthly_desktop_traffic = db.Column(db.Text, nullable=True)
    mom_desktop_traffic_change = db.Column(db.Numeric, nullable=True)
    yoy_desktop_traffic_change = db.Column(db.Numeric, nullable=True)
    desktop_unique_visitors = db.Column(db.Text, nullable=True)
    mom_desktop_unique_visitors_change = db.Column(db.Numeric, nullable=True)
    yoy_desktop_unique_visitors_change = db.Column(db.Numeric, nullable=True)
    mobile_web_monthly_traffic = db.Column(db.Text, nullable=True)
    mom_mobile_web_traffic_change = db.Column(db.Numeric, nullable=True)
    yoy_mobile_web_traffic_change = db.Column(db.Numeric, nullable=True)
    mobile_web_unique_visitors = db.Column(db.Text, nullable=True)
    mom_mobile_web_unique_visitors_change = db.Column(db.Numeric, nullable=True)
    yoy_mobile_web_unique_visitors_change = db.Column(db.Numeric, nullable=True)
    direct_traffic_share = db.Column(db.Numeric, nullable=True)
    email_share = db.Column(db.Numeric, nullable=True)
    referrals_share = db.Column(db.Numeric, nullable=True)
    social_share = db.Column(db.Numeric, nullable=True)
    organic_search_share = db.Column(db.Numeric, nullable=True)
    paid_search_share = db.Column(db.Numeric, nullable=True)
    display_ads_traffic_share = db.Column(db.Numeric, nullable=True)
    direct_traffic = db.Column(db.Text, nullable=True)
    mom_direct_traffic_change = db.Column(db.Numeric, nullable=True)
    yoy_direct_traffic_change = db.Column(db.Numeric, nullable=True)
    two_years_direct_visits_trend = db.Column(db.Text, nullable=True)
    email_visits = db.Column(db.Text, nullable=True)
    mom_email_visits_change = db.Column(db.Numeric, nullable=True)
    yoy_email_visits_change = db.Column(db.Numeric, nullable=True)
    two_years_mail_visits_trend = db.Column(db.Text, nullable=True)
    referral_visits = db.Column(db.Text, nullable=True)
    mom_referrals_visits_change = db.Column(db.Numeric, nullable=True)
    yoy_referrals_visits_change = db.Column(db.Numeric, nullable=True)
    two_years_referrals_visits_trend = db.Column(db.Text, nullable=True)
    social_visits = db.Column(db.Text, nullable=True)
    mom_social_visits_change = db.Column(db.Numeric, nullable=True)
    yoy_social_visits_change = db.Column(db.Numeric, nullable=True)
    two_years_social_visits_trend = db.Column(db.Text, nullable=True)
    organic_search_visits = db.Column(db.Text, nullable=True)
    mom_organic_search_change = db.Column(db.Numeric, nullable=True)
    yoy_organic_search_change = db.Column(db.Numeric, nullable=True)
    two_years_organic_search_visits_trend = db.Column(db.Text, nullable=True)
    paid_search_visits = db.Column(db.Text, nullable=True)
    mom_paid_search_change = db.Column(db.Numeric, nullable=True)
    yoy_paid_search_change = db.Column(db.Numeric, nullable=True)
    two_years_paid_search_visits_trend = db.Column(db.Text, nullable=True)
    display_ad_traffic = db.Column(db.Text, nullable=True)
    mom_display_traffic_change = db.Column(db.Numeric, nullable=True)
    yoy_display_visits_change = db.Column(db.Numeric, nullable=True)
    two_years_display_ads_visits_trend = db.Column(db.Text, nullable=True)
    international_visits = db.Column(db.Text, nullable=True)
    international_visits_share = db.Column(db.Numeric, nullable=True)
    male_share = db.Column(db.Numeric, nullable=True)
    female_share = db.Column(db.Numeric, nullable=True)
    age1824 = db.Column(db.Numeric, nullable=True)
    age2534 = db.Column(db.Numeric, nullable=True)
    age3544 = db.Column(db.Numeric, nullable=True)
    age4554 = db.Column(db.Numeric, nullable=True)
    age5564 = db.Column(db.Numeric, nullable=True)
    age65 = db.Column(db.Numeric, nullable=True)
    visit_duration = db.Column(db.Text, nullable=True)
    monthly_visits_per_visitor = db.Column(db.Numeric, nullable=True)
    pages_per_visit = db.Column(db.Numeric, nullable=True)
    total_page_views = db.Column(db.Text, nullable=True)
    mom_total_page_views_change = db.Column(db.Numeric, nullable=True)
    yoy_total_page_views_change = db.Column(db.Numeric, nullable=True)
    bounce_rate = db.Column(db.Numeric, nullable=True)
    desktop_visit_duration = db.Column(db.Text, nullable=True)
    desktop_pages_per_visit = db.Column(db.Numeric, nullable=True)
    desktop_total_page_views = db.Column(db.Text, nullable=True)
    mom_desktop_page_views_change = db.Column(db.Numeric, nullable=True)
    yoy_desktop_page_views_change = db.Column(db.Numeric, nullable=True)
    desktop_bounce_rate = db.Column(db.Numeric, nullable=True)
    mobile_web_visit_duration = db.Column(db.Text, nullable=True)
    mobile_web_pages_per_visit = db.Column(db.Numeric, nullable=True)
    mobile_web_total_page_views = db.Column(db.Text, nullable=True)
    mom_mobile_web_page_views_change = db.Column(db.Numeric, nullable=True)
    yoy_mobile_web_page_views_change = db.Column(db.Numeric, nullable=True)
    mobile_web_bounce_rate = db.Column(db.Numeric, nullable=True)

    similarweb_revenue_estimate = db.Column(db.BigInteger, nullable=True)
    employee_count_revenue_estimate = db.Column(db.BigInteger, nullable=True)
    web_traffic_revenue_estimate = db.Column(db.BigInteger, nullable=True)
    company_revenue_estimate = db.Column(db.BigInteger, nullable=True)
    online_revenue_estimate = db.Column(db.BigInteger, nullable=True)
    ad_spend_estimate = db.Column(db.BigInteger, nullable=True)
    ip_ad_spend_estimate = db.Column(db.BigInteger, nullable=True)
    licensing_opportunity_estimate = db.Column(db.BigInteger, nullable=True)
    summary_industry_category = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    last_updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), onupdate=db.func.now()
    )

    def __init__(self, enrichment_data=None):
        if not enrichment_data or "brand_id" not in enrichment_data:
            raise ValueError("Missing required field: 'brand_id'")

        initialization_att = EnrichmentSimWebUtility().get_initialization_attributes()
        for key in initialization_att:
            if key in enrichment_data:
                setattr(self, key, enrichment_data[key])

    def extract_column_name(self, input_string, table_name):
        """
        Extract the column name from a string of the format 'table_name.column_name'.

        Args:
            input_string (str): The input string in the format 'table_name.column_name'.
            table_name (str): The table name to match and extract the column name.

        Returns:
            str: The column name if it matches the table name; otherwise, an empty string.
        """
        # Check if the input_string starts with the table_name followed by a dot
        if input_string.startswith(f"{table_name}."):
            # Extract and return the column name part
            return input_string[len(table_name) + 1 :]
        return ""

    # pylint: disable=no-value-for-parameter
    def get_all_columns(self):
        """
        To get list of columns in camelCase from already instantiated EnrichmentSimWeb object
        """
        return [
            self.extract_column_name(column) for column in self.__table__.columns
        ]  # pylint: disable=no-value-for-parameter

    def to_dict(self):
        """
        To convert class object to required python dictionary
        returns: EnrichmentSimWeb in python dictionary
        """
        all_attrs = EnrichmentSimWebUtility().get_initialization_attributes()

        response_data = {}

        for key in all_attrs:
            value = getattr(self, key)

            if isinstance(value, Decimal):
                value = float(value)
            elif isinstance(value, db.Column):
                value = None
            elif value is None:
                value = ""

            response_data[f"{(key)}"] = value

        response_data["created_at"] = (
            self.created_at.isoformat() if self.created_at else None
        )
        response_data["last_updated_at"] = (
            self.last_updated_at.isoformat() if self.last_updated_at else None
        )
        response_data["enrichment_sim_web_id"] = (
            self.enrichment_sim_web_id if self.enrichment_sim_web_id else None
        )

        return response_data
