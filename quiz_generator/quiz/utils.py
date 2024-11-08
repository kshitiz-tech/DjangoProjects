import fitz
import os
import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

def text_extraction(file):

    text =""
      # PyMuPDF
        # Open the uploaded PDF file
    with fitz.open(stream=file.read(), filetype="pdf") as pdf:
        for page_num, page in enumerate(pdf):
            page_text = page.get_text() # Debugging statement
            text += page_text or ""
    return text


def generate_quiz(text):
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages = [{"role":'user', "content":'Create a quiz with questions and answers based on the following text:\n\n{text}'}]

    )
    return response.choices[0].message.content

def quiz_formatter(contents):
    
    question_1_index_start = contents.find('Question 1:')
    question_1_index_end = contents.find('**Answer:**')

    question_1 = contents[question_1_index_start:question_1_index_end]
    return question_1


