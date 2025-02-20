"""
Extension file will include all app level extensions which are being used.
"""

import os

from flask_migrate import Migrate
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

print("In extension", os.getenv("SQLALCHEMY_SCHEMA"))
metadata = MetaData(schema=os.getenv("SQLALCHEMY_SCHEMA"))

db = SQLAlchemy(metadata=metadata)
migrate = Migrate()
api = Api(validate=True)
