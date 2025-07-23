

import google.generativeai as genai
genai.configure(api_key="AIzaSyABrlmK4_c2vKClQ13-oCsUb9H_6QCxwEI")
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
prompt = "Write an SQL query to get total sales from a table named 'total_sales'."
response = model.generate_content(prompt)
print(" Gemini's Answer:\n")
print(response.text)
