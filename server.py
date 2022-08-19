from projecao_hiperdimensional import projetor
from flask import Flask, render_template, request
import json

app = Flask("Recomendador de empresa")


@app.route("/")
def renderIndexPage():
    # Write the code to render template
    return render_template("index.html")

@app.route("/recomendador")
def projecao():
    return answer



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
