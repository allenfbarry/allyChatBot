import nltk
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
from collections import defaultdict
import numpy as np


f = open(r"cor.txt")
corpus=f.read()
tokens = word_tokenize(corpus)

n = 3  
ngrams_model = defaultdict(lambda: defaultdict(lambda: 0))

for ngram in ngrams(tokens, n):
    context = tuple(ngram[:-1])
    word = ngram[-1]
    ngrams_model[context][word] += 1

def generate_text(model, context):
    l=[]
    context = tuple(context)
    c=0
    while c<=5: 
        weighted_choices = [(word, freq) for word, freq in model[context].items()]
        if not weighted_choices:
            c+=1
            continue
        choices, frequencies = zip(*weighted_choices)
        total_frequency = sum(frequencies)
        probabilities = [freq / total_frequency for freq in frequencies]
        probab=max(probabilities)
        next_word=np.random.choice(choices,p=probabilities)
        yield next_word
        if next_word.endswith((".","?","!")):
            break
        
        context = context[1:] + (next_word,)
        

def generate_response(question):
    tokens = word_tokenize(question.lower())
    try:
        n_grams = list(ngrams(tokens, n-1))
        context = n_grams[-1]
        response_generator = generate_text(ngrams_model, context)
        response = [context[-1]]
        for word in response_generator:
            response.append(word)
        
        response = ' '.join(response)
        response = response.capitalize()
        return response
    except:
        return "Tell or ask me something else"
        
# Chatbot loop running
while True:
    question = input("You : ")
    if question.lower()=="bye":
        print("Ally : Bye, talk to you later!")
        break
    elif question.lower()=="goodbye":
        print("Ally : Goodbye!")
        break
    elif question.lower()=="see you":
        print("Ally : See you later!")
        break
    response = generate_response(question)
    print("Ally :",response)
    
    
import json

def lambda_handler(event, context):
    message = event['Records'][0]['SNS']['Message']
    response = generate_response(message)
    return {
        'statusCode': 200,
        'body': json.dumps({'message': response})
    }
