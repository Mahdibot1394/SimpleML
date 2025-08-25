import sys
import os
from simpleML_parser import SimpleMLParser

def convert_sml_to_html(sml_path):
    # Read .sml file
    with open(sml_path, 'r', encoding='utf-8') as f:
        sml_content = f.read()
    # Parse to HTML
    parser = SimpleMLParser(sml_content)
    html_content = parser.parse()
    # Write to .html file
    html_path = os.path.splitext(sml_path)[0] + '.html'
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Converted {sml_path} to {html_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python sml_to_html.py <file.sml>")
        sys.exit(1)
    input_file = sys.argv[1]
    if not os.path.isfile(input_file) or not input_file.endswith('.sml'):
        print("Please provide a valid .sml file.")
        sys.exit(1)
    convert_sml_to_html(input_file)