from abc import abstractmethod, ABC
import copy
import logging

class AbstractConnector(ABC):
    DEFAULT_CONFIG = {
        "host": "127.0.0.1", # IP Address or Domain name of RabbitMQ Service
        "port": 27017, # Serving port of RabbitMQ Service
        "username": "guest", # Username of account
        "password": "guest" # Password of account
    }
    
    def __init__(self, **configs):
        # update custom configs
        self.config = copy.copy(self.DEFAULT_CONFIG)
        for key in self.config:
            if key in configs:
                self.config[key] = configs.pop(key)
        
        # Only check for extra config keys
        assert not configs, 'Unrecognized configs: %s' % (configs,)

        self.__setup()
    
    @abstractmethod
    def __setup(self, *args, **kwargs):
        pass
    