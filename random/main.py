from fastapi import FastAPI
from typing import Optional
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import yt
import uvicorn
# import ./index.html as index
index = open("index.html").read()

app = FastAPI()


@app.get("/")
async def root():
    return HTMLResponse(content=index, status_code=200)


@app.get("/about/developer")
async def about():
    return {"Name": "Anurag Dahal",
            "Address": "Birtamode,Jhapa",
            "Age": "20"}


@app.post("/about/developer/{name}/{address}/{age}")
async def put_details(name: str, address: str, age: int, sort=Optional[str]):
    return {"Name": f"{name}",
            "Address": f"{address}",
            "Age": f"{age}"}

class latest_blog(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True

@app.get("/blog/latest")
async def blog_latest():
    return {"title": "Latest Blog",
            "content": "This is the content of the latest blog"}
    


@app.post("/blog/{id}/content")
async def content(request:latest_blog, id: int, limit=10, sort: Optional[str] = None):
    return {

        "blog_id": id,
        "data": f"blog has been created with title as {request.title}",
        "content": f"{request.content} and published status as {request.published}"
    }
#query parameter and validation
@app.get("/blog/{id}")
async def update(id: int, limit, update: bool=True):
    if update:
        return {f"{limit} updated blogs from the db"}
    else:
        return {f"{id} blog is not updated"}


@app.delete("/blog/{id}")
async def delete_blog(id: int):
    return {f"{id} blog is deleted from the db"}


@app.get("/yt/")
async def download(link: str):
    yt.download(link)
    return {"Downloaded": "Downloaded"}


if __name__ == "__main__":
    uvicorn.run(app, port=8000)