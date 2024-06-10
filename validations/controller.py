from validations.data_classes import AppValidation, RevokedValidation
from validations.tools import create_password, revoke_password, check_password

async def create_validation(data: AppValidation, db):
    creation_status = await create_password(data.password, db, data.name)
    return creation_status


async def revoke_validation(data: RevokedValidation, db):
    return await revoke_password(data.name, data.revoked, db)

async def check_validation(data: AppValidation, db):
    valid = await check_password()
    return valid