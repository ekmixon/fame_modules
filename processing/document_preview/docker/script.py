import argparse
import os
from pdf2image import convert_from_path
import re


def pdftoimages(target, max_pages):
    pages = convert_from_path(target, last_page=int(max_pages))
    # delete extension in case we had to create pdf file from an office file
    target = os.path.splitext(target)[0]

    counter = 0

    # create folder if not exists
    if not os.path.isdir('output'):
        os.mkdir('output')

    # save pages to jpeg format
    for page in pages:
        counter = counter + 1
        page.save(f"./output/{re.sub('[^A-Za-z0-9]+', '_', target)}_{counter}.jpeg")

    if counter == 0:
        print('error: could not convert PDF to images')


def libreofficeconversion(args):
    # convert to pdf using libreoffice
    convert_pdf = f'libreoffice --headless --convert-to pdf "{os.path.basename(args.target)}" 2> /dev/null'

    os.system(convert_pdf)

    if os.path.exists(f'{os.path.splitext(args.target)[0]}.pdf'):
        return True
    print('error: libreoffice could not convert file to PDF')
    return False


def main(args):

    # if office file, convert to pdf file with libreoffice library
    if args.target_type in ['word', 'excel', 'powerpoint']:
        if libreofficeconversion(args):
            pdftoimages(f'{os.path.splitext(args.target)[0]}.pdf', args.max_pages)
    elif args.target_type == 'pdf':
        pdftoimages(args.target, args.max_pages)
    else:
        print('warning: Unsupported target file')
        print('warning: libreoffice will try to convert the file to PDF')
        # convert to pdf file through libreoffice process
        if libreofficeconversion(args):
            pdftoimages(f'{os.path.splitext(args.target)[0]}.pdf', args.max_pages)


# ------------ Viewing document Script  ------------ #
# goal : Allow viewing of documents                  #
# works on : pdf, word, excel, powerpoint            #
# output : jpeg images (output folder)               #
# arguments :                                        #
#    * --target : input file                         #
#    * --target_type : input file type               #
#    * --max_pages : last page to view               #
# command : python scrits.py args                    #
# -------------------------------------------------- #

if __name__ == '__main__':
    # argument configuration
    parser = argparse.ArgumentParser()
    parser.add_argument('--target')
    parser.add_argument('--target_type')
    parser.add_argument('--max_pages')
    args = parser.parse_args()

    main(args)
