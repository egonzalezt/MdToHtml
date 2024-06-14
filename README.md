# Markdown to HTML Converter

This script converts a Markdown file into an HTML file using a specified template and CSS. It also offers the option to convert images to base64 within the HTML. Additionally, it logs if any videos in the Markdown should be included for proper HTML functionality.

<p align="center"><a target="_blank"><img src="./logo.png" width="200"></a></p>

## Installation

Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

Then run:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

The script can be executed with the following mandatory argument:

* --md-path: Path to the Markdown file.

```bash
python md-to-html.py --md-path=./readme.md
```

## Optional Arguments

* `--template-path`: Path to the HTML template file (default: template.html).
* `--css-path`: Path to the CSS file (default: styles.css).
* `--encoding`: Encoding of the files (default: `utf-8`).
* `--image-to-base64`: Convert images to base64 in the HTML (1, true, True for yes, 0, false, False for no; default: 1).

Example with all optional arguments:

```bash
python md-to-html.py --md-path=./readme.md --template-path=./template.html --css-path=./styles.css --encoding=utf-8 --image-to-base64=true
```

## Arguments

* `--md-path`: (**Required**) Path to the Markdown file to be converted.
* `--template-path`: (*Optional*) Path to the HTML template file. Default is template.html.
* `--css-path`: (*Optional*) Path to the CSS file. Default is styles.css.
* `--encoding`: (*Optional*) Encoding of the files. Default is `utf-8`.
* `--image-to-base64`: (*Optional*) Convert images to base64 in the HTML. Accepts 1, true, True for enabling, 0, false, False for disabling. Default is 1.

## Logging

If the Markdown file contains videos, the script will log the presence of these videos and suggest including them for proper functionality in the HTML.

## License

This project is licensed under the [Apache 2.0 license](./LICENSE).