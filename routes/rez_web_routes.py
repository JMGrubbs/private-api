from fastapi import APIRouter, HTTPException, Depends
from dependencies import validate_api_key, db_session