from fastapi import FastAPI, Depends, Response, status, HTTPException
import schemas
from mangum import Mangum
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
handler=Mangum(app)


'''This function is used to get the database and then close it after the work is done'''
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

index = open("index.html").read()


@app.get("/new")
async def root():
    return HTMLResponse(content=index, status_code=200)

# to post a blog into a database
@app.post("/blog",status_code=status.HTTP_201_CREATED)
async def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(request)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog



# to get blogs from the database
@app.get("/blog/get",status_code=302)
async def get_all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No blogs found")
    return blogs

# to get a particular blog from the database

@app.get("/blog/{id}", status_code=200,response_model=schemas.show)
async def view(id: int, db: Session = Depends(get_db)):
    view_blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not view_blog: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog of id {id} is not found")
    return view_blog


# to delete all 
@app.delete("/blog/delete_all", status_code=status.HTTP_202_ACCEPTED)
async def delete_all(db: Session = Depends(get_db)):
    all_blogs = db.query(models.Blog).all()
    if not all_blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No blogs found")
    # here the delete,commit function of sql alchemy accepts single model instance not a list of instance so we need to delete individually
    for blog in all_blogs:
        db.delete(blog)
    db.commit()
    return "All blogs have been deleted"

# to delete a blog from the database
@app.delete("/blog/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: int, db: Session = Depends(get_db)):
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
    return "deleted"

# to update a blog of given id

@app.put("/update/{id}",status_code=status.HTTP_202_ACCEPTED)
async def update(request:schemas.Blog,id:int,db:Session=Depends(get_db)):
    update_blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not update_blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Blog of id {id} not found")
    update_blog.update({"title":request.title,"body": request.body})
    db.commit()
    return "updated title and body "
    
# to create a new user

