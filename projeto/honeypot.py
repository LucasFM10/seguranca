from flask import Flask, request, render_template
import requests

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

# Rota principal
@app.route("/", methods=["GET", "POST"])
def home():
    # Captura a requisição
    ip_address = request.remote_addr
    method = request.method
    path = request.path
    headers = dict(request.headers)
    location = get_geolocation(ip_address)

    # Armazena os logs na lista
    log_entry = {
        'ip': ip_address,
        'method': method,
        'path': path,
        'location': location,
        'headers': headers
    }
    request_logs.append(log_entry)

    # Exibe as requisições na página inicial
    return render_template("index.html", logs=request_logs)

# Rota Honeypot (para registro de requisições indesejadas)
@app.route("/honeypot", defaults={"path": ""}, methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
@app.route("/honeypot/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
def honeypot(path):
    ip_address = request.remote_addr
    location = get_geolocation(ip_address)

    # Log da requisição
    log_entry = f"Intruder Alert! IP: {ip_address}, Location: {location}, Method: {request.method}, Path: {request.path}, Headers: {dict(request.headers)}"
    print(log_entry)  # Também exibe no console para monitoramento

    return "403 Forbidden - Access Denied", 403

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
