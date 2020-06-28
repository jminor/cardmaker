# CardMaker

A simple utility to make printable game cards from a CSV spreadsheet, and some template SVGs.

## Example

Starting with [this spreadsheet](example/all+your+base.csv), and a couple of SVG templates, like [this one](example/action.svg), CardMaker will produce images like this:

![Example Image 1](example/output/ALL+YOUR+BASE+ARE+BELONG+TO+US.png)
(in [PNG](example/output/ALL+YOUR+BASE+ARE+BELONG+TO+US.png) and [SVG](example/output/ALL+YOUR+BASE+ARE+BELONG+TO+US.svg) formats)

## Requirements

You will need these things:
- A recent version of Python (tested with 3.8, but any 3+ should work).
- Inkscape (used for rendering SVG to PNG).
- A Windows, Mac, or Linux computer.

## How It Works

Your spreadsheet needs these columns:
- Card Name
- Template
- Copies
- (Plus any other columns you want)

Each row in the spreadsheet will become a card output image.

The `Card Name` field defines the output filename (with a `.png` or `.svg` extension added).

The `Template` field determines which template SVG will be used for that card. You can use a single template for all your cards, or a different one for different types of cards. The example uses 4 templates for 4 types of outputs (rules, back, thing, action).

The `Copies` field determines how many copies of the identical image will be produced when printed. (NOT IMPLEMENTED YET)

Any other columns you include can be used to fill in the template SVG(s) you provide. If a column is not used in a template, it is ignored - so you can have loads of columns for other purposes.

## SVG Templates

The SVG templates that you provide will be filled in with text from each row in your spreadsheet, and then rendered into output SVG and PNG files.

Text substitution is done with Python-style patterns like `{field}`.

For example, you might have an SVG text element with `NAME: {Card Name}` in it. The `{Card Name}` will be replaced with each card's name, as listed in the spreadsheet.

Custom fields can be used also. For example, a text field might have `{Cost}` in it, and you could have a column in your spreadsheet called "Cost" with values in it for each card.

Numbers and strings can be formatted according to the formatting rules in [PEP 3101](https://www.python.org/dev/peps/pep-3101/)

Any column in your spreadsheet can be used anywhere in your template. This can include simple text strings, colors, sizes, snippets of SVG code, or whatever. Keep in mind, however, that if you are creating your SVG template in an application like Inkscape, you may be limited by where you can put strings like `{whatever}` by the editor you are using. If this is problematic, you can always hand-edit the template SVGs in a text editor, to place the substitution patterns where you want them (e.g. for colors, etc.)

## Output Sizes, DPI, etc.

The output size and DPI are determined entirely by the template SVGs. CardMaker uses Inkscape's page area to determine the output region.

## Printing

TODO: Combining output images into grids for easy printing.

