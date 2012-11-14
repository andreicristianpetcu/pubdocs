#!/usr/bin/env python
from mechanize import Browser
import sys, os, time


def get_years_with_laws():
    # appearantly we do not have laws in all years since 1864.
    # I chose the years from http://www.clr.ro/rep_dil_2002/rep.aspx
    years = [1864, 1865, 1879, 1881, 1887, 1909, 1916, 1918, 1919, 1924, 1925,
             1927, 1929, 1930, 1931, 1933, 1934, 1937, 1938, 1940]
    years += range(1942, 2013)
    
    # dev only
    years = range(2010, 2013)
    return sorted(years,reverse=True)

def generate_laws(temporaryDirectory):
    years_with_laws = get_years_with_laws()
    print('Starting to download the laws in years ' + str(years_with_laws))
    for year in years_with_laws:
        fetch_laws_page_from_year(str(year), temporaryDirectory)
  
def fetch_laws_page_from_year(year, temporaryDirectory):  
    lawsDirectory = os.path.join(temporaryDirectory, 'all_laws');
    if not os.path.exists(lawsDirectory):
        os.makedirs(lawsDirectory)
        print('The laws directory did not exist so I created it')
        print(lawsDirectory)

    fileToWriteLawsListIn = os.path.join(lawsDirectory, year + '.html')
    print('File to write in is ' + fileToWriteLawsListIn)
    lawWasNotDownloaded = not os.path.isfile(fileToWriteLawsListIn)
    if lawWasNotDownloaded:
        startDownload = int(round(time.time() * 1000))
        
        print('Getting laws from year ' + year)
        url = get_ugly_url_for_laws(year)
        browser = Browser()
        browser.open(url)
        html = browser.response().get_data()

        with open(fileToWriteLawsListIn, 'a') as f: 
            f.write (html)

        endDownload = int(round(time.time() * 1000))
        print('Finished downloading laws for year ' + year + '. It took only ' 
              + str(endDownload - startDownload) + ' milliseconds')
    else:
        print('This year was already fetched ' + year 
              + '. Skipping to the next year')

  
def get_ugly_url_for_laws(year):
    url = 'http://www.clr.ro/rep_dil_2002/viewGrid.aspx?Type=Submit&pk1=SELECT%20*%20FROM%20legi%20Where%20legi.cod%20Like%20%27%nr.%/'
    url += year        
    url += '%%27%20AND%20NOT%20Isnull(legi.titlul)%20AND%20(legi.Cod_even%3C%3E%277%27%20AND%20legi.Cod_even%3C%3E%278%27%20AND%20legi.Cod_even%3C%3E%279%27%20AND%20(legi.Tip_world=%27%27%20OR%20IsNull(legi.Tip_world))%20AND%20(legi.Nr_world=0%20OR%20IsNull(legi.Nr_world))%20AND%20(legi.An_world=0%20OR%20IsNull(legi.An_world)))%20Order%20by%20Cod_tip%20ASC,%20Cod_an%20ASC,%20Cod_nr%20ASC,%20Cod_even%20ASC%20UNION%20ALL%20SELECT%20*%20FROM%20abrogate%20Where%20abrogate.cod%20Like%20%27%nr.%/'
    url += year        
    url += '%%27%20AND%20NOT%20Isnull(abrogate.titlul)%20AND%20(abrogate.Cod_even%3C%3E%277%27%20AND%20abrogate.Cod_even%3C%3E%278%27%20AND%20abrogate.Cod_even%3C%3E%279%27%20AND%20(abrogate.Tip_world=%27%27%20OR%20IsNull(abrogate.Tip_world))%20AND%20(abrogate.Nr_world=0%20OR%20IsNull(abrogate.Nr_world))%20AND%20(abrogate.An_world=0%20OR%20IsNull(abrogate.An_world)))%20Order%20by%20Cod_tip%20ASC,%20Cod_an%20ASC,%20Cod_nr%20ASC,%20Cod_even%20ASC&pk2=RadioPageTot&pk3=&pk4=TOT&pk5='
    url += year        
    url += '&pk7=1&pk8=Radio8&pk9=Radio5&pk10=Radio11&pk11=nrdoc_empty1'
    return url
    
def main():
    print(__file__)
    print(str(sys.argv))
#    temporaryDirectory = sys.argv[1]
#    generate_laws(temporaryDirectory)

if  __name__ == '__main__':main()
