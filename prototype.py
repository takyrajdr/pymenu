import requests
from bs4 import BeautifulSoup

def get_soup(url: str) -> BeautifulSoup:
    page = requests.get(url)
    return BeautifulSoup(page.content, "html.parser")


def print_klanovka():
    print("KLANOVKA")
    soup = get_soup("https://www.klanovkabistro.cz/poledni-menu/")
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

def print_babygolf():
    print("BABYGOLF")
    soup = get_soup("https://www.restauraceminigolf.cz/denni-menu")
    foods = soup.find_all(name="td", class_="today-menu-name")
    prices = soup.find_all(name="td", class_="today-menu-price")
    for food, price in zip(foods,prices):
        print(" ".join(food.text.split()), price.text)

if __name__ == "__main__":
    print_klanovka()
    print_babygolf()
