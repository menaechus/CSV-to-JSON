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
import netifaces  # You'll need to install this: pip install netifaces

# Global variable to store the JSON data
json_data = ""

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
        global json_data
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')  # Allow all origins
        self.end_headers()
        
        try:
            self.wfile.write(json_data.encode('utf-8'))
            print(f"Served data: {json_data[:100]}...")  # Print first 100 chars for debugging
        except Exception as e:
            print(f"Error serving data: {e}")
    
    def log_message(self, format, *args):
        print(f"Request: {self.command} {self.path}")
        print(f"Status: {args[1]}")

def run_server(server):
    print(f"Serving JSON data on port {server.server_address[1]}")
    server.serve_forever()

def shutdown_server(server):
    print("\nShutting down the server...")
    server.shutdown()
    server.server_close()
    print("Server has been shut down.")

def load_config(config_file):
    with open(config_file, 'r') as f:
        return json.load(f)

def get_network_interfaces():
    interfaces = []
    for interface in netifaces.interfaces():
        try:
            if netifaces.AF_INET in netifaces.ifaddresses(interface):
                for link in netifaces.ifaddresses(interface)[netifaces.AF_INET]:
                    interfaces.append((interface, link['addr']))
        except ValueError:
            pass  # Skip interfaces that don't have an IPv4 address
    return interfaces

if __name__ == "__main__":
    config = {}
    config_file = 'config.json'
    config_updated = False

    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
    
    if 'port' not in config:
        config['port'] = int(input("Enter the port number: "))
        config_updated = True
    else:
        config['port'] = int(config['port'])  # Ensure port is always an integer
    
    if 'csv_file' not in config:
        config['csv_file'] = input("Enter the CSV filename: ")
        config_updated = True
    
    # Get network interfaces
    interfaces = get_network_interfaces()
    
    if 'interface' not in config or config['interface'] not in [ip for _, ip in interfaces]:
        print("Available network interfaces:")
        for i, (name, ip) in enumerate(interfaces):
            print(f"{i+1}. {name}: {ip}")
        choice = int(input("Choose the interface number to bind to: ")) - 1
        config['interface'] = interfaces[choice][1]
        config_updated = True
    
    if config_updated:
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        print("Config file updated with new inputs.")

    # Get the directory of the executable
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))

    input_csv = os.path.join(application_path, config.get('csv_file', 'test.csv'))  # Default to 'test.csv' if not specified

    json_data = csv_to_json(config['csv_file'])
    print(f"Initial JSON data: {json_data[:100]}...")  # Print first 100 chars for debugging
    
    port = config['port']  # This is now guaranteed to be an integer
    interface = config['interface']
    httpd = socketserver.TCPServer((interface, port), JSONHandler)
    server_thread = threading.Thread(target=run_server, args=(httpd,))
    server_thread.start()

    print(f"Serving data from CSV file: {config['csv_file']}")
    print(f"Server is accessible at: http://{interface}:{port}")
    
    print("Server is running. Press 'r' to refresh JSON from CSV, or 'q' to quit.")
    while True:
        command = input().lower()
        if command == 'q':
            break
        elif command == 'r':
            # Refresh JSON from CSV
            json_data = csv_to_json(config['csv_file'])
            print("JSON refreshed from CSV.")
        else:
            print("Invalid command. Use 'r' to refresh or 'q' to quit.")
    
    shutdown_server(httpd)
    server_thread.join()

    print("Application has been terminated.")
