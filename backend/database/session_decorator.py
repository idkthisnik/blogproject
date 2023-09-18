from .connection import engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker()


class Sessioner():
    def dbconnect(func):
        def inner(*args, **kwargs):
            session = Session(bind=engine)
            try:
                result = func(*args, session=session, **kwargs)
                session.commit()
            except:
                session.rollback()
                raise
            finally:
                session.close()
            return result
        return inner