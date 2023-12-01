from fastapi import FastAPI, Depends
import schemas, models
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from database import engine,SessionLocal
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app=FastAPI()
'''This function is used to get the database and then close it after the work is done'''
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

# to post a blog into a database
@app.post("/blog")
async def create(request:schemas.Blog, db:Session=Depends(get_db)):
    new_blog = models.Blog(title=request.title,body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog
    
# to get blogs from the database

@app.get("/blog")
async def get_all(db:Session=Depends(get_db)):
    blogs=db.query(models.Blog).all()
    return blogs