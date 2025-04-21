from flask import Flask, request, render_template
import requests
import json

app = Flask(__name__)

# Lista para armazenar logs em memória
request_logs = []

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
    # Exibe os logs na página
    return render_template("logging.html", logs=request_logs)

# Rota Honeypot (para registro de requisições indesejadas)
@app.route("/honeypot", defaults={"path": ""}, methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
@app.route("/honeypot/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
def honeypot(path):
    ip_address = request.remote_addr
    location = get_geolocation(ip_address)

    # Cria o log da requisição
    log_entry = {
        'ip': ip_address,
        'method': request.method,
        'path': request.path,
        'location': location
    }

    # Armazena o log na lista
    request_logs.append(log_entry)

    # Também salvar no arquivo
    with open("projeto/honeypot.log", "a") as log_file:
        print("aaa")
        log_file.write(json.dumps(log_entry) + "\n")

    # Emite a resposta
    return "403 Forbidden - Access Denied", 403

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
