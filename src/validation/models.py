from apiflask import Schema
from apiflask.fields import String, Integer
from apiflask.validators import Length, Range


class TaskModel(Schema):
    name = String(required=True, validate=Length(min=2, max=32))
    description = String(required=False, validate=Length(min=0, max=256))


class MemoryModel(Schema):
    used_memory = Integer(required=True, validate=Range(min=1))
    alarm_memory_value = Integer(required=True, validate=Range(min=1))
