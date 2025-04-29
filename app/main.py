from fastapi import FastAPI, Query
from pymongo import MongoClient
from fuzzywuzzy import fuzz

from app.amend_nobel import Prize

app = FastAPI()

client = MongoClient("mongodb://mongo:27017/")
db = client["nobel"]
collection = db["prizes"]


def format_laureate_result(laureate, prize):
    full_name = f"{laureate.get('firstname', '')} {laureate.get('surname', '')}".strip()
    return {
        "name": full_name,
        "year": prize.get("year"),
        "category": prize.get("category"),
        "motivation": laureate.get("motivation")
    }


def fuzzy_match(query: str, text: str, threshold: int):
    return fuzz.ratio(query.lower(), text.lower()) >= threshold


@app.get("/")
def root():
    return {"message": "Nobel Prize Winners Search API"}


@app.get("/search/name")
def search_by_name(query: str = Query(...)):
    results = []
    for prize in collection.find():
        for laureate in prize.get("laureates", []):
            full_name = f"{laureate.get('firstname', '')} {laureate.get('surname', '')}".strip()
            if fuzzy_match(query, full_name, 80):  # we can change threshold value based on the accuracy we want
                results.append(format_laureate_result(laureate, prize))
    return results


@app.get("/search/category")
def search_by_category(query: str = Query(...)):
    results = []
    for prize in collection.find():
        if fuzzy_match(query, prize.get("category", ""), 70):
            for laureate in prize.get("laureates", []):
                results.append(format_laureate_result(laureate, prize))
    return results


@app.get("/search/motivation")
def search_by_motivation(query: str = Query(...)):
    results = []
    for prize in collection.find():
        for laureate in prize.get("laureates", []):
            if fuzzy_match(query, laureate.get("motivation", ""), 70):
                results.append(format_laureate_result(laureate, prize))
    return results


@app.post("/add", status_code=201)  # if it exists already we update the record otherwise we add a new one
def add_or_update_prize(prize: Prize):
    existing = collection.find_one({"year": prize.year, "category": prize.category})

    prize_dict = prize.model_dump()

    if existing:
        updated_laureates = existing.get("laureates", []) + [v.model_dump() for v in prize.laureates]
        collection.update_one(
            {"_id": existing["_id"]},
            {"$set": {"laureates": updated_laureates}}
        )
        return {"message": "Prize got updated"}

    collection.insert_one(prize_dict)
    return {"message": "New Prize added"}
