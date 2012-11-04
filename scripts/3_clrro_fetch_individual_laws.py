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
            
def parse_file(laws_file):
    print('Parsing for law details ' + laws_file)
    with open(laws_file) as file:
        laws_file_data = file.read()
    
    html_page = parse.fromstring(laws_file_data)
    
    law_table_rows = html_page.findall(
        "body/center/form/span/center/span/center/span[2]/center/table/tbody/tr")
    
    if len(law_table_rows) > 0:
      print "Working on ", laws_file, ", laws: ", len(law_table_rows)
    
    for table_row in law_table_rows:
      column_in_table = table_row.findall("td")
      
      if column_in_table:
        law_number_from_year = column_in_table[1].find('font/i/a').attrib
        law_natural_id = law_number_from_year.replace('.', '').replace('/', '_')
        active_function = column_in_table[3].find('font/i/a').attrib
        pasive_function = column_in_table[4].find('font/i/a').attrib
        print(law_natural_id)
        print(active_function)
        print(pasive_function)

def main():
    print("Fetching law details")
    temporary_clr_ro_dir = sys.argv[1]
    get_all_downloaded_laws_per_year(temporary_clr_ro_dir)

if __name__ == '__main__':main()
