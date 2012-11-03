#!/usr/bin/env python
from mechanize import Browser
import sys, logging

def get_years_with_laws():
    # appearantly we do not have laws in all years since 1864.
    # I chose the years from http://www.clr.ro/rep_dil_2002/rep.aspx
    years = [1864, 1865, 1879, 1881, 1887, 1909, 1916, 1918, 1919, 1924, 1925,
             1927, 1929, 1930, 1931, 1933, 1934, 1937, 1938, 1940]
    years += range(1942, 2012)
    return sorted(years)

def generate_laws():  
  navigate_to_laws_from_year('2006')
#  navigate_to_laws_from_year('2007')
#  navigate_to_laws_from_year('2008')
  
def navigate_to_laws_from_year(year):  
  url = get_url_forlaws(year)
  browser = Browser()
  browser.open(url)
  html = browser.response().get_data()

  with open ('clr.ro-laws-' + year + '.html', 'a') as f: 
      f.write (html)
  
  print(html)
  
def get_url_forlaws(year):
  url = "http://www.clr.ro/rep_dil_2002/viewGrid.aspx?Type=Submit&pk1=SELECT%20*%20FROM%20legi%20Where%20legi.cod%20Like%20%27%nr.%/"
  url += year        
  url += "%%27%20AND%20NOT%20Isnull(legi.titlul)%20AND%20(legi.Cod_even%3C%3E%277%27%20AND%20legi.Cod_even%3C%3E%278%27%20AND%20legi.Cod_even%3C%3E%279%27%20AND%20(legi.Tip_world=%27%27%20OR%20IsNull(legi.Tip_world))%20AND%20(legi.Nr_world=0%20OR%20IsNull(legi.Nr_world))%20AND%20(legi.An_world=0%20OR%20IsNull(legi.An_world)))%20Order%20by%20Cod_tip%20ASC,%20Cod_an%20ASC,%20Cod_nr%20ASC,%20Cod_even%20ASC%20UNION%20ALL%20SELECT%20*%20FROM%20abrogate%20Where%20abrogate.cod%20Like%20%27%nr.%/"
  url += year        
  url += "%%27%20AND%20NOT%20Isnull(abrogate.titlul)%20AND%20(abrogate.Cod_even%3C%3E%277%27%20AND%20abrogate.Cod_even%3C%3E%278%27%20AND%20abrogate.Cod_even%3C%3E%279%27%20AND%20(abrogate.Tip_world=%27%27%20OR%20IsNull(abrogate.Tip_world))%20AND%20(abrogate.Nr_world=0%20OR%20IsNull(abrogate.Nr_world))%20AND%20(abrogate.An_world=0%20OR%20IsNull(abrogate.An_world)))%20Order%20by%20Cod_tip%20ASC,%20Cod_an%20ASC,%20Cod_nr%20ASC,%20Cod_even%20ASC&pk2=RadioPageTot&pk3=&pk4=TOT&pk5="
  url += year        
  url += "&pk7=1&pk8=Radio8&pk9=Radio5&pk10=Radio11&pk11=nrdoc_empty1"
  return url
    
def main():
#    generate_laws()
    print(get_years_with_laws())


if  __name__ == '__main__':main()
