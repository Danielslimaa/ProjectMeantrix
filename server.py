from biblioteca import projetor
from flask import Flask, render_template, request
import json

from biblioteca.projetor import proj

app = Flask("Recomendador de empresas")

@app.route("/projecao")
@app.route("/englishToFrench")
def englishToFrench():
    textToTranslate = request.args.get('textToTranslate')
    answer = proj(textToTranslate)
    return answer

@app.route("/frenchToEnglish")
def frenchToEnglish():
    textToTranslate = request.args.get('textToTranslate')
    answer = proj(textToTranslate)#translator.french_to_english(textToTranslate)
    return answer

@app.route("/")
def renderIndexPage():
    # Write the code to render template
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
