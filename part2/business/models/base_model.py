import uuid
from datetime import datetime


class BaseModel:
    def __init__(self):
        self.id = uuid.uuid4()
        time = datetime.utcnow()
        self.created_at = time
        self.updated_at = time

    def update_timestamp(self):
        self.updated_at = datetime.utcnow()
