#!/usr/bin/env python
from mechanize import Browser

def get_laws_search_page():  
  # Navigate to the main search page for laws.
  browser = Browser()
  browser.open('http://www.clr.ro/rep_dil_2002/rep.aspx')
  
  html = browser.response().get_data().replace("<br/>", "<br />")
  
  print("html=" + html)
  
#  br.select_form(name='Voturi')
#  form = br.form
#
#  form['drpMonthCal'] = [month]

def main():
    get_laws_search_page()


if  __name__ =='__main__':main()