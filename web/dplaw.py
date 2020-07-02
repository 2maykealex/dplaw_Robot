from flask import Flask, render_template, request, redirect, url_for, json
from pprint import pprint

app = Flask(__name__)

@app.route("/")
def index():
    return redirect(url_for('home'))

@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/abertura")
def abertura():
    return render_template('abertura.html')

@app.route("/abertura/bradesco")
def abertura_bradesco():
    return render_template('abertura_bradesco.html')

@app.route("/abertura/bradesco/default", methods=['POST'])
def abertura_check():
    data = request.form.to_dict()
    pprint(data)
    return render_template('abertura_default.html', data=data)

@app.route("/atualizacao")
def atualizacao():
    return render_template('atualizacao.html')

@app.route("/contrato")
def contrato():
    return render_template('contrato.html')

@app.route("/volumetria")
def volumetria():
    return render_template('volumetria.html')

if __name__ == "__main__":
    app.run(debug=True)