from .connector import MongoConnector
import settings

mongo_connector = MongoConnector(host=settings.DATABASE_CONFIG["host"],
                                port=settings.DATABASE_CONFIG["port"],
                                username=settings.DATABASE_CONFIG["username"],
                                password=settings.DATABASE_CONFIG["password"],
                                database=settings.DATABASE_CONFIG["database"])