from validations.data_classes import AppValidation
from validations.tools import create_password

async def create_validation(data: AppValidation, db):
    print("Creating validation...")
    creation_status = await create_password(data.password, db, data.name)
    return creation_status


async def revoke_validation():
    print("Revoking validation...")

async def check_validation():
    print("Checking validation...")