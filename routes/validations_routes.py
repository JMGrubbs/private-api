from fastapi import APIRouter, Depends

from dependencies import validate_api_key, db_session
from validations.controller import create_validation, check_validation, revoke_validation
from validations.data_classes import AppValidation, RevokedValidation

validationRoutes = APIRouter()


@validationRoutes.get("/", dependencies=[Depends(validate_api_key)])
async def validation_check():
    await check_validation()
    return {"response": {"temp": "Hello World"}}

@validationRoutes.post("/create", dependencies=[Depends(validate_api_key)])
async def validation_create(request: AppValidation, db=Depends(db_session)):
    valid_pass = await create_validation(request, db)
    if not valid_pass:
        return {"response": {"validation": "Password Not Created"}}
    return {"response": {"validation": "Created"}}

@validationRoutes.put("/revoke", dependencies=[Depends(validate_api_key)])
async def validation_create(request: RevokedValidation, db=Depends(db_session)):
    pass_status = await revoke_validation(request, db)
    if not pass_status:
        return {"response": {"validation": "Password Not Revoked"}}
    return {"response": {"temp": "Temp password revoked"}}
