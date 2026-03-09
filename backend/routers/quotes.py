# backend/routers/quotes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas, auth
from database import get_db


router = APIRouter(prefix='/api/quotes', tags=['quotes'])


@router.get('/', response_model=List[schemas.QuoteOut])
def get_my_quotes(db: Session = Depends(get_db), current_user=Depends(auth.get_current_user)):
    return db.query(models.Quote).filter(models.Quote.user_id == current_user.id).all()


@router.post('/', response_model=schemas.QuoteOut)
def create_quote(quote: schemas.QuoteCreate, db: Session = Depends(get_db), current_user=Depends(auth.get_current_user)):
    new_quote = models.Quote(**quote.dict(), user_id=current_user.id)
    db.add(new_quote)
    db.commit()
    db.refresh(new_quote)
    return new_quote


@router.put('/{quote_id}', response_model=schemas.QuoteOut)
def update_quote(quote_id: int, data: schemas.QuoteUpdate, db: Session = Depends(get_db), current_user=Depends(auth.get_current_user)):
    quote = db.query(models.Quote).filter(models.Quote.id == quote_id, models.Quote.user_id == current_user.id).first()
    if not quote:
        raise HTTPException(status_code=404, detail='Quote not found or not yours')
    for key, value in data.dict(exclude_unset=True).items():
        setattr(quote, key, value)
    db.commit()
    db.refresh(quote)
    return quote


@router.delete('/{quote_id}')
def delete_quote(quote_id: int, db: Session = Depends(get_db), current_user=Depends(auth.get_current_user)):
    quote = db.query(models.Quote).filter(models.Quote.id == quote_id, models.Quote.user_id == current_user.id).first()
    if not quote:
        raise HTTPException(status_code=404, detail='Quote not found or not yours')
    db.delete(quote)
    db.commit()
    return {'message': 'Quote deleted successfully'}
