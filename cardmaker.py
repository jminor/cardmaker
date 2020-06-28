#!python

import argparse
import re
import subprocess
import csv
import os
import sys
from xml.sax.saxutils import escape, unescape
from collections import OrderedDict

default_inkscape_paths = [
    "C:/Program Files/Inkscape/bin/inkscape.exe",
    "/Applications/Inkscape.app/Contents/MacOS/Inkscape"
]
default_inkscape_path = None
for path in default_inkscape_paths:
    if os.path.exists(path):
        default_inkscape_path = path

# foo = OrderedDict()
# foo['hey'] = 'Hello'
# foo['bye'] = 'Goodbye'
# assert(list(foo.values())[0] == 'Hello')
# assert(list(foo.values())[1] == 'Goodbye')

required_columns = [
    'Card Name',
    'Template',
    'Copies'
]

# templates['name'] = '<svg>...</svg>'
templates = {}

def load_template(template_name):
    path = os.path.join(args.templates, template_name) + ".svg"
    if not os.path.isfile(path):
        print("ERROR: No template '{}' found here: {}".format(template_name, path))
        sys.exit(1)
    with open(path, "r", encoding='utf-8') as template_file:
        return template_file.read()

def load_templates(templates_names):
    for template_name in templates_names:
        print("Loading template {}...".format(template_name))
        template = load_template(template_name)
        templates[template_name] = template

def read_table(path):
    with open(path, "r", newline='', encoding='utf-8') as input_file:
        data = list(csv.reader(input_file))
    header = data[0]

    for column in required_columns:
        if column not in header:
            raise Exception("Required column '{}' not found.".format(column))

    # turn the table into a list of dictionaries, indexed by column name
    rows = [OrderedDict(zip(header, row)) for row in data[1:]]
    return rows

def fill_template(template, row):
    return template.format(*row.values(), **row)

actual = fill_template(
    "test {0} of {1} the {thing} template {1} system {buzz}",
    OrderedDict([
        ("Card Name", "name"),
        ("Template", "test"),
        ("thing", "value1"),
        ("buzz", "value2"),
        ("unused", "value3")
    ])
)
desired = "test name of test the value1 template test system value2"
if actual != desired:
    print(actual)
assert(actual == desired)

def save_svg(svg, path):
    print("Saving SVG: {}".format(path))
    with open(path, "w", encoding='utf-8') as f:
        f.write(svg)

def render_svg(input_path, output_path):
    print("Rendering SVG: {} to: {}".format(input_path, output_path))
    sys.stdout.flush()
    status = subprocess.call(
        [
            args.inkscape,
            input_path,
            # "--export-width", output_width,
            "--export-area-page",
            "--export-filename", output_path
        ],
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE
    )
    if status:
        print("ERROR: Rendering failed.")
        sys.exit(status)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Make playing card images from a CSV and template SVGs.")
    parser.add_argument('--data', '-d', help='input CSV table containing card data', type=str, required=True)
    parser.add_argument('--templates', '-t', help='folder containing template SVGs', default='.', type=str)
    parser.add_argument('--output', '-o', help='output folder', type=str, required=True)
    parser.add_argument('--inkscape', help='path to Inkscape executable', default=default_inkscape_path, type=str)
    args = parser.parse_args()

    rows = read_table(args.data)
    
    load_templates(set([row['Template'] for row in rows]))

    cards = OrderedDict()

    for row in rows:
        name = row['Card Name']
        template = templates[row['Template']]
        copies = int(row['Copies'])
        
        if name in cards:
            print("WARNING: Duplicate Card Name '{}' ignored.".format(name))

        svg = fill_template(template, row)
        output_base = os.path.join(args.output, name)
        svg_path = output_base+'.svg'
        png_path = output_base+'.png'
        save_svg(svg, svg_path)
        render_svg(svg_path, png_path)

