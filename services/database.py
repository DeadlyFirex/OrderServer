from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from services.config import Config

config = Config().get_config()
engine = create_engine(f"sqlite:///{config.database.absolute_path}",
                       convert_unicode=True, connect_args={"check_same_thread": False})
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    from models import user, product
    Base.metadata.create_all(bind=engine)
