from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from crime_search_engine import CrimeSearchEngine

app = FastAPI()

# Initialize the search engine
embeddings_file = "embeddings.npy"  
metadata_file = "metadata.json" 
model_name = "all-MiniLM-L6-v2"
hf_token = "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"

search_engine = CrimeSearchEngine(
    embeddings_file=embeddings_file,
    metadata_file=metadata_file,
    model_name=model_name,
    hf_token=hf_token
)
search_engine.setup()

# Define response model
class QueryResponse(BaseModel):
    results: Optional[List[dict]]
    message: str

@app.post("/query", response_model=QueryResponse)
async def query_api(request):
    """
    Endpoint to query the CrimeSearchEngine.
    """
    try:
        request_data = await request.json()

        # Extract individual parameters
        userid = request_data.get("userid")
        user_query = request_data.get("user_query")
        output_type = request_data.get("output_type")

        # Validate output type
        # if output_type not in ["text", "chart"]:
        #     raise HTTPException(status_code=400, detail="Invalid output_type. Must be 'text' or 'chart'.")

        # Query the embeddings
        results = search_engine.query_embeddings(query=user_query)

        # Construct response
        response_message = "Query processed successfully."
        return QueryResponse(results=results, message=response_message)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Welcome!"}