from sqlalchemy.sql import text


async def create_password(password: str, db, name: str) -> bool:
    stmt = text("INSERT INTO chatbot.app_validation (name, temp_pass) VALUES (:name, :temp_pass) RETURNING id")
    inserted = False
    try:
        async with db as session:
            inserted = await session.execute(stmt, {"temp_pass": password, "name": name})
            await session.commit()
        if not inserted:
            return False
        return True
    except Exception as e:
        print(e)
        return False


async def revoke_password(name: str, cur_status: bool, db) -> bool:
    stmt = text("UPDATE chatbot.app_validation SET cur_status = :cur_status WHERE name = :name RETURNING id, cur_status")
    revoked = False
    try:
        async with db as session:
            revoked = await session.execute(stmt, {"name": name, "cur_status": cur_status})
            await session.commit()
        print(revoked.fetchone())
        if not revoked:
            return False
        return True
    except Exception as e:
        print(e)
        return False


async def check_password(password: str, db) -> bool:
    stmt = text("SELECT id, name FROM chatbot.app_validation WHERE temp_pass = :password")
    try:
        async with db as session:
            status = await session.execute(stmt, {"password": password})
            await session.commit()
        status = status.fetchone()
        return status
    except Exception as e:
        print(e)
        return False
