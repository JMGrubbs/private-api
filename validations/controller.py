from sessions.data_classes import UserSession
from validations.data_classes import AppValidation, RevokedValidation, CheckValidation
from validations.tools import create_password, revoke_password, check_password
from dependencies import handle_user_sessions


async def create_validation(data: AppValidation, db):
    creation_status = await create_password(data.password, db, data.name)
    return creation_status


async def revoke_validation(data: RevokedValidation, db):
    return await revoke_password(data.name, data.revoked, db)


async def check_validation(data: CheckValidation, db):
    valid = await check_password(data.password, db)
    if valid:
        sessions_dict = {"name": valid[1], "status": valid[0]}
        return sessions_dict
    return False


async def login_user(password: str, db):
    user_session = UserSession(password=password)
    await user_session.validate_session(db=db)
    add_session = await handle_user_sessions(user_session)
    print("session added to cach", add_session)
    if user_session.active_status:
        return user_session.session_id
    return False
