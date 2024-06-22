from fastapi import APIRouter, Depends

from dependencies import validate_api_key, db_session
from validations.controller import create_validation, check_validation, revoke_validation, login_user
from validations.data_classes import AppValidation, RevokedValidation, CheckValidation

validationRoutes = APIRouter()


@validationRoutes.put("/", dependencies=[Depends(validate_api_key)])
async def validation_check(request: CheckValidation, db=Depends(db_session)):
    session_dict = await check_validation(request, db)
    if session_dict:
        return {"status": "success", "response": session_dict}
    return {"status": "Failed", "response": "Password not found"}


@validationRoutes.post("/create", dependencies=[Depends(validate_api_key)])
async def validation_create(request: AppValidation, db=Depends(db_session)):
    valid_pass = await create_validation(request, db)
    if not valid_pass:
        return {"response": {"validation": "Password Not Created"}}
    return {"response": {"validation": "Created"}}


@validationRoutes.put("/revoke", dependencies=[Depends(validate_api_key)])
async def validation_revoke(request: RevokedValidation, db=Depends(db_session)):
    pass_status = await revoke_validation(request, db)
    if not pass_status:
        return {"response": {"validation": "Password Not Revoked"}}
    return {"response": {"temp": "Temp password revoked"}}


@validationRoutes.put("/validateuser", dependencies=[Depends(validate_api_key)])
async def user_login(request: CheckValidation, db=Depends(db_session)):
    user_session = await login_user(request.password, db=db)
    if user_session.active_status:
        return {"response": {"validation": "success", "key": user_session.session_id}}
    return {"response": {"validation": "failed"}}
