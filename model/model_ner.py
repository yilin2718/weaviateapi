
from spacy.lang.en import English
from gensim.parsing.preprocessing import remove_stopwords

class QueryParse ():

  def __init__(self):
    self.nlp_model = English()
    ruler = self.nlp_model.add_pipe("entity_ruler").from_disk("model/test1_NER_model_may28.jsonl")

# this version of parse_query returns a dictionary 
  def parse_query (self, qry_request, context): 
    """
    parse user query
    """
    # eventually use lower case - now mixed case
    #doc = self.nlp_model(str.lower(qry_request))
    doc = self.nlp_model(qry_request)
    phrase_list = []
    label_list = []
    comb_list = {}
    for ent in doc.ents:
      phrase_list.append(ent.text)
      label_list.append(ent.label_)
      comb_list[ent.label_]= ent.text
    
    # add weaviate_context : just information excluding words for ent.label
    weaviate_context=qry_request
    keys=comb_list.keys()
    for key in keys:
        if key!='weaviate_neartext':
            weaviate_context=weaviate_context.replace(comb_list[key], '')  
    
    weaviate_context=remove_stopwords(weaviate_context)    
    comb_list["weaviate_neartext"]= weaviate_context
    
    return comb_list

model = QueryParse()

def get_model ():
    return model
