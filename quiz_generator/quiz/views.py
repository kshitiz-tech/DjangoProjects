from django.shortcuts import render
from .forms import PDFUploadForm
from .utils import text_extraction
from .utils import generate_quiz, quiz_formatter
from .models import UploadFile
import openai
import json
import requests
import ast






# Create your views here.

def index(request):

    return render(request,'index.html')


def quiz_generator(request):
    global questions
    global answers
    if request.method == "POST":
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():

            pdf_file = form.cleaned_data.get('file')
            # Save the PDF temporarily
            obj = form.save(commit=False)
            obj.file = pdf_file
            obj.save()
            
            '''with obj.file.open('wb') as f:
                for chunk in pdf_file.chunks():
                    f.write(chunk)'''
            #extract text and generate quiz
            text = text_extraction(obj.file)
            system_prompt = f"Create a quiz with questions and answers based on the following text:\n\n{text}"
            system_prompt += "Organize the following multiple-choice quiz questions, choices, and answers into separate Python lists or dictionaries. The goal is to store each element clearly and efficiently for further use:\n\n1. Use a list named 'questions' where each item is a dictionary containing a 'question' key with the question text , an 'options' key with a dictionary of answer choices (e.g., 'a', 'b', 'c', 'd'). and an 'answer' key with value of particular answer\n2.\n\nHere’s an example format:\n\nquestions = [\n    {\n        'question': 'Question text',\n        'options': {'a': 'Choice A', 'b': 'Choice B', 'c': 'Choice C', 'd': 'Choice D'},\n ''answer' :'correct_answer_choice'  },\n ]\n\nPlease follow this structure when organizing the quiz data."
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{
                    'role':'system',
                    'content': 'Your response should be JSON format'
                },
                {
                    "role": "user",
                    "content": system_prompt,
                    
                }],
                response_format={'type':'json_object'}
            )
            quiz = response.choices[0].message.content
            data = json.loads(quiz)
            '''for datum in data:
                question_text = datum[0]
                options = datum[1]
                correct_answer = datum[2]
                print(f"Question: {question_text}")
                print(f"Options: {options}")
                print(f"Correct Answer: {correct_answer}") '''
            
            
            return render(request, "quiz.html", {"data": data})
    else:
        form = PDFUploadForm()
    return render(request, "upload.html", {"form": form})


