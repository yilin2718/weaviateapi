from urllib import request
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

import weaviate 

# initiate the Weaviate client
client = weaviate.Client("http://localhost:8081")
#172.21.0.2
#client = weaviate.Client("http://host.docker.internal:8081")

templates=Jinja2Templates(directory="templates")

app = FastAPI()

@app.get("/")
def frontpage(request: Request):  #, concept = None
    """
    displays front page 
    """
    # print(request)
    return templates.TemplateResponse("frontpage.html", {"request": request, "results": []})



def get_query_for_concept(text: str):
    near_text_filter = {
        "concepts": [text],
        "certainty": 0.7
    }
    query_result = client.query\
        .get("Product", ["title","description","price","mainCat"])\
        .with_near_text(near_text_filter)\
        .with_limit(5)\
        .do()

    return(query_result['data']['Get']['Product'])



@app.post("/search")
async def search(request: Request, search: str = Form()): 
    results = get_query_for_concept(search)
    print(results)

    return templates.TemplateResponse("frontpage.html", {"results": results, "request": request})
