import uuid
from datetime import datetime


class BaseModel:
    def __init__(self):
        self.id = str(uuid.uuid4())
        time = datetime.utcnow()
        self.created_at = time
        self.updated_at = time

    def save(self):
        return self

    def to_dict(self):
        result = self.__dict__.copy()
        result["created_at"] = self.created_at.isoformat()
        result["updated_at"] = self.updated_at.isoformat()
        return result
