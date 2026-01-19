# Pydantic schemas
from models.schemas import UserProfile
from pydantic import ValidationError

def validate_data(data: dict):
    try:
        validated = UserProfile(**data)
        return True, validated, None
    except ValidationError as e:
        return False, None, e
