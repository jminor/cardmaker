# CardMaker

A simple utility to make printable game cards from a CSV spreadsheet, and some template SVGs.

## Requirements

You will need these things:
- A recent version of [Python](https://python.org/) (tested with 3.8, but any 3+ should work).
- [Inkscape](https://inkscape.org/) (used for rendering SVG to PNG).
- A Windows, Mac, or Linux computer (tested on Windows).

## Installation

To install CardMaker, you can [download a zip](https://github.com/jminor/cardmaker/archive/master.zip) or use git from the command line:

```
% git clone https://github.com/jminor/cardmaker.git
% cd cardmaker
% python cardmaker.py --help
```

## Example

This repo includes a small example game called [All Your Base](http://www.dvorakgame.co.uk/index.php/All_Your_Base_deck) designed by [Kevan](http://www.dvorakgame.co.uk/index.php/User:Kevan) as part of the game [Dvorak](https://boardgamegeek.com/boardgame/9010/dvorak). That game is not part of this software, and may be subject to copyright.

Starting with [this spreadsheet](example/all_your_base.csv), and a couple of SVG templates, like [this one](example/action.svg), CardMaker will produce images like this:

![Example Image 1](example/output/ALL%20YOUR%20BASE%20ARE%20BELONG%20TO%20US.png)
![Example Image 2](example/output/Setup.png)

(in [PNG](example/output/ALL%20YOUR%20BASE%20ARE%20BELONG%20TO%20US.png) and [SVG](example/output/ALL%20YOUR%20BASE%20ARE%20BELONG%20TO%20US.svg) formats)

To run CardMaker on the example, do this:

```
% cd cardmaker/example
% python ../cardmaker.py --data all_your_base.csv --output output/
```

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

## A Note About SVG Rendering

SVG is a very powerful and flexible format for Scalable Vector Graphics. There are many implementations of SVG rendering, many of which differ in some details. As such, you may notice that the SVG templates, and SVG output files look different in your browser than they do in Inkscape, or in other programs. If you want your cards to look perfect, then I suggest that you use Inkscape to make your template (since CardMaker uses it for rendering) and then use a high resolution PNG output for printing.

## Output Sizes, DPI, etc.

The output size and DPI are determined entirely by the template SVGs. CardMaker uses Inkscape's page area to determine the output region.

## Printing

TODO: Combining output images into grids for easy printing.

