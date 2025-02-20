"""
Extra Utilities for SimilarWeb's Enrichment Model
"""


class EnrichmentSimWebUtility:
    """
    Extra Utilities for SimilarWeb's Enrichment Model
    """

    all_attributes = [
        "enrichment_sim_web_id",
        "brand_id",
        "enrichment_status",
        "rank",
        "industry",
        "ppc_spend",
        "company_name",
        "annual_revenue",
        "online_revenue",
        "employees",
        "hq_country",
        "hq_state",
        "hq_city",
        "hq_address",
        "hq_postal_code",
        "phone_number",
        "email_address",
        "total_funding",
        "monthly_transactions",
        "company_linkedin_url",
        "top_country",
        "monthly_visits",
        "average_monthly_visits",
        "mom_traffic_change",
        "yoy_traffic_change",
        "two_years_visits_trend",
        "unique_visitors",
        "mom_unique_visitors_change",
        "yoy_unique_visitors_change",
        "two_years_unique_visitors_trend",
        "desktop_traffic_share",
        "mobile_traffic_share",
        "two_years_page_views_trend",
        "monthly_desktop_traffic",
        "mom_desktop_traffic_change",
        "yoy_desktop_traffic_change",
        "desktop_unique_visitors",
        "mom_desktop_unique_visitors_change",
        "yoy_desktop_unique_visitors_change",
        "mobile_web_monthly_traffic",
        "mom_mobile_web_traffic_change",
        "yoy_mobile_web_traffic_change",
        "mobile_web_unique_visitors",
        "mom_mobile_web_unique_visitors_change",
        "yoy_mobile_web_unique_visitors_change",
        "direct_traffic_share",
        "email_share",
        "referrals_share",
        "social_share",
        "organic_search_share",
        "paid_search_share",
        "display_ads_traffic_share",
        "direct_traffic",
        "mom_direct_traffic_change",
        "yoy_direct_traffic_change",
        "two_years_direct_visits_trend",
        "email_visits",
        "mom_email_visits_change",
        "yoy_email_visits_change",
        "two_years_mail_visits_trend",
        "referral_visits",
        "mom_referrals_visits_change",
        "yoy_referrals_visits_change",
        "two_years_referrals_visits_trend",
        "social_visits",
        "mom_social_visits_change",
        "yoy_social_visits_change",
        "two_years_social_visits_trend",
        "organic_search_visits",
        "mom_organic_search_change",
        "yoy_organic_search_change",
        "two_years_organic_search_visits_trend",
        "paid_search_visits",
        "mom_paid_search_change",
        "yoy_paid_search_change",
        "two_years_paid_search_visits_trend",
        "display_ad_traffic",
        "mom_display_traffic_change",
        "yoy_display_visits_change",
        "two_years_display_ads_visits_trend",
        "international_visits",
        "international_visits_share",
        "male_share",
        "female_share",
        "age1824",
        "age2534",
        "age3544",
        "age4554",
        "age5564",
        "age65",
        "visit_duration",
        "monthly_visits_per_visitor",
        "pages_per_visit",
        "total_page_views",
        "mom_total_page_views_change",
        "yoy_total_page_views_change",
        "bounce_rate",
        "desktop_visit_duration",
        "desktop_pages_per_visit",
        "desktop_total_page_views",
        "mom_desktop_page_views_change",
        "yoy_desktop_page_views_change",
        "desktop_bounce_rate",
        "mobile_web_visit_duration",
        "mobile_web_pages_per_visit",
        "mobile_web_total_page_views",
        "mom_mobile_web_page_views_change",
        "yoy_mobile_web_page_views_change",
        "mobile_web_bounce_rate",
        "similarweb_revenue_estimate",
        "employee_count_revenue_estimate",
        "web_traffic_revenue_estimate",
        "company_revenue_estimate",
        "online_revenue_estimate",
        "ad_spend_estimate",
        "ip_ad_spend_estimate",
        "licensing_opportunity_estimate",
        "summary_industry_category",
        "created_at",
        "last_updated_at",
    ]

    def get_all_attributes(self):
        """
        All the db columns for EnrichmentSimWeb Class
        Consideration: Any changes here should be reflected in EnrichmentSimWeb Model Class
        """
        return self.all_attributes

    def get_initialization_attributes(self):
        """
        All the attributes required for initilization of EnrichmentSimWeb Class
        Consideration: Any changes here should be reflected in places like POST APIs for EnrichmentSimWeb Routes
        """

        not_required_list = [
            "enrichment_sim_web_id",
            "created_at",
            "last_updated_at",
        ]
        initialization_attributes = [
            x for x in self.all_attributes if x not in not_required_list
        ]
        return initialization_attributes
