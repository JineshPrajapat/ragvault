from functools import wraps
from app.core.database import db_instance

def use_db_async(func):
    """
    Decorator to automatically provide a SQLAlchemy session to the function.
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with db_instance.get_session() as db:
            return await func(*args, db=db, **kwargs)
    return wrapper
