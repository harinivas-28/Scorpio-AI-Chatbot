import os
import google.generativeai as genai
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import pandas as pd
import json
from flask import Flask, render_template, request, redirect, url_for
import markdown

app = Flask(__name__)

# Load environment variables
load_dotenv()

# Initialize Google Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_pdf_text(pdf_paths):
    text = ""
    for pdf_path in pdf_paths:
        pdf_reader = PdfReader(pdf_path)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_txt_text(txt_paths):
    text = ""
    for txt_path in txt_paths:
        with open(txt_path, "r", encoding='utf-8') as file:
            text += file.read()
    return text

def get_csv_text(csv_paths):
    text = ""
    for csv_path in csv_paths:
        df = pd.read_csv(csv_path)
        text += df.to_string(index=False)
    return text

def get_combined_text(uploaded_files):
    combined_text = ""
    for file_path in uploaded_files:
        if file_path.endswith(".pdf"):
            combined_text += get_pdf_text([file_path])
        elif file_path.endswith(".txt"):
            combined_text += get_txt_text([file_path])
        elif file_path.endswith(".csv"):
            combined_text += get_csv_text([file_path])
    return combined_text

def get_gemini_response(query, context=None):
    try:
        model = genai.GenerativeModel('gemini-pro')
        if context:
            prompt=f"Answer the question based on this context: {context}. Question: {query}"
            response = model.generate_content([prompt, query])
        else:
            prompt=f"Answer the question using information from the internet. Question: {query}"
            response = model.generate_content([prompt, query])
        return response.text
    except Exception as e:
        print(f"Error generating response: {e}")
        return None

def history(file_path, question, answer):
    """
    Appends a question-answer pair to a JSON file containing a list of dictionaries.
    
    Parameters:
    - file_path: Path to the JSON file.
    - question: The question to be added.
    - answer: The answer to be added.
    """
    # Load existing data from the JSON file
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            if not isinstance(data, list):
                raise ValueError("JSON file does not contain a list of dictionaries.")
    except FileNotFoundError:
        # If the file does not exist, initialize an empty list
        data = []
    except json.JSONDecodeError:
        # Handle the case where the JSON file is empty or corrupted
        data = []
    except ValueError as e:
        print(e)
        return

    # Append the new question-answer pair to the list
    data.append({'question': question, 'answer': answer})

    # Write the updated list back to the JSON file
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(e)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_question = request.form.get('user_question')
        uploaded_files = request.form.getlist('uploaded_files')

        if user_question:
            if uploaded_files:
                context_text = get_combined_text(uploaded_files)
                response = get_gemini_response(user_question, context=context_text)
            else:
                response = get_gemini_response(user_question)

            history("history.json", user_question, response)
            # Convert Markdown to HTML
            html_response = markdown.markdown(response) 
            return render_template('index.html', response=html_response, user_question=user_question)
    return render_template('index.html')

@app.route('/history')
def show_history():
    try:
        with open('history.json', 'r') as file:
            data = json.load(file)
            for answer in data:
                answer['answer'] = markdown.markdown(answer['answer'])
            return render_template('history.html', history=data)
    except FileNotFoundError:
        return "No history found."

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/clear_history', methods=['POST'])
def clear_history():
    try:
        with open('history.json', 'w') as file:
            json.dump([], file)
        return 'History cleared', 200
    except Exception as e:
        print(f'Error clearing history: {e}')
        return 'Error clearing history', 500


if __name__ == '__main__':
    app.run(debug=True)