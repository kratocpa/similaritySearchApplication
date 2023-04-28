from fastapi import FastAPI, HTTPException
from app.data_loader.data_etl import DataETL
from app.gateways.elasticsearch_gateway import ElasticsearchGateway

app = FastAPI()
elasticsearch_gateway = ElasticsearchGateway()


@app.get("/search_relevant_companies")
async def search_relevant_companies(search_term: str, size: int | None = None):
    result = elasticsearch_gateway.search_item(search_term=search_term, size=size)
    return {"results": result}


@app.get("/load_data")
async def load_data():
    try:
        data_etl = DataETL()
        data_etl.run()
        return {"message": "Data loaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=404, detail="Error loading data")
