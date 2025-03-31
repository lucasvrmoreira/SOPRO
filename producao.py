from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import os
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
app.secret_key = 'chave-secreta-sicro'  # só pra exibir mensagens

# URL da API da aplicação de estoque (ajuste se for usar no Render)
API_ESTOQUE = os.getenv('API_ESTOQUE_URL')

@app.route('/')
def index():
    return redirect(url_for('ver_saldo'))

@app.route('/saldo')
def ver_saldo():
    try:
        response = requests.get(f'{API_ESTOQUE}/api/saldo')
        saldo = response.json()
    except Exception as e:
        flash('Erro ao conectar com o sistema de estoque', 'danger')
        saldo = []

    return render_template('saldo_producao.html', saldo=saldo)

@app.route('/solicitar', methods=['POST'])
def solicitar():
    tipo = request.form['tipo']
    tamanho = request.form['tamanho']
    quantidade = int(request.form['quantidade'])

    ordem = {
        'tipo': tipo,
        'tamanho': tamanho,
        'quantidade': quantidade
    }

    try:
        response = requests.post(f'{API_ESTOQUE}/api/ordens', json=ordem)
        if response.status_code == 201:
            flash('Solicitação enviada com sucesso!', 'success')
        else:
            flash('Erro ao enviar solicitação', 'danger')
    except Exception as e:
        flash('Erro na comunicação com o sistema de estoque', 'danger')

    return redirect(url_for('ver_saldo'))

if __name__ == '__main__':
    app.run(port=5001, debug=True)
