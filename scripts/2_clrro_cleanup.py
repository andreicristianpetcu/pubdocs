#!/usr/bin/env python
from mechanize import Browser
import sys, os, time
from xml.etree import ElementTree as parse
from stgit.argparse import dirty_files


def clean_all_downloaded_files(downloaded_files_dir):
    if not os.path.exists(downloaded_files_dir):
        os.makedirs(downloaded_files_dir)
 
    dirty_files = [ os.path.join(downloaded_files_dir, file_name) 
                 for file_name in os.listdir(downloaded_files_dir)]
    for dirty_file in sorted(dirty_files, reverse=True):
        if os.path.isfile(dirty_file) and dirty_file.endswith('.html'): 
            clean_file_content = clean_file(dirty_file)
            clean_file_path = os.path.join(downloaded_files_dir, 
                                           'clean_files', dirty_file)
            with open(dirty_file + '.clean.html' , 'w+') as file:
                file.write (clean_file_content)
            
            
def clean_file(dirty_file):
    print("Cleaning file " + dirty_file)
    with open(dirty_file) as file:
        dirty_file_content = file.read()
        
    dirty_file_content = dirty_file_content.replace('windows-1250', 'utf-8')
    decoded_content = dirty_file_content.decode('windows-1250')
    utf8_conent = decoded_content.encode('UTF-8')
    return utf8_conent 

def main():
    downloaded_files_dir = sys.argv[1] if len(sys.argv)>1 else '/tmp/legilibere/clr_ro/all_laws'
    clean_all_downloaded_files(downloaded_files_dir)

if __name__ == '__main__':main()
