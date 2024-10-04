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

def csv_to_json(csv_file_path, delimiter):
    # Read the CSV file and create a dictionary
    data = {}
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=delimiter)
        print(f"CSV file opened: {csv_file}")
        for row in csv_reader:
            if len(row) >= 2:
                variable, ip = row[0], row[1]
                data[variable] = ip
                print(f"Added: {variable} -> {ip}")
            else:
                print(f"Skipped row: {row}")
    print(f"Final data: {data}")
    return json.dumps(data, indent=4)

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

def save_config(config_file, config):
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=4)

def get_ip_addresses():
    ip_addresses = []
    try:
        # Get all IP addresses
        hostname = socket.gethostname()
        ip_addresses = socket.gethostbyname_ex(hostname)[2]
    except Exception as e:
        print(f"Error getting IP addresses: {e}")
    return ip_addresses

def choose_interface(ip_addresses):
    print("Available interfaces:")
    for i, ip in enumerate(ip_addresses):
        print(f"{i+1}. {ip}")
    choice = input("Choose the interface number (or press Enter for all interfaces): ")
    if choice.strip():
        return ip_addresses[int(choice) - 1]
    return ""

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

    # Ask for CSV file
    default_csv = config.get('csv_file', 'test.csv')
    input_csv = input(f"Enter the CSV file name (default: {default_csv}): ").strip() or default_csv
    input_csv = os.path.join(application_path, input_csv)
    
    # Ask for delimiter
    default_delimiter = config.get('delimiter', ',')
    delimiter = input(f"Enter the CSV delimiter (default: '{default_delimiter}'): ").strip() or default_delimiter

    # Update and save config
    config['csv_file'] = os.path.basename(input_csv)
    config['delimiter'] = delimiter
    save_config(config_file, config)

    json_data = csv_to_json(input_csv, delimiter)
    
    # Choose interface
    ip_addresses = get_ip_addresses()
    chosen_interface = choose_interface(ip_addresses)

    with socketserver.TCPServer((chosen_interface, port), JSONHandler) as httpd:
        server_thread = threading.Thread(target=run_server, args=(httpd,))
        server_thread.start()

        print(f"Server is running on port {port}")
        print(f"Serving data from CSV file: {input_csv}")
        print(f"Using delimiter: '{delimiter}'")
        
        if chosen_interface:
            print(f"Server is accessible at: http://{chosen_interface}:{port}")
        else:
            print("Server is accessible at:")
            for ip in ip_addresses:
                print(f"http://{ip}:{port}")
        
        print("Press 'R' to refresh JSON data, 'Q' to quit.")
        
        while True:
            if keyboard.is_pressed('r'):
                json_data = csv_to_json(input_csv, delimiter)
                print("JSON data refreshed.")
                time.sleep(0.5)  # Prevent multiple refreshes on a single press
            elif keyboard.is_pressed('q'):
                break

        shutdown_server(httpd)
        server_thread.join()

    print("Application has been terminated.")
