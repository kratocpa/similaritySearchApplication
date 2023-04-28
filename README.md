# Similarity search application
Minimal fastapi application which allows the user to send a query and which returns N most relevant results.

## Run
```
git clone https://github.com/kratocpa/similaritySearchApplication.git
```
```
cd similaritySearchApplication
```
```
pip install -r requirements.txt
```
```
docker-compose up -d
```
Run search api
```
uvicorn app.main:app --reload
```

## Load data
Load input data - if the endpoint is called multiple times, the data in elasticsearch will be duplicated.
It takes approximately 5 minutes.
```
wget localhost:8000/load_data
```


## Usage

This endpoint can be used for searching
```
127.0.0.1:8000/search_relevant_companies?search_term={search_term}&size={size}
```
Specific examples
```
http://127.0.0.1:8000/search_relevant_companies?search_term=autoservisy&size=10
http://127.0.0.1:8000/search_relevant_companies?search_term=firmy, ktere pouzivaji CNC stroje&size=10
```

