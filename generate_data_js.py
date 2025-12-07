import json
import os
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description='Generate data.js from trades JSON file.')
    parser.add_argument('input_file', nargs='?', default='trades.json', help='Path to the input JSON file (default: trades.json)')
    args = parser.parse_args()

    input_path = args.input_file

    if not os.path.exists(input_path):
        print(f"Error: File '{input_path}' not found.")
        sys.exit(1)

    print(f"Reading from {input_path}...")

    try:
        # Read input json
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Write to web/data.js
        os.makedirs('web', exist_ok=True)
        with open('web/data.js', 'w', encoding='utf-8') as f:
            f.write('const TRADES_DATA = ')
            json.dump(data, f, indent=2)
            f.write(';')
        
        print(f"Successfully created web/data.js from {input_path}")

    except json.JSONDecodeError:
        print(f"Error: '{input_path}' is not a valid JSON file.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
