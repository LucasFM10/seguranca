from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)

# Configuração do banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///logs.db'  # Nome do banco de dados
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desativa o rastreamento de modificações

db = SQLAlchemy(app)

# Modelo de Log
class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(100))
    method = db.Column(db.String(10))
    path = db.Column(db.String(200))
    location = db.Column(db.String(200))

    def __repr__(self):
        return f"<Log {self.method} {self.path}>"

# Função para obter a geolocalização do IP
def get_geolocation(ip):
    try:
        response = requests.get(f"http://ipinfo.io/{ip}/json", timeout=5)
        data = response.json()
        return f"{data.get('city', 'Unknown')}, {data.get('region', 'Unknown')}, {data.get('country', 'Unknown')} - ISP: {data.get('org', 'Unknown')}"
    except Exception:
        return "Geolocation lookup failed"

# Rota principal (home) - Página estática
@app.route("/", methods=["GET"])
def home():
    return """
    <h1>Bem-vindo à Home do Aplicativo!</h1>
    <p>Esta página não contém informações sobre as requisições.</p>
    """

# Rota de Logs (/logging) - Página dinâmica
@app.route("/logging", methods=["GET"])
def logging():
    logs = Log.query.all()  # Recupera todos os logs do banco de dados
    return render_template("logging.html", logs=logs)

# Rota Honeypot (para registro de requisições indesejadas)
@app.route("/honeypot", defaults={"path": ""}, methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
@app.route("/honeypot/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
def honeypot(path):
    ip_address = request.remote_addr
    location = get_geolocation(ip_address)

    # Cria o log da requisição
    log_entry = Log(ip=ip_address, method=request.method, path=request.path, location=location)

    # Armazena o log no banco de dados
    db.session.add(log_entry)
    db.session.commit()

    return "403 Forbidden - Access Denied", 403

# Cria o banco de dados (apenas na primeira vez)
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
