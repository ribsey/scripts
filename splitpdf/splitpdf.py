#!/usr/bin/env python3

# Created by Ribi Lukas (ribsey) at 25.05.2021

# Description: This script extracts names from a pdf page and stores that page in a new pdf with the name as file name.

# Modification:
# Date       | Name             | Description
# 27.05.2021 | ribsey           | resolved errors for specific files (regex1)

import re
import warnings
from argparse import ArgumentParser
from os import path, remove

import pandas as pd
import pdfplumber
from PyPDF2 import PdfFileReader, PdfFileWriter


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def arguments():
    """
    Handles the CLI arguments

    :return arguments
    """
    parser = ArgumentParser(
        description='Extracts every page of the source pdf and writes it to a new pdf with the name found on the page.',
        epilog='If no abbreviation list is specified or no abbreviation could be found, the full names will be added '
               'to the destination file name.'
               'By default the destination file name is the source file name withe the name added')
    parser.add_argument('source', metavar='source', type=str,
                        help='path of source file')
    parser.add_argument('-a', metavar='abbreviation-list', type=str,
                        help='path of abbreviation list', required=False)
    parser.add_argument('-d', metavar='destination', type=str,
                        help='common destination file name or path', required=False)
    parser.add_argument('-i', action='store_true',
                        help='ignores pages without names, if not specified saves it with page number in fil name',
                        required=False)
    parser.add_argument('-o', action='store_true',
                        help='overwrite existing file',
                        required=False)
    return parser.parse_args()


def getNames(src):
    """
    Parses the PDF text and extracts the name(s) of each page.

    :param str src: Path to the source file
    :return list names: List of dictionaries with the name(s) and the corresponding page number
    """

    # regex for payroll capturing name and surname
    regex1 = re.compile(
        '(Herr|Frau).*\n([a-zA-Z??????????????]+) ([a-zA-Z??????????????]+) ?([a-zA-Z??????????????]*)(-)?(?(5)[a-zA-Z??????????????]+|) +Vers')
    # regex for donation statement capturing name and surname and if available the name of the partner
    regex2 = re.compile(
        '(?:Monatsabrechnung Spenden f??r )([a-zA-Z??????????????]+) ([a-zA-Z??????????????]+)( & )?(?(3)([a-zA-Z??????????????]+)|)')

    names = []
    with pdfplumber.open(src) as pdf:
        numPages = len(pdf.pages)
        for i in range(numPages):
            page = pdf.pages[i]
            pageContent = page.extract_text()
            reg = regex1.split(pageContent)
            if len(reg) == 7:
                if reg[4] == '':
                    # single name
                    names.append({
                        'type': 'payroll',
                        'pageNum': i,
                        'name': reg[2],
                        'name2': '',
                        'surname': reg[3],
                        'abbr': ''
                    })
                else:
                    # two names
                    names.append({
                        'type': 'payroll',
                        'pageNum': i,
                        'name': f'{reg[2]} {reg[3]}',
                        'name2': '',
                        'surname': reg[4],
                        'abbr': ''
                    })
            else:
                reg = regex2.split(pageContent)
                if len(reg) == 6:
                    if reg[4] is not None:
                        # couple
                        names.append({
                            'type': 'donation',
                            'pageNum': i,
                            'name': reg[2],
                            'name2': reg[4],
                            'surname': reg[1],
                            'abbr': ''
                        })
                    elif reg[2] != '':
                        # single person
                        names.append({
                            'type': 'donation',
                            'pageNum': i,
                            'name': reg[2],
                            'name2': '',
                            'surname': reg[1],
                            'abbr': ''
                        })
                else:
                    # no name found
                    names.append({
                        'type': 'not found',
                        'pageNum': i,
                        'name': '',
                        'name2': '',
                        'surname': '',
                        'abbr': ''
                    })
                    print(bcolors.WARNING + 'Could not find any name on page: ' + str(i + 1) + bcolors.ENDC)
    return names


def getAbbr(names, listPath):
    """
    Searches the abbreviation to the given name

    :param list names: List of dictionaries with the names
    :param list listPath: Path to the excel file containing the abbreviations
    :return list names: List of dictionaries with the name(s) with added abbreviation
    """
    data = pd.read_excel(listPath, skiprows=5)
    abbr = data['K??rzel'].tolist()
    name = data['Name'].tolist()

    abbrList = dict(zip(name, abbr))

    for name in names:
        if name['name2'] == '':
            s = f"{name['surname']} {name['name']}"
        else:
            s = f"{name['surname']} {name['name']} & {name['name2']}"

        try:
            name['abbr'] = abbrList[s]
        except Exception as e:
            if s != ' ':
                print(bcolors.WARNING + 'Could not find abbreviation for: ' + str(e) +
                      ' -> using full name as file name' + bcolors.ENDC)
        else:
            print('Found abbreviaton for: \'' + s + '\'')
    return names


def extractPages(src, dst, start, end=0):
    """
    Extracts the pages between start to end from the source file to the destination file

    :param str src: Path to the source file
    :param str dst: Path to the destination file
    :param int start: Start page number (first page number is '0'!)
    :param int end: end page number (0: one page only)
    """
    pdf = PdfFileReader(src)

    if end == 0:
        end = start + 1
    else:
        end += 1

    pdf_writer = PdfFileWriter()
    for page in range(start, end):
        pdf_writer.addPage(pdf.getPage(page))
    with open(dst, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)


if __name__ == '__main__':
    warnings.simplefilter("ignore")
    args = arguments()

    # process arguments
    print('')
    if args.source:
        srcPath = path.expanduser(args.source)
    else:
        srcPath = ''
    if args.a:
        abbrPath = path.expanduser(args.a)
    else:
        abbrPath = ''
    if args.d:
        dstPath = path.expanduser(args.d)
        # if argument is not a directory but a file name
        if path.dirname(dstPath) == '':
            dstPath = path.dirname(srcPath) + '/' + path.expanduser(args.d)
    else:
        dstPath = srcPath

    if dstPath[-4:] == '.pdf':
        dstPath = dstPath[:-4]

    # check if paths are legit
    if not path.isfile(srcPath):
        print(bcolors.FAIL + 'No such file: ' + srcPath + bcolors.ENDC)
        exit(1)
    else:
        print('Source file: ', srcPath)
    if not path.isdir(path.dirname(dstPath)):
        print(bcolors.FAIL + 'No such directory: ' + path.dirname(dstPath) + bcolors.ENDC)
        exit(1)
    else:
        print('Common destination file name: ', dstPath)
    if not path.isfile(abbrPath) and not abbrPath == '':
        print(bcolors.FAIL + 'No such file: ' + abbrPath + bcolors.ENDC)
        exit(1)
    else:
        print('Abbreviation list : ', args.a)
    print('')

    # extract names for each pdf page
    names = getNames(srcPath)
    i = 0
    for name in names:
        if name['name'] != '':
            i += 1
    print(f'Names found: {i}')

    # get abbreviations if list available
    if abbrPath:
        names = getAbbr(names, abbrPath)

    print('')

    # save pages
    i = 0
    for name in names:
        writeFile = True
        if name['abbr'] != '':
            dst = dstPath + '_' + name['abbr'] + '.pdf'
        else:
            if name['name'] == '':
                if args.i:
                    writeFile = False
                else:
                    dst = dstPath + '_' + str(name['pageNum']) + '.pdf'
            else:
                if name['name2'] == '':
                    dst = dstPath + '_' + name['surname'] + '_' + name['name'].replace(' ', '_') + '.pdf'
                else:
                    dst = dstPath + '_' + name['surname'] + '_' + name['name'].replace(' ', '_') + '_' + \
                          name['name2'].replace(' ', '_') + '.pdf'

        if writeFile:
            if path.isfile(dst):
                if args.o:
                    remove(dst)
                else:
                    writeFile = False
                    print(bcolors.WARNING + 'File \'' + dst + '\' already exists!' + bcolors.ENDC)

            if writeFile:
                print('writing file: ' + dst)
                extractPages(srcPath, dst, name['pageNum'])
                print('finished: ' + dst)
                i += 1

    print('')
    print(f'finished writing {i} files')
