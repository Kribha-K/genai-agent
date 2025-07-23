# genai-agent
GenAI intern project: AI Agent to Answer E-commerce Data Questions

1.Converts user questions into SQL using Gemini Pro (LLM).
2.Runs the query on a local ecommerce.db database.
3.Returns clean, structured results (JSON format).

How It Works
Run main.py to load CSV files into ecommerce.db.

Start the FastAPI server by using
uvicorn visualization:app --reload
Open http://127.0.0.1:8000/docs to test your questions.

