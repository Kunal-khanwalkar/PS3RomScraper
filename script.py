from helper import fetchSite
from helper import FTP
from lxml import html

NOPAYSTATION = 'https://nopaystation.com'

def download(game):    
    result = fetchSite(NOPAYSTATION + game)
    tree = html.fromstring(result.content)
    title = tree.xpath('/html/body/div[1]/div/div[2]/h4')[0].text_content()

    divs = tree.xpath('/html/body/div[1]/div/div[2]/div[@class="form-row"]')    

    print('\n' + title)
    for row in divs[2:5]:
        for col in row:
            print(col.xpath('./label')[0].text_content() + ' : ' + col.xpath('./input')[0].attrib.get('value'), end=', ')
        print('\n',end='')
    print('\n')        

    input("Press Enter to download this ROM...\n")

    rap_url = NOPAYSTATION + divs[5].xpath('./div[2]/a')[0].attrib.get('href')
    rap_name = divs[5].xpath('./div[2]/a')[0].attrib.get('download')
    FTP(rap_url, rap_name, title)
    
    pkg = divs[0].xpath('./div/input')[0].attrib.get('value')
    FTP(pkg, title+'.pkg', title)


def nopaystation(Search_Query):
    URL = NOPAYSTATION + '/search?query=' + Search_Query + '&platform=ps3&limit=10&orderBy=completionDate&sort=DESC&missing=Show'
    result = fetchSite(URL)    
    tree = html.fromstring(result.content)
    table_of_contents = tree.xpath('/html/body/div[1]/div/div[2]/div[1]/table/tbody')[0]

    if len(table_of_contents) == 0:
        raise SystemExit('No Entries found')
        
    for idx,title in enumerate(table_of_contents): 
        print('\n-\n' + str(idx+1) + '). ' + title.xpath('./td/a')[0].text_content())
        info = title.xpath('./td/span')
        for ele in info:
            print(ele.text_content() + ', ',end='')
    print('\n')
    
    option = input('Enter option: ')
    download(table_of_contents.xpath('./tr['+ option +']/td/a')[0].attrib.get('href'))


def main():
    Search_Query = input('Enter the name of the game: ')
    Search_Query = Search_Query.replace(' ','+')
    nopaystation(Search_Query)

if __name__=='__main__' :
    main()
