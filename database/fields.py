import inspect
from bson.objectid import ObjectId
import cryptocode
from settings import SECRET_KEY

class FieldInterface:
    def __init__(self, assertion_class, allow_none, *args, **kwargs):
        assert inspect.isclass(assertion_class), "Expected assertion_class is a class not instance"
        assert isinstance(allow_none, bool), "Expected allow_none is an instance of bool"
        self.assertion_class = assertion_class
        self.allow_none = allow_none
        self._field_name = ""
    
    def __str__(self):
        return str(self.value)
    
    def set_field_name(self, field_name):
        assert isinstance(field_name, str), "Expected field_name is an instance of str"
        self._field_name = field_name
        return field_name

    def validate_value(self, value):
        if value is None:
            if self.allow_none:
                return value
            else:
                raise AttributeError(f"Field {self._field_name} not allowed None value")
        assert isinstance(value, self.assertion_class), f"Field '{self._field_name}' expected {self.assertion_class} but got {value.__class__}"
        return value

class IntegerField(FieldInterface):
    def __init__(self, allow_none=True, *args, **kwargs):
        super().__init__(int, allow_none, *args, **kwargs)

class FloatField(FieldInterface):
    def __init__(self, allow_none=True, *args, **kwargs):
        super().__init__(float, allow_none, *args, **kwargs)

class TextField(FieldInterface):
    def __init__(self, allow_none=True, *args, **kwargs):
        super().__init__(str, allow_none, *args, **kwargs)

class ArrayField(FieldInterface):
    def __init__(self, allow_none=True, *args, **kwargs):
        super().__init__(list, allow_none, *args, **kwargs)

class ObjectIdField(FieldInterface):
    def __init__(self, allow_none=True, *args, **kwargs):
        super().__init__(ObjectId, allow_none, *args, **kwargs)

class PasswordField(FieldInterface):
    def __init__(self, allow_none=False, *args, **kwargs):
        super().__init__(str, allow_none, *args, **kwargs)
    
    def validate_value(self, value):
        value = super().validate_value(value)
        return cryptocode.encrypt(value, SECRET_KEY)

    def validate_password(self, input_string_1, input_string_2):
        return cryptocode.encrypt(input_string_1, SECRET_KEY) == cryptocode.encrypt(input_string_2, SECRET_KEY)

class BooleanField(FieldInterface):
    def __init__(self, allow_none=True, *args, **kwargs):
        super().__init__(bool, allow_none, *args, **kwargs)

