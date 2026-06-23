from .db import engine, Base
from .models import Transaction, UserStats

def init_db():
    Base.metadata.create_all(bind=engine)