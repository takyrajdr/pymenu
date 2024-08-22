import requests
import typer
from bs4 import BeautifulSoup
from urllib3 import Retry
from requests.adapters import HTTPAdapter

# App for Web Scraping of the launch menus in Novodovrska, P4
app = typer.Typer(help="Utility for WebScraping of the menus.")

def get_verification_certificate(out_file:str="tmp.pem",cert_url:str="") -> str:
    """Downloads a specific validation certificate to the specified file. Will return the name of the file.

    Args:
        out_file (str, optional): Name & path to the file where certificate will be stored in. Defaults to "tmp.pem".
        cert_url (str, optional): URL from which certificate is downloaded from. Defaults to "".

    Returns:
        str: Returns the name of the file.
    """    
    cert_req = requests.get(cert_url)
    with open(out_file,"w") as file:
        file.write(cert_req.text)
    return out_file

def get_soup(url: str,cert_url:str) -> BeautifulSoup:
    req = requests.Session()
    # Only use specific certificate from URL when Certificate URL is non-empty
    if cert_url != "":
        swatch_cert = get_verification_certificate(cert_url=cert_url)
        req.verify = swatch_cert
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.9,cs;q=0.8',
        'Connection': 'keep-alive',
        'Host': 'www.klanovkabistro.cz',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        # 'Accept-Encoding': 'gzip, deflate, br, zstd',
        # 'Accept-Language': 'en-US,en;q=0.9',
        # 'Cache-Control': 'no-cache',
        # 'Connection': 'keep-alive',
        # 'Pragma': 'no-cache',
        # 'Sec-Fetch-Dest': 'document',
        # 'Sec-Fetch-Mode': 'navigate',
        # 'Sec-Fetch-Site': 'none',
        # 'Sec-Fetch-User': '?1',
        # 'Upgrade-Insecure-Requests': '1',
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        # 'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        # 'sec-ch-ua-mobile': '?0',
        # 'sec-ch-ua-platform': '"Windows"',
    } # Headers, so that the get is similiar to wjhat would browser do
    page = req.get(url=url,headers=headers)
    # When response is not OK. Print the response object (will print the code).
    if page.status_code != 200:
        print(page)
    return BeautifulSoup(page.content, "html.parser")

def print_klanovka(cert_url):
    print("KLANOVKA")
    soup = get_soup("https://www.klanovkabistro.cz/poledni-menu/",cert_url)
    weekly = soup.find_all(name="div", class_="et_pb_text_inner")
    # print(weekly)
    for daily in weekly:
        # print(daily.prettify())
        days = daily.find("h5")
        day_menu = daily.find_all("h6")
        day_menu = daily.find_all("p")
        if days is not None:
            print(days.text)
            for itm in day_menu:
                # print(itm)
                food_str = str(itm)
                food = food_str.split("<br/>")[0].split(">")[1]
                price = itm.find(name="em")
                if price is not None:
                    print_price = price.text
                    print(food, ":", print_price)

def print_babygolf(cert_url):
    print("BABYGOLF")
    soup = get_soup("https://www.restauraceminigolf.cz/denni-menu",cert_url)
    foods = soup.find_all(name="td", class_="today-menu-name")
    prices = soup.find_all(name="td", class_="today-menu-price")
    for food, price in zip(foods,prices):
        print(" ".join(food.text.split()), price.text)

@app.command()
def print_menus(cert_url:str = typer.Option("", help="URL to the cerficite for verification.")) -> None:
    """CLI Typer Command to call this script. Can be called directly.

    Args:
        cert_url (str, optional): URL to the certificate used for certicate validation. Defaults to typer.Option("", help="URL to the cerficite for verification.").
    """    
    print_klanovka(cert_url)
    print_babygolf(cert_url)

if __name__ == "__main__":
    app(prog_name=__file__)

