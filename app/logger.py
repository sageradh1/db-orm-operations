"""
App level logger module based on runtime environment development or production
"""

import logging
import os

if os.getenv("FLASK_ENV") == "production":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filename="./logs/app.log",
    )
else:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filename="./logs/app.log",
    )

# Whenever a logger object is required, app_logger can be imported by
# other files
app_logger = logging.getLogger("companydb_app")
