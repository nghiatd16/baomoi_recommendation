from abc import abstractmethod, ABC
from .fields import FieldInterface
import json

class AbstractModel(ABC):
    def __init__(self, **kwargs):
        print("init model")
        self.attribute_names = set()
        for key in kwargs:
            setattr(self, key, kwargs[key])
            self.attribute_names.add(key)
        self._property_dict = self._get_property()
    
    def _get_property(self):
        property_dict = dict()
        # print(vars(self.__class__))
        for keys in vars(self.__class__):
            if isinstance(getattr(self, keys), FieldInterface):
                property_dict[keys] = getattr(self, keys).__class__
        return property_dict

    def addAttribute(self, name, value):
        setattr(self, name, value)
        self.attribute_names.add(name)

    def add_attribute(self, name, value):
        self.addAttribute(name, value)

    def delAttribute(self, name):
        if name in self.attribute_names:
            delattr(self, name)
            self.attribute_names.remove(name)
    
    def del_attribute(self, name):
        self.delAttribute(name)

    def toJson(self):
        data_pack = dict()
        for attr_name in self.attribute_names:
            data_pack[attr_name] = getattr(self, attr_name)
        return json.dumps(data_pack, ensure_ascii=False)
    
    def to_json(self):
        return self.toJson()
    
    @classmethod
    def fromJson(cls, json_string):
        data_pack = json.loads(json_string)
        return AbstractModel(**data_pack)
    
    @classmethod
    def from_json(cls, json_string):
        return cls.fromJson(json_string)

    def __getitem__(self, key):
        if key not in self.attribute_names:
            raise KeyError("Key {} not found".format(key))
        return getattr(self, key)
    
    def __contains__(self, item):
        if item in self.attribute_names:
            return True
        return False