#!/usr/bin/env python
# SPDX-License-Identifier: MIT

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
        print("ERROR: No template '{}' found at path: {}".format(template_name, path))
        sys.exit(1)
    print("Loading template: {}".format(path))
    with open(path, "r", encoding='utf-8') as template_file:
        return template_file.read()

def load_templates(templates_names):
    for template_name in templates_names:
        template = load_template(template_name)
        templates[template_name] = template

assert(escape("a&b") == "a&amp;b")
assert(unescape("a&amp;b") == "a&b")

def read_table(path):
    with open(path, "r", newline='', encoding='utf-8') as input_file:
        data = list(csv.reader(input_file))
    header = data[0]

    for column in required_columns:
        if column not in header:
            raise Exception("Required column '{}' not found.".format(column))

    # if a cell has an & or other reserved SVG token, we need
    # to escape it.
    def prep(row):
        return [escape(cell) for cell in row]

    # turn the table into a list of dictionaries, indexed by column name
    rows = [OrderedDict(zip(header, prep(row))) for row in data[1:]]
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
    with open(path, "w", newline='\n', encoding='utf-8') as f:
        f.write(svg)

def save_gametable(cards, path):
    output = """
{{
    cards = {{
{}
    }},
    interaction_options = {{}}
}}
"""
    halo = cards.get("Halo")
    halo_img = None
    if halo:
        halo_img = halo["svg_path"].replace(".svg",".png")
    back = cards.get("Back")
    back_img = None
    if back:
        back_img = back["svg_path"].replace(".svg",".png")
    card_specs = []
    x,y,z = 0,0,0
    for card in cards.values():
        if card["name"] in ("Back", "Halo"):
            continue
        img = card["svg_path"].replace(".svg",".png")
        card_spec = """
        ["{}"] = {{
            id = "{}",
            img = "http:{}",
            back_img = "http:{}",
            halo_img = "http:{}",
            pos = vec3({},{},{}),
            rotation = 0,
            scale = 1,
            facing_up = true
        }}""".format(
            card["id"],
            card["id"],
            img,
            back_img,
            halo_img,
            x,y,z
        )
        card_specs.append(card_spec)
        z+=1
    result = output.format(",\n".join(card_specs))
    with open(path, "w", newline='\n', encoding='utf-8') as f:
        f.write(result)


def render_svgs(svg_paths):
    # Render them all in a batch for speed
    # The startup cost for Inkscape is pretty high...
    cmd = [
        args.inkscape,
        "--export-area-page",
        "--export-type=png"
    ]
    output = subprocess.check_call(
        cmd + svg_paths,
        stderr=subprocess.STDOUT
    )
    print(output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Make playing card images from a CSV and template SVGs."
    )
    parser.add_argument(
        '--data', '-d',
        help='input CSV table containing card data',
        type=str, required=True
    )
    parser.add_argument(
        '--templates', '-t',
        help='folder containing template SVGs',
        default='', type=str
    )
    parser.add_argument(
        '--output', '-o',
        help='output folder',
        type=str, required=True
    )
    parser.add_argument(
        '--inkscape',
        help='path to Inkscape executable',
        default=default_inkscape_path, type=str
    )
    parser.add_argument(
        '--gametable',
        help='output a GameTable .lua file',
        type=str
    )
    args = parser.parse_args()

    rows = read_table(args.data)
    
    load_templates(set([row['Template'] for row in rows]))

    card_names = set()
    svg_paths = []

    cards = {}

    for row in rows:
        name = row['Card Name']
        template = templates[row['Template']]
        copies = int(row['Copies'])
        
        if name in card_names:
            print("WARNING: Duplicate Card Name '{}' ignored.".format(name))
            continue
        else:
            card_names.add(name)

        svg = fill_template(template, row)

        for index in range(copies):
            if copies == 1:
                copy_number = ""
            else:
                copy_number = "_{}".format(index+1)

            id = "{}{}".format(
                name,
                copy_number
            )
            svg_path = os.path.join(args.output, id+".svg")
            save_svg(svg, svg_path)
            svg_paths.append(svg_path)
            cards[id] = {
                "id": id,
                "name": name,
                "row": row,
                "svg_path": svg_path
            }

    print("Rendering SVG to PNG...")

    # On Windows, we need to make sure our normal
    # output is flushed, otherwise Inkscape's output
    # appears before ours which is confusing...
    sys.stdout.flush()
    sys.stderr.flush()

    render_svgs(svg_paths)

    if args.gametable:
        save_gametable(cards, args.gametable)
