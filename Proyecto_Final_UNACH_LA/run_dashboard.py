import http.server
import socketserver
import webbrowser
import os

PORT = 8000
DIRECTORY = "06_Dashboard_Interactivo"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

# Move to the root directory where the python script is, 
# but the handler needs to serve from root to access both 06_Dashboard_Interactivo AND 03_ / 04_ for data.
# Wait, if we serve from root, the user goes to http://localhost:8000/06_Dashboard_Interactivo/

class RootHandler(http.server.SimpleHTTPRequestHandler):
    pass

def main():
    print(f"Iniciando el servidor del Dashboard UNACH-LA...")
    
    with socketserver.TCPServer(("", PORT), RootHandler) as httpd:
        url = f"http://localhost:{PORT}/06_Dashboard_Interactivo/"
        print(f"Servidor corriendo en el puerto {PORT}")
        print(f"Abriendo el dashboard en tu navegador web: {url}")
        
        # Abre el navegador automáticamente
        webbrowser.open(url)
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor detenido.")

if __name__ == "__main__":
    main()
