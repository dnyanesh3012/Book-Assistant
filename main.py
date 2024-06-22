from fastapi import FastAPI, HTTPException, Depends
from typing import List, Dict
import random
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Retrieve API key from environment variables
API_KEY = os.getenv("API_KEY")

# Mock function to get top 100 books
def get_mock_top_books(genre: str) -> List[Dict]:
    return [{"title": f"Book {i} ({genre})", "genre": genre} for i in range(1, 101)]

# Dependency to verify API key
def verify_api_key(api_key: str = Depends(lambda: API_KEY)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

@app.get("/get_top_books")
def get_top_books(genre: str, api_key: str = Depends(verify_api_key)):
    try:
        top_books = get_mock_top_books(genre)
        return top_books
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get_top_ten_books")
def get_top_ten_books(genre: str, api_key: str = Depends(verify_api_key)):
    try:
        top_books = get_mock_top_books(genre)[:10]
        return top_books
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get_single_book")
def get_single_book(genre: str, api_key: str = Depends(verify_api_key)):
    try:
        top_ten_books = get_mock_top_books(genre)[:10]
        chosen_book = random.choice(top_ten_books)
        return chosen_book
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/close_task")
def close_task(api_key: str = Depends(verify_api_key)):
    return {"message": "Thank you for using the book recommendation agent!"}
