from flask import Flask, request, render_template_string
from flask_socketio import SocketIO, emit
import requests

app = Flask(__name__)
socketio = SocketIO(app)

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

# Rota Home - Página estática
@app.route("/", methods=["GET"])
def home():
    return """
    <h1>Bem-vindo à Home do Aplicativo!</h1>
    <p>Esta página não contém informações sobre as requisições.</p>
    """

# Rota de Logs - Página dinâmica
@app.route("/logging", methods=["GET", "POST"])
def logging():
    return render_template_string("""
    <h1>Página de Logs (Atualização Dinâmica)</h1>
    <div id="logs"></div>
    <script src="https://cdn.socket.io/4.5.1/socket.io.min.js"></script>
    <script type="text/javascript">
        var socket = io.connect('http://' + document.domain + ':' + location.port);
        socket.on('new_log', function(data) {
            var logsDiv = document.getElementById("logs");
            logsDiv.innerHTML += "<p><b>" + data.method + "</b> " + data.path + " - " + data.location + "</p>";
        });
    </script>
    """)

# Rota Honeypot (para registro de requisições indesejadas)
@app.route("/honeypot", defaults={"path": ""}, methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
@app.route("/honeypot/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
def honeypot(path):
    ip_address = request.remote_addr
    location = get_geolocation(ip_address)
    
    log_entry = {
        'ip': ip_address,
        'method': request.method,
        'path': request.path,
        'location': location
    }
    
    # Adiciona o log à lista
    request_logs.append(log_entry)

    # Emite o novo log para os clientes conectados ao socket
    socketio.emit('new_log', log_entry)

    return "403 Forbidden - Access Denied", 403

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8080)
