from urllib import request
from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from model.model_ner import QueryParse, get_model
import weaviate 

# initiate the Weaviate client
#client = weaviate.Client("http://localhost:8081") 

weaviate_url = 'http://34.67.249.252:8080/'
secret = weaviate.AuthClientPassword("admin", "admin")
# Initiate the client with the secret
client = weaviate.Client(weaviate_url, secret)



templates=Jinja2Templates(directory="./src/templates")
app = FastAPI() 


@app.get("/")
def frontpage(request: Request):  #, concept = None
    """
    displays front page 
    """
    # print(request)
    return templates.TemplateResponse("frontpage.html", {"request": request, "results": []})

# def get_query_for_ner_concept(text: str):
#     near_text_filter = {
#         "concepts": [text]
#        # "certainty": 0.7
#     }
#     query_result = client.query\
#         .get("Product", ["title","description","price","mainCategory"])\
#         .with_near_text(near_text_filter)\
#         .with_limit(5)\
#         .do()
#     return(query_result['data']['Get']['Product'])
# "category", "brand" ,


def get_query_for_ner_concept(text_ner):

    near_text_filter = {
        "concepts": [text_ner['weaviate_neartext']]
        # "certainty": 0.7
    }

    keys=text_ner.keys()
    operands_list=[]
    for key in keys:
        if key!='weaviate_neartext':
            if key =='VENDOR':
                operands_list.append({
                     "path": ["brand"],
                     "operator": "Equal",
                     "valueString": text_ner['VENDOR']
                   })
            elif key =='CATEGORY':
                 operands_list.append({
                     "path": ["category"],
                     "operator": "Equal",
                     "valueString": text_ner['CATEGORY']
                   })
            else: 
                continue 
    if len(operands_list)>0:            
        where_filter = {
            "operator": "Or",
            "operands": operands_list
            }    
        query_result = client.query\
                .get("Product", ["title", "brand","description","price","mainCategory"])\
                .with_near_text(near_text_filter)\
                .with_limit(5)\
                .with_where(where_filter)\
                .do()
       #         .with_near_text(near_text_filter)\
    else: # if search query doesnt have name to be regonized by NER 
        query_result = client.query\
        .get("Product", ["title", "description","price","mainCategory"])\
        .with_near_text(near_text_filter)\
        .with_limit(5)\
        .do()

    return(query_result['data']['Get']['Product'])

@app.post("/search")
async def search(request: Request, search: str = Form(), model: QueryParse = Depends(get_model)): 
     search_ner=model.parse_query(search, 'xx')
     print(search_ner)
     results = get_query_for_ner_concept(search_ner)
     #results = get_query_for_ner_concept(search) -- THIS IS FOR DEBUGGING 
     #print(results)

    #  always make sure that we return a list, as frontend will iterate over it:
     if type(results) is not list:
          results = []

     return templates.TemplateResponse("frontpage.html", {"search": search, "results": results, "request": request})
