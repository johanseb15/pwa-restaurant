from bson import ObjectId

def to_object_id(id_str: str) -> ObjectId:
    return ObjectId(id_str)

def to_string_id(obj_id: ObjectId) -> str:
    return str(obj_id)
