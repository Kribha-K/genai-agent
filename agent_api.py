

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import google.generativeai as genai

genai.configure(api_key="AIzaSyABrlmK4_c2vKClQ13-oCsUb9H_6QCxwEI")  # Replace this with your actual API key


app = FastAPI()

model = genai.GenerativeModel("models/gemini-1.5-flash")


DB_PATH = "db/ecommerce.db"


class QueryInput(BaseModel):
    question: str


def generate_sql_from_question(question: str) -> str:
    prompt = f"""
You are an expert SQL assistant for an SQLite database with the following schema:

Table: product_total_sales
- date (TEXT)
- item_id (INTEGER)
- total_sales (REAL)
- total_units_ordered (INTEGER)

Table: product_ad_sales
- date (TEXT)
- item_id (INTEGER)
- ad_sales (REAL)
- impressions (INTEGER)
- ad_spend (REAL)
- clicks (INTEGER)
- units_sold (INTEGER)

Table: product_eligibility
- eligibility_datetime_utc (TEXT)
- item_id (INTEGER)
- eligibility (TEXT)
- message (TEXT)

Write an SQLite query that answers this user question:
\"\"\"{question}\"\"\"

✅ Only return the SQL query — no explanation, no markdown, just raw SQL.
    """
    response = model.generate_content(prompt)
    return response.text.strip().split("```")[0].strip()


@app.post("/ask")
def ask_question(input: QueryInput):
    try:
        question = input.question
        sql_query = generate_sql_from_question(question)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(sql_query)
        result = cursor.fetchall()
        conn.close()

        return {
            "question": question,
            "sql_query": sql_query,
            "answer": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


