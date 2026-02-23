import requests
from bs4 import BeautifulSoup
import re
import datetime
import sys

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.8",
}

PRODUCTS = {
    "森日向子 香港粉絲攝影會【2026年3月21日】": {
        "第一場 (12:00–13:00)": "https://javstarmeet.com/collections/%E6%94%9D%E5%BD%B1%E6%9C%83/products/%F0%9F%93%B8-%E7%AF%A0%E5%8E%9F%E4%BC%8A%E4%BB%A3-%E9%A6%99%E6%B8%AF%E7%B2%89%E7%B5%B2%E6%94%9D%E5%BD%B1%E6%9C%83-2026%E5%B9%B43%E6%9C%8824%E6%97%A5?variant=52007360528665",  # adjust variant if needed for specific slot
        "第二場 (13:50–14:50)": "https://javstarmeet.com/collections/%E6%94%9D%E5%BD%B1%E6%9C%83/products/%F0%9F%93%B8-%E7%AF%A0%E5%8E%9F%E4%BC%8A%E4%BB%A3-%E9%A6%99%E6%B8%AF%E7%B2%89%E7%B5%B2%E6%94%9D%E5%BD%B1%E6%9C%83-2026%E5%B9%B43%E6%9C%8824%E6%97%A5?variant=52007360561433",
        "第三場 (15:40–16:40)": "https://javstarmeet.com/collections/%E6%94%9D%E5%BD%B1%E6%9C%83/products/%F0%9F%93%B8-%E7%AF%A0%E5%8E%9F%E4%BC%8A%E4%BB%A3-%E9%A6%99%E6%B8%AF%E7%B2%89%E7%B5%B2%E6%94%9D%E5%BD%B1%E6%9C%83-2026%E5%B9%B43%E6%9C%8824%E6%97%A5?variant=52007360594201",
    },
    "森日向子 香港粉絲攝影會【2026年3月21日】-「個人加購拍攝券」": {  # your previous event
        "第一場 (12:00–13:00)": "https://javstarmeet.com/collections/%E6%94%9D%E5%BD%B1%E6%9C%83/products/%E2%8F%B1%EF%B8%8F-%F0%9F%93%B8-%E6%A3%AE%E6%97%A5%E5%90%91%E5%AD%90-%E9%A6%99%E6%B8%AF%E7%B2%89%E7%B5%B2%E6%94%9D%E5%BD%B1%E6%9C%83-2026%E5%B9%B43%E6%9C%8824%E6%97%A5-%E5%80%8B%E4%BA%BA%E5%8A%A0%E8%B3%BC%E6%8B%8D%E6%94%9D%E5%88%B8?variant=52007361511705",
        "第二場 (13:50–14:50)": "https://javstarmeet.com/collections/%E6%94%9D%E5%BD%B1%E6%9C%83/products/%E2%8F%B1%EF%B8%8F-%F0%9F%93%B8-%E6%A3%AE%E6%97%A5%E5%90%91%E5%AD%90-%E9%A6%99%E6%B8%AF%E7%B2%89%E7%B5%B2%E6%94%9D%E5%BD%B1%E6%9C%83-2026%E5%B9%B43%E6%9C%8824%E6%97%A5-%E5%80%8B%E4%BA%BA%E5%8A%A0%E8%B3%BC%E6%8B%8D%E6%94%9D%E5%88%B8?variant=52007361544473",
        "第三場 (15:40–16:40)": "https://javstarmeet.com/collections/%E6%94%9D%E5%BD%B1%E6%9C%83/products/%E2%8F%B1%EF%B8%8F-%F0%9F%93%B8-%E6%A3%AE%E6%97%A5%E5%90%91%E5%AD%90-%E9%A6%99%E6%B8%AF%E7%B2%89%E7%B5%B2%E6%94%9D%E5%BD%B1%E6%9C%83-2026%E5%B9%B43%E6%9C%8824%E6%97%A5-%E5%80%8B%E4%BA%BA%E5%8A%A0%E8%B3%BC%E6%8B%8D%E6%94%9D%E5%88%B8?variant=52007361577241",
    },
}

def get_remaining_qty(url):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=12)
        resp.raise_for_status()
    except Exception as e:
        print(f"Request failed for {url}: {e}", file=sys.stderr)
        return None

    soup = BeautifulSoup(resp.text, "html.parser")

    input_el = soup.find("input", {"data-current-qty": re.compile(r"\d+")})
    if input_el and "data-current-qty" in input_el.attrs:
        try:
            return int(input_el["data-current-qty"])
        except:
            pass

    qty_input = soup.find("input", {"name": "quantity", "type": "number"})
    if qty_input and "max" in qty_input.attrs:
        try:
            return int(qty_input["max"])
        except:
            pass

    print(f"No quantity found for {url}", file=sys.stderr)
    return None


if __name__ == "__main__":
    for product_name, slots in PRODUCTS.items():
        #print(f"產品：{product_name}")
        for slot_name, url in slots.items():
            qty = get_remaining_qty(url)
            if qty is not None:
                print(f"{slot_name} 剩餘數量：{qty}")
            else:
                print(f"{slot_name} 查詢失敗或無數量顯示 / 有存貨但無數字")
