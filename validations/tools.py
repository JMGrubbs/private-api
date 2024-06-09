from sqlalchemy.sql import text

async def create_password(password: str, db, name: str) -> bool:
    stmt = text("INSERT INTO chatbot.app_validation (name, temp_pass) VALUES (:name, :temp_pass) RETURNING id")
    inserted = False
    async with db as session:
        inserted = await session.execute(stmt, {"temp_pass": password, "name": name})
        await session.commit()
    print(inserted)
    if not inserted:
        return False

    return True
