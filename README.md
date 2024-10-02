# CSV to JSON Server

## Description
CSV to JSON Server is a Windows application that converts CSV files to JSON format and serves the data via a simple HTTP server. This tool is designed for easy data conversion and sharing, with features for dynamic updates and basic server controls.

## Features
- Convert CSV files to JSON format
- Serve JSON data via a simple HTTP server
- Configuration file support for port, CSV filename, and network interface
- User selection of network interface from available options
- Dynamic JSON data refresh without server restart
- Terminal-based controls (r for refresh, q to quit)
- Cross-Origin Resource Sharing (CORS) support
- Debug logging for troubleshooting

## System Requirements
- Windows 32-bit or 64-bit operating system

## Installation
1. Download the latest `csv2json.exe` from the [Releases](https://github.com/yourusername/csv-to-json-server/releases) page.
2. Place the executable in a directory of your choice.

## Usage
1. Run `csv2json.exe`.
2. If running for the first time, you'll be prompted to enter:
   - Port number for the server
   - CSV filename
   - Select a network interface from the list of available interfaces
3. These settings will be saved in a `config.json` file for future use.
4. Once the server starts, you'll see the specific address where it's accessible.
5. Use the following commands in the terminal:
   - `r`: Refresh JSON data from the CSV file
   - `q`: Quit the application

## CSV File Format
- The CSV file should use semicolon (;) as the delimiter.
- Place the CSV file in the same directory as the executable.

## Configuration
A `config.json` file will be created in the same directory as the executable, storing:
- `port`: The port number for the HTTP server
- `csv_file`: The name of the CSV file to convert
- `interface`: The IP address of the selected network interface

## Known Limitations
- Windows-only support in the current release
- CSV must use semicolon (;) as delimiter
- Limited error handling for malformed CSV files

## Future Improvements
- Cross-platform support (Mac, Linux)
- Support for different CSV delimiters
- Ability to specify CSV file location
- Enhanced data validation and error reporting

## Contributing
Contributions to the CSV to JSON Server project are welcome! Please feel free to submit pull requests, create issues or spread the word.


## Contact
For support or queries, please open an issue on this GitHub repository.
