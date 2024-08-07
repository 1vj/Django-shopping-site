import uuid
from django.utils.crypto import get_random_string

def generate_email_auth_token(device_uuid):
    # Generate a random token using Django's get_random_string function
    random_token = get_random_string(length=32)

    # Concatenate the device UUID and random token to create the email authentication token
    email_auth_token = f"{device_uuid}-{random_token}"

    return email_auth_token

# Example usage:
device_uuid = uuid.uuid4()  # Generate a random UUID for the device
email_auth_token = generate_email_auth_token(device_uuid)
print("Email authentication token:", email_auth_token)
