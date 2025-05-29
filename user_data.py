from faker import Faker

def generate_user():
    fake = Faker()
    payload = {
        "email": fake.email(),
        "password": fake.password(),
        "name": fake.name()
    }
    return payload