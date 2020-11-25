from abc import abstractmethod, ABC
import copy
import logging
from pymongo import MongoClient

class AbstractConnector(ABC):
    DEFAULT_CONFIG = {
        "host": "127.0.0.1", # IP Address or Domain name of warehouse
        "port": 27017, # Serving port of data warehouse service
        "username": "guest", # Username of account
        "password": "guest", # Password of account
        "database": None
    }
    
    def __init__(self, **configs):
        # update custom configs
        self.config = copy.copy(self.DEFAULT_CONFIG)
        for key in self.config:
            if key in configs:
                self.config[key] = configs.pop(key)
        # Check for database name
        assert self.config["database"] is not None, "Must set schema name"
        # Only check for extra config keys
        assert not configs, 'Unrecognized configs: %s' % (configs,)

        self._setup()
        
    
    @abstractmethod
    def _setup(self, *args, **kwargs):
        pass

class MongoConnector(AbstractConnector):
    def __init__(self, host, port, username, password, database):
        super().__init__(host=host, port=port, username=username, password=password, database=database)

    def _setup(self, *args, **kwargs):
        print(self.config)
        self.mongo_client = MongoClient(host=self.config['host'], 
                                        port=self.config['port'], 
                                        username=self.config['username'],
                                        password=self.config['password'],
                                        authMechanism='SCRAM-SHA-256')
        
        self.mongo_schema = self.mongo_client[self.config['database']]
        
        print(self.mongo_client.list_database_names())
    
    def insert_record(self, column_name, data):
        column_object = self.mongo_schema[column_name]
        record_object = column_object.insert_one(data)
        return record_object.inserted_id
        
