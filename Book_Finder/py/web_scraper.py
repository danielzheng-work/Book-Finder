import bs4 as bs
import mechanize
import sys
import ssl

# need to install a few libraries using pip3:
# bs4, lxml, mechanize

# this method scrapes the amazon webpage and returns the title based on the ASIN
def web_scraper(asin):
    # add an ssl bypass so that service is not denied 
    ssl._create_default_https_context = ssl._create_unverified_context
    url = 'https://www.amazon.com/gp/product/' + asin
    # create the browser 
    # using mechanize because requests and urllib get denied service after a few attempts 
    page = mechanize.Browser()
    page.set_handle_robots(False)
    # so we don't get a robot check
    headers = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    page.addheaders = [('User-agent', headers)]
    # open the url 
    page.open(url)
    # add the page html data to the soup structure so we can read it 
    soup = bs.BeautifulSoup(page.response().read(), features = "lxml")
    # filter the title data and then strip extra characters
    title = soup.title.string.rsplit(':')[0]
    return(title)


# test web_scraper('0001050230')
# method used to display the output in the gui 
if __name__ == '__main__':
    bookName = sys.argv[1]
    print("ASIN converted to: " + web_scraper(bookName))
