from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .db import get_db
from .init_db import init_db
from . import schemas, crud, ranking

app = FastAPI(title="Transaction Ranking System")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # for demo project
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

@app.get("/")
def root():
    return {"message": "Backend is running"}

@app.post("/transaction", response_model=schemas.TransactionResponse)
def create_transaction(tx: schemas.TransactionCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_transaction(db, tx)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/summary/{user_id}", response_model=schemas.SummaryResponse)
def get_summary(user_id: str, db: Session = Depends(get_db)):
    summary = crud.get_user_summary(db, user_id)
    if not summary:
        raise HTTPException(status_code=404, detail="User not found")
    return summary

@app.get("/ranking")
def get_ranking(db: Session = Depends(get_db)):
    return ranking.get_rankings(db)