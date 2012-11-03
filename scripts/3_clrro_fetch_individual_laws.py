#!/usr/bin/env python
from mechanize import Browser
import sys, os, time
from xml.etree import ElementTree as parse



def get_all_downloaded_laws_per_year(temporary_clr_ro_dir):
    laws_files = [ os.path.join(temporary_clr_ro_dir, file) 
                 for file in os.listdir(temporary_clr_ro_dir)]
    for laws_file in sorted(laws_files, reverse=True):
        if os.path.isfile(laws_file) and laws_file.endswith('.html'): 
            parse_file(laws_file)

def debug_parse_with_sax(file_to_parse):
    ignored_tags = ['tr', 'td', 'a', 'sup']
    for event, elem in parse.iterparse(file_to_parse, events=("start", "end")):
        if not elem.tag in ignored_tags:
            if event == "start":
                print("+" + elem.tag)
            else:
                print("-" + elem.tag)

def parse_rows_with_sax(file_to_parse):
    rows = []
    row = [None]*5
    column = -1
    parsing_table = False
    for event, elem in parse.iterparse(file_to_parse, events=("start", "end")):
        if event == 'start':
            if elem.tag == 'table':
                parsing_table = True
            elif parsing_table:
                if elem.tag == 'tr':
                    row = ['']*5
                    rows.append(row)
                    column = -1
                elif elem.tag == 'td':
                    column += 1
                    row[column] = str(elem.text)
                elif elem.tag == 'a':
                    row[column] = elem.get('href')
                else:
                     row[column] += str(elem.text)
                        
        elif event == 'end':
            if elem.tag == 'table':
                parsing_table = False
                break
                
    return rows
 
def parse_file(laws_file):
    print('Parsing for law details ' + laws_file)
    parsed_rows = parse_rows_with_sax(laws_file)
    print(str(len(parsed_rows)) + ' Laws found in file ' + laws_file)

def main():
    print(__file__)
    print(str(sys.argv))
    temporary_clr_ro_dir = sys.argv[1]
    get_all_downloaded_laws_per_year(temporary_clr_ro_dir)

if __name__ == '__main__':main()
