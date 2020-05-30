#!/usr/bin/python3
# *-* coding: utf-8 *-*
"""
    Converts PDFs to text.
"""
import logging
import argparse
import os
import tempfile
import mimetypes
from typing import List

from pdf2image import convert_from_path
from PIL import Image
import pytesseract

PAGE_SEPARATER = "\n" + ("=" * 50) + "\n"


def save_pdf_to_jpg(pdf: str, path: str) -> (str, List[str]):
    """ Saves the given PDF to one JPG per page to the path. 
        :param pdf: str, path to the PDF
        :param path: str, path where to store the images
        :returns str, List[str]: File base name, List of all file names associated
    """
    filenames = []
    logging.debug("Convert PDF to image")
    pages = convert_from_path(pdf, 500)
    logging.info("%s has %s pages", pdf, len(pages))

    for page_num, page in enumerate(pages):
        filename = os.path.join(
            path, "%s_%s.jpg" % (os.path.splitext(os.path.basename(pdf))[0], page_num)
        )
        logging.info("Save page %d to %s", page_num, filename)
        page.save(filename, "JPEG")
        filenames.append(filename)

    return os.path.splitext(os.path.basename(pdf))[0], filenames


def convert_image_to_text(
    base_name: str, images: List[str], output_path: str, add_page_separater: bool = True
) -> str:
    """ Takes images as input and converts their content to text.
        :param base_name: str, file base name
        :param images: List[str], path to the images to read, in order
        :param output_path: str, Where to write the result
        :param add_page_separater: Add PAGE_SEPARATER between pages
        :returns str: file name of the output TXT
    """
    first_page = True
    output_filename = os.path.join(output_path, base_name + ".txt")
    logging.info("Saving results to %s", output_filename)
    logging.debug("PAGE_SEPARATER is %s", add_page_separater)
    with open(output_filename, "w") as output_file:
        for image in images:
            if add_page_separater and not first_page:
                output_file.write(PAGE_SEPARATER)
            text = str(pytesseract.image_to_string(Image.open(image)))
            output_file.write(text)
            first_page = False

    return output_filename


parser = argparse.ArgumentParser(
    description="Convert PDF to text via OCR on JPGs from those PDFs"
)
parser.add_argument(
    "--input",
    type=str,
    required=True,
    help="Path pointing to a PDF or a folder with PDFs to parse",
)
parser.add_argument(
    "--output", type=str, required=True, help="Path where to store the output TXTs"
)
parser.add_argument(
    "--silent",
    action="store_true",
    help="Silence all logging, only show output filenames as result",
)
if __name__ == "__main__":
    args = parser.parse_args()
    if args.silent:
        logging.getLogger().setLevel(logging.ERROR)
    else:
        logging.getLogger().setLevel(logging.DEBUG)

    logging.debug("Creating temporary directory for images")
    with tempfile.TemporaryDirectory() as tmpdirname:
        documents = []
        if os.path.isdir(args.input):
            logging.debug("Input is a directory, searching for PDFs and JPGs")
            for root, dirs, files in os.walk(args.input):
                for filename in files:
                    file_path = os.path.join(root, filename)
                    logging.debug("Found file: %s, path: %s", filename, file_path)
                    if not os.path.isfile(file_path):
                        continue

                    if mimetypes.guess_type(file_path)[0] == "image/jpeg":
                        # Add images directly
                        documents.append(
                            (
                                os.path.splitext(os.path.basename(file_path))[0],
                                [file_path],
                            )
                        )
                    elif mimetypes.guess_type(file_path)[0] != "application/pdf":
                        logging.debug("File '%s' is not PDF", file_path)
                    else:
                        documents.append(save_pdf_to_jpg(file_path, tmpdirname))
        else:
            logging.debug("Input is a file")
            if mimetypes.guess_type(file_path)[0] == "image/jpeg":
                documents.append((os.path.splitext(args.input)[0], [args.input]))
            else:
                documents.append(save_pdf_to_jpg(args.input, tmpdirname))

        output = []
        for document in documents:
            output.append(convert_image_to_text(document[0], document[1], args.output))
        print(",".join(output))  # for stdout, in case a tool wants to process that
else:
    parser.parse_args([])
