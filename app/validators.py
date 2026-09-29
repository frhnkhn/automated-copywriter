from pydantic import ValidationError

from .models import CopyRequest


def validate_request(data):

    try:
        request = CopyRequest(**data)

        return request

    except ValidationError as error:

        print("\n❌ Invalid input:\n")
        print(error)

        return None