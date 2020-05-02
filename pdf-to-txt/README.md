# PDF to Text
Converts PDFs to images and then to text.

## CLI
### Installation
`pipenv install --deploy --ignore-pipfile`

### Usage
To display the command line arguments, just run
```sh
$pipenv run python3 src/main.py --help
usage: main.py [-h] --input INPUT --output OUTPUT [--silent]

Convert PDF to text via OCR on JPGs from those PDFs

optional arguments:
  -h, --help       show this help message and exit
  --input INPUT    Path pointing to a PDF or a folder with PDFs to parse
  --output OUTPUT  Path where to store the output TXTs
  --silent         Silence all logging, only show output filenames as result
```

Use the `--silent` flag if you wish to process the output files with other programs alone a pipe.
Only the outfiles files, delimited by `,` will be outputted (logging will be set to error).

## Docker
### Installation
`docker build -t pdf2text:latest .`

### Usage
The `Dockerfile` will mount to `VOLUMES` to `/input` and `/output`. Assign them to local folders you want to use.

```sh
PDF_INPUT_DIR="/tmp/pdf_parser_input"
TXT_OUTPUT_DIR="/tmp/pdf_parser_out"

# Convert PDFs to TXTs
docker run -v ${PDF_INPUT_DIR}:/input -v ${TXT_OUTPUT_DIR}:/output -t pdf2text:latest
```
