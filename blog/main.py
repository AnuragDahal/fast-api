from fastapi import FastAPI, Depends, Response, status, HTTPException
import schemas
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
'''This function is used to get the database and then close it after the work is done'''


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# to post a blog into a database


@app.post("/blog")
async def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog
    # raise HTTPException(status_code=status.HTTP_201_CREATED,detail=f"Blog of id {models.Base.id} created")

# to get blogs from the database


@app.get("/blog")
async def get_all(response: Response, db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    if not blogs:
        response.status_code = status.HTTP_404_NOT_FOUND
    return blogs

# to get a particular blog from the database


@app.get("/blog/{id}", status_code=200)
async def view(id: int, response: Response, db: Session = Depends(get_db)):
    view_blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not view_blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog of id {id} is not found")
    return view_blog

# to delete a blog from the database


@app.delete("/blog/{id}")
async def delete(id: int, response: Response, db: Session = Depends(get_db)):
    delete_blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not delete_blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog of id {id} is not found")
    ''' the response can also be given by the following manner but it is a bit lengthy
        response.status_code=status.HTTP_404_NOT_FOUND
        return{
            "data":f"Blog of id {id} not found"
        }'''
    db.delete(delete_blog)
    db.commit()
    response.status_code = status.HTTP_204_NO_CONTENT
    return "deleted"

# to delete all blogs from the database

@app.delete("/blog/delete")
async def delete_all(response: Response, db: Session = Depends(get_db)):
    all_blogs = db.query(models.Blog).filter(models.Blog).all()
    if not all_blogs:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail="No blogs to be deleted")
    db.delete(all_blogs)
    db.commit()
    return all_blogs
