# Nobel Prize Winners Search API

This project provides a Python web API that allows you to search the 
[Nobel Prize dataset](https://api.nobelprize.org/v1/prize.json) by laureate name, category, or motivation using 
fuzzy matching. It is fully containerized with Docker and uses MongoDB for data storage and FastAPI for the API.

---

## Tech Stack

- **Python 3.10**
- **FastAPI** 
- **MongoDB** 
- **Docker & Docker Compose** 
- **fuzzywuzzy** (for approximate text matching)

---

## How to Run the App

### 1. Clone this repository

```bash
git clone https://github.com/nikolasfiniotis/code-challenge.git
cd code-challenge
```

### 2. Load Nobel Prize data into MongoDB

Start MongoDB container:
```bash
docker-compose up -d mongo
```

Then run the data loader which downloads the JSON dataset and populates MongoDB.
```bash
python3 data/load_data.py
```

### 3. Start the web API

```bash
docker-compose up --build
```

open a web browser to: http://localhost:8000

play with the rest endpoints using the following and search based on the attribute you want from the below:
* /search/name?query=
* /search/category?query=
* /search/motivation?query=

visit the swagger version by adding /docs to the local host url and use the request body to add or update a prize:

```
{
  "year": "2025",
  "category": "string",
  "laureates": [
    {
      "firstname": "string",
      "surname": "string",
      "motivation": ""
    }
  ]
}
```