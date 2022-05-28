import weaviate 

# initiate the Weaviate client
client = weaviate.Client("http://localhost:8081")

def get_query_from_concept(text: str):
    near_text_filter = {
        "concepts": [text],
        "certainty": 0.7
        }
    query_result = client.query\
        .get("Product", ["title","description","price"])\
        .with_near_text(near_text_filter)\
        .with_limit(3)\
        .do()
    return(query_result)



@app.post("/concept")
async def search(text: str):    
    return {get_query_from_concept(text)}
