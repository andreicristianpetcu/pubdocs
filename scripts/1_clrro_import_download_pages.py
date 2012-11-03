#!/usr/bin/env python
from mechanize import Browser
import sys, logging

def get_laws_search_page():  
  # Navigate to the main search page for laws.
  browser = Browser()
  
  navigate_to_laws_from_year(browser, '2006')
  navigate_to_laws_from_year(browser, '2007')
  navigate_to_laws_from_year(browser, '2008')
  
def navigate_to_laws_from_year(browser, year):  
#  url = "http://www.clr.ro/rep_dil_2002/viewGrid.aspx?Type=Submit&pk1=SELECT%20*%20FROM%20legi%20Where%20legi.cod%20Like%20%27L.nr.%/"
#  url += year
#  url += "%%27%20AND%20NOT%20Isnull%28legi.titlul%29%20AND%20%28legi.Cod_even%3C%3E%277%27%20AND%20legi.Cod_even%3C%3E%278%27%20AND%20legi.Cod_even%3C%3E%279%27%20AND%20%28legi.Tip_world=%27%27%20OR%20IsNull%28legi.Tip_world%29%29%20AND%20%28legi.Nr_world=0%20OR%20IsNull%28legi.Nr_world%29%29%20AND%20%28legi.An_world=0%20OR%20IsNull%28legi.An_world%29%29%29%20Order%20by%20Cod_tip%20ASC,%20Cod_an%20ASC,%20Cod_nr%20ASC,%20Cod_even%20ASC%20UNION%20ALL%20SELECT%20*%20FROM%20abrogate%20Where%20abrogate.cod%20Like%20%27L.nr.%/"
#  url += year
#  url += "%%27%20AND%20NOT%20Isnull%28abrogate.titlul%29%20AND%20%28abrogate.Cod_even%3C%3E%277%27%20AND%20abrogate.Cod_even%3C%3E%278%27%20AND%20abrogate.Cod_even%3C%3E%279%27%20AND%20%28abrogate.Tip_world=%27%27%20OR%20IsNull%28abrogate.Tip_world%29%29%20AND%20%28abrogate.Nr_world=0%20OR%20IsNull%28abrogate.Nr_world%29%29%20AND%20%28abrogate.An_world=0%20OR%20IsNull%28abrogate.An_world%29%29%29%20Order%20by%20Cod_tip%20ASC,%20Cod_an%20ASC,%20Cod_nr%20ASC,%20Cod_even%20ASC&pk2=RadioPageTot&pk3=&pk4=L&pk5="
#  url += year
#  url += "&pk7=1&pk8=Radio8&pk9=Radio5&pk10=Radio11&pk11=nrdoc_empty1"
  
  url = "http://www.clr.ro/rep_dil_2002/viewGrid.aspx?Type=Submit&pk1=SELECT%20*%20FROM%20legi%20Where%20legi.cod%20Like%20%27%nr.%/"
  url += year        
  url += "%%27%20AND%20NOT%20Isnull(legi.titlul)%20AND%20(legi.Cod_even%3C%3E%277%27%20AND%20legi.Cod_even%3C%3E%278%27%20AND%20legi.Cod_even%3C%3E%279%27%20AND%20(legi.Tip_world=%27%27%20OR%20IsNull(legi.Tip_world))%20AND%20(legi.Nr_world=0%20OR%20IsNull(legi.Nr_world))%20AND%20(legi.An_world=0%20OR%20IsNull(legi.An_world)))%20Order%20by%20Cod_tip%20ASC,%20Cod_an%20ASC,%20Cod_nr%20ASC,%20Cod_even%20ASC%20UNION%20ALL%20SELECT%20*%20FROM%20abrogate%20Where%20abrogate.cod%20Like%20%27%nr.%/"
  url += year        
  url += "%%27%20AND%20NOT%20Isnull(abrogate.titlul)%20AND%20(abrogate.Cod_even%3C%3E%277%27%20AND%20abrogate.Cod_even%3C%3E%278%27%20AND%20abrogate.Cod_even%3C%3E%279%27%20AND%20(abrogate.Tip_world=%27%27%20OR%20IsNull(abrogate.Tip_world))%20AND%20(abrogate.Nr_world=0%20OR%20IsNull(abrogate.Nr_world))%20AND%20(abrogate.An_world=0%20OR%20IsNull(abrogate.An_world)))%20Order%20by%20Cod_tip%20ASC,%20Cod_an%20ASC,%20Cod_nr%20ASC,%20Cod_even%20ASC&pk2=RadioPageTot&pk3=&pk4=TOT&pk5="
  url += year        
  url += "&pk7=1&pk8=Radio8&pk9=Radio5&pk10=Radio11&pk11=nrdoc_empty1"
  
  browser.open(url)
  html = browser.response().get_data()

  with open ('clr.ro.'+ year + '.html', 'a') as f: 
      f.write (html)
  
  print(html)
    
#  browser.select_form(name='Form1')
#  form = browser.form
#
#  form['Anul'] = [year]
#  html = browser.submit().read()
  
#  print(html)

def main():
#    logger = logging.getLogger("mechanize")
#    logger.addHandler(logging.StreamHandler(sys.stdout))
#    logger.setLevel(logging.DEBUG)

    get_laws_search_page()


if  __name__ =='__main__':main()