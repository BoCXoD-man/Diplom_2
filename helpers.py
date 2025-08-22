import uuid
from faker import Faker

fake = Faker('en_US')


def generate_user_data() -> tuple[str, str, str]:
    """
    Return:
        tuple[str, str, str]: email, password, name
    """
    email = f"{uuid.uuid4().hex}@{fake.free_email_domain()}"  # уникален межзапусково
    password = fake.password(length=10)
    name = f"{fake.first_name()} {fake.last_name()}"
    return email, password, name