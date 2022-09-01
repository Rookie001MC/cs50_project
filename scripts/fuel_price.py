import pandas as pd
import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse


def price_get():

    page_data = get_page()
    if page_data is False:
        response_object = create_response_object(False)
    else:
        soup = BeautifulSoup(page_data, "html.parser")

        # Thank god I only need to deal with 1 table 🥲
        table = soup.find("table", class_="table")
        fuel_data = table_parsing(table)

        response_object = create_response_object(fuel_data)
    return response_object


def get_page():
    try:
        url = "https://www.pvoil.com.vn/truyen-thong/tin-gia-xang-dau"
        data = requests.get(url).text
    except BaseException as err:
        data = False
        print(f"Error in fetching data: {err}")
    return data


def table_parsing(table):
    list_of_heads = table.thead.find_all("strong")
    last_updated_head = list_of_heads[2].text.strip()
    last_updated_time = parse(last_updated_head, fuzzy=True)

    result = {"last_updated": last_updated_time.strftime("%d/%m/%Y, %H:%M")}
    product = []
    price = []
    offset = []
    for row in table.tbody.find_all("tr"):
        columns = row.find_all("td")

        if columns != []:
            product.append(columns[1].text.strip())
            price.append(columns[2].text.strip())
            offset.append(columns[3].text.strip())

    df = pd.DataFrame(
        {"product": product, "price": price, "offset_by_previous": offset}
    )

    data = df.to_dict("records")
    result["data"] = data
    return result


def translate_fuel_names(product):
    TRANSLATIONS = {
        "Xăng RON 95-III": "E5 RON 95-III",
        "Xăng E5 RON 92-II": "E5 RON 92-II",
        "Dầu DO 0,05S-II": "Diesel Oil DO 0.05S",
        "Dầu KO": "Kerosene",
    }

    if product in TRANSLATIONS:
        return TRANSLATIONS[product]


def create_response_object(data):
    if data is False:
        response = {"text": "Something has gone wrong!"}
    else:
        last_updated = data["last_updated"]
        fuel_data = data["data"]
        data_string = ""

        for product in fuel_data:
            data_string += f"{product['product']}: {product['price']} dong/liter - {product['offset_by_previous']} dong/liter difference compared to last adjustment.\n"

        response = {
            "text": f"""Showing current Vietnam fuel prices:
Last adjustment: {last_updated}

{data_string}
Source:
https://www.pvoil.com.vn/truyen-thong/tin-gia-xang-dau"""
        }
    return response


if __name__ == "__main__":
    price_get()
