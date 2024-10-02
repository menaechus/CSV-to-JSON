import csv
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import socketserver
import threading
import sys
import time
import socket
import os
import keyboard

def csv_to_json(csv_file_path):
    # Read the CSV file and create a dictionary
    data = {}
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')  # Use semicolon as delimiter
        print(f"CSV file opened: {csv_file}")
        for row in csv_reader:
            if len(row) >= 2:
                name = row[0]
                address = row[1]
                data[name] = address
                print(f"Added: {name} -> {address}")
            else:
                print(f"Skipped row: {row}")
    print(f"Final data: {data}")
    return json.dumps([data], indent=4)

class JSONHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json_data.encode())

def run_server(server):
    print(f"Serving JSON data on port {port}")
    server.serve_forever()

def shutdown_server(server):
    print("\nShutting down the server...")
    server.shutdown()
    server.server_close()
    print("Server has been shut down.")

def load_config(config_file):
    with open(config_file, 'r') as f:
        return json.load(f)

def get_ip_addresses():
    ip_addresses = []
    try:
        # Get all IP addresses
        hostname = socket.gethostname()
        ip_addresses = socket.gethostbyname_ex(hostname)[2]
    except Exception as e:
        print(f"Error getting IP addresses: {e}")
    return ip_addresses

if __name__ == "__main__":
    # Get the directory of the executable
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))

    config_file = os.path.join(application_path, "config.json")

    # Load configuration
    config = load_config(config_file)
    port = config.get('port', 8000)  # Default to 8000 if not specified
    input_csv = os.path.join(application_path, config.get('csv_file', 'test.csv'))  # Default to 'test.csv' if not specified

    json_data = csv_to_json(input_csv)
    
    with socketserver.TCPServer(("", port), JSONHandler) as httpd:
        server_thread = threading.Thread(target=run_server, args=(httpd,))
        server_thread.start()

        print(f"Server is running on port {port}")
        print(f"Serving data from CSV file: {input_csv}")
        
        # Get and display IP addresses
        ip_addresses = get_ip_addresses()
        if ip_addresses:
            print("Server is accessible at:")
            for ip in ip_addresses:
                print(f"http://{ip}:{port}")
        else:
            print("Could not determine server IP addresses.")
        
        print("Press Ctrl+Q to shut down the server.")
        
        # Wait for Ctrl+Q
        keyboard.wait('ctrl+q')
        
        shutdown_server(httpd)
        server_thread.join()

    print("Application has been terminated.")
