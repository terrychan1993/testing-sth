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

VARIANTS = {
    "1": "https://javstarmeet.com/collections/%E6%94%9D%E5%BD%B1%E6%9C%83/products/%E2%8F%B1%EF%B8%8F-%F0%9F%93%B8-%E6%A3%AE%E6%97%A5%E5%90%91%E5%AD%90-%E9%A6%99%E6%B8%AF%E7%B2%89%E7%B5%B2%E6%94%9D%E5%BD%B1%E6%9C%83-2026%E5%B9%B43%E6%9C%8824%E6%97%A5-%E5%80%8B%E4%BA%BA%E5%8A%A0%E8%B3%BC%E6%8B%8D%E6%94%9D%E5%88%B8?variant=52007361511705",
    "2": "https://javstarmeet.com/collections/%E6%94%9D%E5%BD%B1%E6%9C%83/products/%E2%8F%B1%EF%B8%8F-%F0%9F%93%B8-%E6%A3%AE%E6%97%A5%E5%90%91%E5%AD%90-%E9%A6%99%E6%B8%AF%E7%B2%89%E7%B5%B2%E6%94%9D%E5%BD%B1%E6%9C%83-2026%E5%B9%B43%E6%9C%8824%E6%97%A5-%E5%80%8B%E4%BA%BA%E5%8A%A0%E8%B3%BC%E6%8B%8D%E6%94%9D%E5%88%B8?variant=52007361544473",
    "3": "https://javstarmeet.com/collections/%E6%94%9D%E5%BD%B1%E6%9C%83/products/%E2%8F%B1%EF%B8%8F-%F0%9F%93%B8-%E6%A3%AE%E6%97%A5%E5%90%91%E5%AD%90-%E9%A6%99%E6%B8%AF%E7%B2%89%E7%B5%B2%E6%94%9D%E5%BD%B1%E6%9C%83-2026%E5%B9%B43%E6%9C%8824%E6%97%A5-%E5%80%8B%E4%BA%BA%E5%8A%A0%E8%B3%BC%E6%8B%8D%E6%94%9D%E5%88%B8?variant=52007361577241",
}

def get_remaining_qty(url):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=12)
        resp.raise_for_status()
    except Exception as e:
        print(f"Request failed for {url}: {e}", file=sys.stderr)
        return None

    soup = BeautifulSoup(resp.text, "html.parser")

    # Best: data-current-qty
    input_el = soup.find("input", {"data-current-qty": re.compile(r"\d+")})
    if input_el and "data-current-qty" in input_el.attrs:
        try:
            return int(input_el["data-current-qty"])
        except:
            pass

    # Fallback: max on quantity input
    qty_input = soup.find("input", {"name": "quantity", "type": "number"})
    if qty_input and "max" in qty_input.attrs:
        try:
            return int(qty_input["max"])
        except:
            pass

    # Last resort: any nearby number in stock text
    stock_text = soup.find(string=re.compile(r"(剩餘|剩余|remaining|left|only|有存貨)\s*[\dX]+", re.I))
    if stock_text:
        m = re.search(r"\d+", stock_text)
        if m:
            return int(m.group())

    print(f"No quantity found for {url}", file=sys.stderr)
    return None


if __name__ == "__main__":
    for slot_name, url in VARIANTS.items():
        qty = get_remaining_qty(url)
        if qty is not None:
            print(f"{slot_name} remaining：{qty}")

        else:
            print(f"{slot_name} 查詢失敗或已售罄/無數量顯示")

        print("-" * 40)
