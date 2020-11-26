from abc import abstractmethod, ABC
from .fields import FieldInterface, TextField, ObjectIdField
import json
import warnings
from .objects import mongo_connector


class AbstractModel(ABC):
    def __init__(self, **kwargs):
        self._property_dict = self._get_property()
        for prop in self._property_dict:
            if prop not in kwargs:
                kwargs[prop] = None
        self.attribute_names = set()
        for key in kwargs:
            setattr(self, key, kwargs[key])
            self.attribute_names.add(key)
        self.collection_name = self.__class__.__name__.lower()
    
    def _get_property(self):
        property_dict = dict()
        for key in vars(self.__class__):
            if isinstance(getattr(self, key), FieldInterface):
                
                if key not in ['index', 'idx', '_id']:
                    getattr(self, key).set_field_name(key)
                    property_dict[key] = getattr(self, key)
                else:
                    warnings.warn(f"_id will automatically added. key {key} shouldn't provided")
        # Add default _id fields
        property_dict["_id"] = ObjectIdField(allow_none=True)
        property_dict["_id"].set_field_name("_id")
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

    def asdict(self):
        data_pack = dict()
        for attr_name in self.attribute_names:
            value = getattr(self, attr_name)
            data_pack[attr_name] = self._property_dict[attr_name].validate_value(value)
        return data_pack

    def toJson(self):
        data_pack = self.asdict()

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

    def save(self):
        if self._id is None:
            mongo_connector.insert_document(self)
        else:
            mongo_connector.update_document(self)
    
    def delete(self):
        if self._id is not None:
            mongo_connector.delete_document(self)
            self._id = None