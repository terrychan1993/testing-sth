import requests
from bs4 import BeautifulSoup
import re
import time

URL = "https://javstarmeet.com/collections/%E6%94%9D%E5%BD%B1%E6%9C%83/products/%E2%8F%B1%EF%B8%8F-%F0%9F%93%B8-%E6%A3%AE%E6%97%A5%E5%90%91%E5%AD%90-%E9%A6%99%E6%B8%AF%E7%B2%89%E7%B5%B2%E6%94%9D%E5%BD%B1%E6%9C%83-2026%E5%B9%B43%E6%9C%8824%E6%97%A5-%E5%80%8B%E4%BA%BA%E5%8A%A0%E8%B3%BC%E6%8B%8D%E6%94%9D%E5%88%B8?variant=52007361577241"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.8",
}

def get_remaining_qty():
    try:
        resp = requests.get(URL, headers=HEADERS, timeout=12)
        resp.raise_for_status()
    except Exception as e:
        print(f"Request failed: {e}")
        return None

    soup = BeautifulSoup(resp.text, "html.parser")

    # Method 1 — most accurate in your case — data-current-qty
    input_el = soup.find("input", {"data-current-qty": re.compile(r"\d+")})
    if input_el and "data-current-qty" in input_el.attrs:
        return int(input_el["data-current-qty"])

    # Method 2 — fallback: the max attribute on quantity input
    qty_input = soup.find("input", {"name": "quantity", "type": "number"})
    if qty_input and "max" in qty_input.attrs:
        try:
            return int(qty_input["max"])
        except (ValueError, TypeError):
            pass

    # Method 3 — some themes also have it in a nearby element (less common)
    stock_text = soup.find(string=re.compile(r"(剩餘|剩余|remaining|left|only)\s*\d+", re.I))
    if stock_text:
        m = re.search(r"\d+", stock_text)
        if m:
            return int(m.group())

    print("Cannot find quantity info in HTML.")
    return None


# ────────────────────────────────────────
# Usage examples
# ────────────────────────────────────────
    qty = get_remaining_qty()
    if qty is not None:
        print(f"第三場 (15:40–16:40) 剩餘數量：{qty}")
        if qty <= 3:
            print("!!! 數量很少了 !!!")
    else:
        print("查詢失敗")
