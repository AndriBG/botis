from flask import Flask, render_template, jsonify, make_response, request
import re  # librería para expresiones regulares
import random
import json

from flask.wrappers import Request  # librería para genenal un número random
from messages import responses, questions # importar la base de conocimiento

def get_response(user_input):
    split_message = re.split(r'\s|[,:;.?!-_]\s*', user_input.lower()) # limpiar el input del usuario
    response = check_all_messages(split_message)
    return response

# función que determina el porcentaje del posible mensaje a responder
# parámetros: mensaje del usuario, palabras reconocidas, una sola respuesta o varias, y palabra requerida
def message_probability(user_message, recognized_words, single_response=False, required_word=[]):
    message_certainty = 0 # por cada respuesta la certeza siempre reinicia
    has_required_words = True # igual para las palabras requeridas en true.

    #recorrer las palabras reconocidas con las que cuenta actualmente nuestro bot.
    for word in recognized_words:
        if word in user_message:
            message_certainty += 1 # cuenta las palabras reconocidas en el mensaje del usuario

    # dividir la cantidad de certezas entre las palabras reconocidas, sacando el porcentaje
    percentage = float(message_certainty) / float(len(recognized_words))

    for word in required_word:
        if word not in user_message: # determina si no hay palabras requeridas dentro del mensaje del usuario
            has_required_words = False
            break

    # si tiene palabras requeridas o si la respuesta es única, devuelve el porcentaje
    if has_required_words or single_response:
        return int(percentage * 100)
    else: # sino retorna 0
        return 0

# verifica el mensaje usuario, en todos los demás mensajes
def check_all_messages(message):
        highest_prob = {}

        # 
        def response(bot_response, list_of_words, single_response=False, required_words=[]):
            nonlocal highest_prob # indica que la variable highest_prob no es local en este método "response"
            highest_prob[bot_response] = message_probability(
                message, list_of_words, single_response, required_words) # usa la función message_probability para determinar el porcentaje del mensaje del usuario en la lista de palabras reconocidas

        # recorre todas las preguntas y respuestas que tiene
        for r, q in zip(responses, questions):
            response(bot_response = r, list_of_words = q, single_response=True) # esta llamada modifica a "highest_prob"
        
        # busca la conincidencia máxima en highest_prob
        best_match=max(highest_prob, key=highest_prob.get)

        # si no encuentra conincidencia devuelve la función "unknown" de lo contrario devuelve la respuesta
        return unknown() if highest_prob[best_match] < 1 else best_match

# devuelve una respuesta aleatoria, para cuando no haga match
def unknown():
    response=['puedes decirlo de nuevo?', 'No estoy seguro de lo quieres',
        'búscalo en google a ver que tal'][random.randrange(3)]
    return response

# una instancia de la librería Flask
application = Flask(__name__)

# este es un endpoint que puede ser consultado tanto por GET como POST
@application.route('/botis', methods=['POST'])
def response_server():
    if request.is_json:
        req = request.get_json()
        response = {
            "message": get_response(req.get("field_text"))
        }
        res = make_response(jsonify(response), 200)
        print(res)
        return res # devuelve la respuesta en formato json
    else:
        res = make_response(jsonify({"message":"No JSON Received"}), 400)
        return  "No JSON received", 400

# para correr el servidor, por el puerto 5300
if __name__ == '__main__':
    # application.run(debug = True, port = 5500)
    application.run()
    # application.run("0.0.0.0", port = 5300)
