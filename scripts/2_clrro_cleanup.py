#!/usr/bin/env python
from mechanize import Browser
import sys, os, time
from xml.etree import ElementTree as parse
from stgit.argparse import dirty_files


def clean_all_downloaded_files(downloaded_files_dir, clean_files_dir):
    if not os.path.exists(clean_files_dir): os.makedirs(clean_files_dir)
 
    dirty_files = [ file_name for file_name in os.listdir(downloaded_files_dir)]
    
    for dirty_file in sorted(dirty_files, reverse=True):
        dirty_file_path = os.path.join(downloaded_files_dir, dirty_file)
        clean_file_path = os.path.join(clean_files_dir, dirty_file)
        if os.path.isfile(dirty_file_path) and dirty_file.endswith('.html'): 
            print('Cleaning file ' + dirty_file_path + 
                  ' result is in ' + clean_file_path)
            clean_file_content = clean_file(dirty_file_path)
            clean_file_path = os.path.join(clean_files_dir, dirty_file)
            with open(clean_file_path, 'w+') as file:
                file.write (clean_file_content)
            
def clean_file(dirty_file):
    """This method removes various useless parts of the file."""
    with open(dirty_file) as file:
        dirty_file_content = file.read()
        
    tmp_file_content = ''
    for line in dirty_file_content.split('\n'):
        # Skip the realy realy big input. This input has a huge value.
        if not line.startswith('<input type="hidden" name="__VIEWSTATE"'):
            tmp_file_content += line      
    # Use propper UTF-8 encoding
    tmp_file_content = tmp_file_content.replace('windows-1250', 'utf-8')
    decoded_content = tmp_file_content.decode('windows-1250')
    utf8_conent = decoded_content.encode('UTF-8')
    removed_unbalanced_tags = clean_xml_document_for_parser(utf8_conent)
    return removed_unbalanced_tags 

def clean_xml_document_for_parser(content):
    """This method cleans the document so it will not break the DOM parser."""
    # Remove unbalanced tags
    # Some tags appear only opened or closed
    content = content.replace('</HEAD>', '').replace('<HEAD>', '')
    content = content.replace('</head>', '').replace('<head>', '')
    content = content.replace('<BR>', '').replace('<HR>', '')
    content = content.replace('<CENTER>', '').replace('</CENTER>', '')
    content = content.replace('&nbsp;', '')
    content = content.replace('<br>', '')
    # Remove fonts and non-standard tags
    content = content.replace('<HR WIDTH = 65% Align=Center SIZE=1>', '')
    content = content.replace('<font color=navy>', '')
    content = content.replace('<font color=Green>', '')
    content = content.replace('<font color=RoyalBlue>', '')
    content = content.replace('<font color=Red>', '')
    content = content.replace('</font color>', '')
    content = content.replace('<Font>', '').replace('</Font>', '')
    content = content.replace('<font>', '').replace('</font>', '')
    content = content.replace('<font face="Arial" color="Black" size="2">', '')
    content = content.replace('<font face="Arial" color="SteelBlue" size="3">', '')
    content = content.replace('<font face="Arial" color="Navy" size="2">', '')
    content = content.replace('<font face="Arial" color="Black" size="1">', '')
    # Remove useless bold, italic and underline tags
    content = content.replace('<b>', '').replace('</b>', '')
    content = content.replace('<i>', '').replace('</i>', '')
    content = content.replace('<u>', '').replace('</u>', '')
    content = content.replace('<U>', '').replace('</U>', '')
    
    return content

def main():
    print(__file__)
    print(str(sys.argv))
    downloaded_files_dir = sys.argv[1]
    clean_files_dir = sys.argv[2]
    clean_all_downloaded_files(downloaded_files_dir, clean_files_dir)

if __name__ == '__main__':main()
