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
    with open(dirty_file) as file:
        dirty_file_content = file.read()
        
    dirty_file_content = dirty_file_content.replace('windows-1250', 'utf-8')
    decoded_content = dirty_file_content.decode('windows-1250')
    utf8_conent = decoded_content.encode('UTF-8')
    removed_unbalanced_tags = remove_unbalanced_tags(utf8_conent)
    return removed_unbalanced_tags 

def remove_unbalanced_tags(content):
    content = content.replace('</HEAD>', '').replace('<HEAD>', '')
    content = content.replace('</head>', '').replace('<head>', '')
    return content

def main():
    print("Cleaning files")
    downloaded_files_dir = sys.argv[1]
    clean_files_dir = sys.argv[2]
    clean_all_downloaded_files(downloaded_files_dir, clean_files_dir)

if __name__ == '__main__':main()
