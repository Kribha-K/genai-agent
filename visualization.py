rom fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import google.generativeai as genai
import matplotlib.pyplot as plt
import pandas as pd
import base64
from io import BytesIO



genai.configure(api_key="AIzaSyABrlmK4_c2vKClQ13-oCsUb9H_6QCxwEI")
model = genai.GenerativeModel("gemini-1.5-pro")
 

DB_PATH = r"C:\Users\mekaa\OneDrive\Documents\genai_project\db\ecommerce.db"


app = FastAPI()

class QueryRequest(BaseModel):
    question: str

def generate_bar_chart(data, columns):
    df = pd.DataFrame(data, columns=columns)

    if df.shape[1] < 2:
        return None  # Need at least 2 columns to plot

    plt.figure(figsize=(8, 4))
    plt.bar(df[columns[0]], df[columns[1]])
    plt.xlabel(columns[0])
    plt.ylabel(columns[1])
    plt.title("Bar Chart")
    plt.xticks(rotation=45)

    buf = BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)

    return base64.b64encode(buf.read()).decode("utf-8")


@app.post("/query")
async def ask_agent(req: QueryRequest):
    question = req.question

    try:
       
        prompt = f"""
You are a data analyst assistant. Convert the user question into a valid SQL query for a SQLite database.
Only return the SQL query. No explanation, no markdown, no code blocks.

User question: {question}
"""
        response = model.generate_content([prompt])
        sql_query = response.text.strip()
        print("Generated SQL:", sql_query)

       
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        conn.close()

       
        chart_base64 = None
        if rows and len(columns) >= 2 and len(rows) <= 20 and "plot" in question.lower():
            chart_base64 = generate_bar_chart(rows, columns)

       
        return {
            "query": sql_query,
            "result": rows,
            "columns": columns,
            "chart": chart_base64
        }

    except Exception as e:
        return {
            "error": str(e),
            "query": sql_query if 'sql_query' in locals() else None
        }