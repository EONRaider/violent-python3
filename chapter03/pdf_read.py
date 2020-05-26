import argparse
from PyPDF4 import PdfFileReader


def print_meta(filename):
    with open(filename, 'rb') as pdf:
        pdf_file = PdfFileReader(pdf)
        doc_info = pdf_file.getDocumentInfo()
        print(f'[*] PDF MetaData For: {str(filename)}')
        for metaItem in doc_info:
            print(f'[+] {metaItem}: {doc_info[metaItem]}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        usage='python3 pdf_read.py PDF_FILE_NAME')
    parser.add_argument('pdf_file', type=str, metavar='PDF_FILE_NAME',
                        help='specify the name of the PDF file')

    args = parser.parse_args()
    print_meta(args.pdf_file)
