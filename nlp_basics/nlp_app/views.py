from django.shortcuts import render
from dotenv import load_dotenv
import os
import google.generativeai as genai
import streamlit as st

load_dotenv()  # Load environment variables

# Configure Google API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

# Create your views here.
def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

def index(request):
    return render(request, "index.html")

def prompt_processing(request):
    if request.method== "POST":
        prompt= request.POST.get("prompt")
        response = get_gemini_response(prompt)
        context = {
            'prompt': prompt,
            'response': response
        }
        return render(request, 'response.html', context)
    else:
        return render(request, "index.html")
