from flask import Flask, request, jsonify, render_template
import json
import re

app = Flask(__name__)

# Load the FAQ data
with open('faqs.json') as f:
    faqs = json.load(f)

def retrieve_answer(question):
    question = question.lower()
    question_words = set(re.findall(r'\w+', question))

    max_overlap = 0
    best_answer = "Sorry, I do not have the answer to that question."

    for faq in faqs:
        faq_words = set(re.findall(r'\w+', faq['question'].lower()))
        overlap = len(faq_words.intersection(question_words))
        if overlap > max_overlap:
            max_overlap = overlap
            best_answer = faq['answer']

    return best_answer

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    question = data.get('question', '')
    if not question:
        return jsonify({'answer': 'Please ask a question.'})
    answer = retrieve_answer(question)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)