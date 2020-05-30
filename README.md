# doc-metaguesser
Tries to guess meta information of documents for storing that into a relational model.
This is a personal project I use to improve searchability for documents I receive (digitally or physically+scanned).

I collect my documents in a NAS, which is where this project is running on.

It consists of two parts:
* `pdf-to-text`: This program converts PDFs to text, by converting them to images and then using OCR to read the contents into a TXT
* `txt-metaguesser`: This program reads textfiles and tries to make educated guesses about meta information

Additionally there is a bash script controlling the whole process, in case you want to run it all together (like me).


