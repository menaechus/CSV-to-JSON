# CSV to JSON Server

## Description
CSV to JSON Server is a Windows application that converts CSV files to JSON format and serves the data via a simple HTTP server. This tool is designed for easy data conversion and sharing, with features for dynamic updates and basic server controls.

## Features
- Convert CSV files to JSON format
- Serve JSON data via a simple HTTP server
- Configuration file support for port and CSV filename
- User selection of network interface from available options
- Dynamic JSON data refresh without server restart
- Terminal-based controls (R for refresh, Q to quit)

## System Requirements
- Windows 32-bit or 64-bit operating system
- Python 3.x (if running from source)

## Installation
1. Download the latest `csv2json.exe` from the [Releases](https://github.com/yourusername/csv-to-json-server/releases) page.
2. Place the executable in a directory of your choice.

## Usage
1. Run `csv2json.exe`.
2. You'll be prompted to enter:
   - CSV filename (will add .csv extension if missing)
   - CSV delimiter
   - Select a network interface from the list of available interfaces
3. These settings will be saved in a `config.json` file for future use.
4. Once the server starts, you'll see the specific address where it's accessible.
5. Use the following commands in the terminal:
   - `R`: Refresh JSON data from the CSV file
   - `Q`: Quit the application

## CSV File Format
- The CSV file should be in the same directory as the executable.
- The delimiter can be specified when running the application.

## Configuration
A `config.json` file will be created in the same directory as the executable, storing:
- `port`: The port number for the HTTP server
- `csv_file`: The name of the CSV file to convert
- `delimiter`: The delimiter used in the CSV file

## Known Limitations
- Windows-only support in the current release
- Limited error handling for malformed CSV files

## Future Improvements
- Cross-platform support (Mac, Linux)
- Enhanced data validation and error reporting
- GUI for easier configuration and monitoring

## Contributing
Contributions to the CSV to JSON Server project are welcome! Please feel free to submit pull requests, create issues or spread the word.

## Contact
For support or queries, please open an issue on this GitHub repository.
