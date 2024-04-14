from django.shortcuts import render
from dotenv import load_dotenv
import os
import google.generativeai as genai
import streamlit as st
import spacy


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
        responsetext=[]
        for chunk in response:
            responsetext.append(chunk.text)
        # print(responsetext)
        textcorpora=""
        for item in responsetext:
            textcorpora+=item
        print(textcorpora)

        # Load the SpaCy English language model
        nlp = spacy.load("en_core_web_sm")

        # Sample text
        # text = "Apple is headquartered in Cupertino, California. Steve Jobs founded Apple."

        # Process the text with SpaCy
        doc = nlp(textcorpora)

        # Get the English stopwords list from SpaCy
        stop_words = spacy.lang.en.stop_words.STOP_WORDS

        # Count the total number of tokens
        total_tokens = len(doc)

        # Count the total number of stopwords
        total_stopwords = sum(1 for token in doc if token.text.lower() in stop_words)

        # Perform Named Entity Recognition (NER)
        entities = [(ent.text, ent.label_) for ent in doc.ents]

        print("Total number of tokens:", total_tokens)
        print("Total number of stopwords:", total_stopwords)
        for entity , labels in entities:
            print(f"Entity: {entity} , Label: {labels}")
        # print("Named Entities:", entities)

        context = {
            'prompt': prompt,
            'response': response,
            'tokens':total_tokens,
            'stopwords': total_stopwords,
            'entities': entities #need to process it
        }
        return render(request, "index.html", context)
    else:
        message="Error"
        return render(request, "index.html",message)
