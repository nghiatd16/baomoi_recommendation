import inspect
class FieldInterface:
    def __init__(self, assertion_class, *args, **kwargs):
        assert inspect.isclass(assertion_class), "Expected assertion_class is a class not instance"
        self.assertion_class = assertion_class
        self.value = None
    
    def __str__(self):
        return str(self.value)

    def set_value(self, value):
        assert isinstance(value, assertion_class), f"Expected {assertion_class} but got {value.__class__}"
        self.value = value

class IntegerField(FieldInterface):
    def __init__(self, *args, **kwargs):
        super().__init__(int, *args, **kwargs)

class FloatField(FieldInterface):
    def __init__(self, *args, **kwargs):
        super().__init__(float, *args, **kwargs)

class TextField(FieldInterface):
    def __init__(self, *args, **kwargs):
        super().__init__(str, *args, **kwargs)

class ArrayField(FieldInterface):
    def __init__(self, *args, **kwargs):
        super().__init__(list, *args, **kwargs)
