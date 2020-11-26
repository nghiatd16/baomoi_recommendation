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
        pass
    
    def insert_document(self, orm_object):
        with MongoClient(host=self.config['host'], 
                                        port=self.config['port'], 
                                        username=self.config['username'],
                                        password=self.config['password'],
                                        authMechanism='SCRAM-SHA-256') as mongo_client:
        
            self.mongo_schema = mongo_client[self.config['database']]
            collection_name = orm_object.collection_name
            collection_object = self.mongo_schema[collection_name]
            data = orm_object.asdict()
            data.pop("_id")
            document_object = collection_object.insert_one(data)
            orm_object._id = document_object.inserted_id
            return orm_object
    
    def update_document(self, orm_object):
        with MongoClient(host=self.config['host'], 
                                        port=self.config['port'], 
                                        username=self.config['username'],
                                        password=self.config['password'],
                                        authMechanism='SCRAM-SHA-256') as mongo_client:
        
            self.mongo_schema = mongo_client[self.config['database']]
            collection_name = orm_object.collection_name
            collection_object = self.mongo_schema[collection_name]
            query = {"_id", orm_object._id}
            update_data = orm_object.asdict()
            update_data.pop("_id")
            newvalues = { "$set": update_data }

            collection_object.update_one(query, newvalues)
            return orm_object
    
    def delete_document(self, orm_object):
        with MongoClient(host=self.config['host'], 
                                        port=self.config['port'], 
                                        username=self.config['username'],
                                        password=self.config['password'],
                                        authMechanism='SCRAM-SHA-256') as mongo_client:
        
            self.mongo_schema = mongo_client[self.config['database']]
            collection_name = orm_object.collection_name
            collection_object = self.mongo_schema[collection_name]
            query = {"_id", orm_object._id}
            collection_object.delete_one(query)
    
    def find_document(self, collection_name, condition_dict):
        with MongoClient(host=self.config['host'], 
                                        port=self.config['port'], 
                                        username=self.config['username'],
                                        password=self.config['password'],
                                        authMechanism='SCRAM-SHA-256') as mongo_client:
        
            self.mongo_schema = mongo_client[self.config['database']]
            collection_object = self.mongo_schema[collection_name]
            result = collection_object.find(condition_dict)
            return result
        
