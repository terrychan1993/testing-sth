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
        "森日向子攝影會第一場 (12:00–13:00)": "https://javstarmeet.com/collections/%E6%94%9D%E5%BD%B1%E6%9C%83/products/%F0%9F%93%B8-%E7%AF%A0%E5%8E%9F%E4%BC%8A%E4%BB%A3-%E9%A6%99%E6%B8%AF%E7%B2%89%E7%B5%B2%E6%94%9D%E5%BD%B1%E6%9C%83-2026%E5%B9%B43%E6%9C%8824%E6%97%A5?variant=52007360528665",  # adjust variant if needed for specific slot
        "森日向子攝影會第二場 (13:50–14:50)": "https://javstarmeet.com/collections/%E6%94%9D%E5%BD%B1%E6%9C%83/products/%F0%9F%93%B8-%E7%AF%A0%E5%8E%9F%E4%BC%8A%E4%BB%A3-%E9%A6%99%E6%B8%AF%E7%B2%89%E7%B5%B2%E6%94%9D%E5%BD%B1%E6%9C%83-2026%E5%B9%B43%E6%9C%8824%E6%97%A5?variant=52007360561433",
        "森日向子攝影會第三場 (15:40–16:40)": "https://javstarmeet.com/collections/%E6%94%9D%E5%BD%B1%E6%9C%83/products/%F0%9F%93%B8-%E7%AF%A0%E5%8E%9F%E4%BC%8A%E4%BB%A3-%E9%A6%99%E6%B8%AF%E7%B2%89%E7%B5%B2%E6%94%9D%E5%BD%B1%E6%9C%83-2026%E5%B9%B43%E6%9C%8824%E6%97%A5?variant=52007360594201",
    },
    "森日向子 香港粉絲攝影會【2026年3月21日】-「個人加購拍攝券」": {
        "森日向子攝影會第一場加購 (12:00–13:00)": "https://javstarmeet.com/collections/%E6%94%9D%E5%BD%B1%E6%9C%83/products/%E2%8F%B1%EF%B8%8F-%F0%9F%93%B8-%E6%A3%AE%E6%97%A5%E5%90%91%E5%AD%90-%E9%A6%99%E6%B8%AF%E7%B2%89%E7%B5%B2%E6%94%9D%E5%BD%B1%E6%9C%83-2026%E5%B9%B43%E6%9C%8824%E6%97%A5-%E5%80%8B%E4%BA%BA%E5%8A%A0%E8%B3%BC%E6%8B%8D%E6%94%9D%E5%88%B8?variant=52007361511705",
        "森日向子攝影會第二場加購 (13:50–14:50)": "https://javstarmeet.com/collections/%E6%94%9D%E5%BD%B1%E6%9C%83/products/%E2%8F%B1%EF%B8%8F-%F0%9F%93%B8-%E6%A3%AE%E6%97%A5%E5%90%91%E5%AD%90-%E9%A6%99%E6%B8%AF%E7%B2%89%E7%B5%B2%E6%94%9D%E5%BD%B1%E6%9C%83-2026%E5%B9%B43%E6%9C%8824%E6%97%A5-%E5%80%8B%E4%BA%BA%E5%8A%A0%E8%B3%BC%E6%8B%8D%E6%94%9D%E5%88%B8?variant=52007361544473",
        "森日向子攝影會第三場加購 (15:40–16:40)": "https://javstarmeet.com/collections/%E6%94%9D%E5%BD%B1%E6%9C%83/products/%E2%8F%B1%EF%B8%8F-%F0%9F%93%B8-%E6%A3%AE%E6%97%A5%E5%90%91%E5%AD%90-%E9%A6%99%E6%B8%AF%E7%B2%89%E7%B5%B2%E6%94%9D%E5%BD%B1%E6%9C%83-2026%E5%B9%B43%E6%9C%8824%E6%97%A5-%E5%80%8B%E4%BA%BA%E5%8A%A0%E8%B3%BC%E6%8B%8D%E6%94%9D%E5%88%B8?variant=52007361577241",
    },
    "森日向子 香港粉絲見面會【 2026年3月22日】- 入場券": {
        "森日向子見面會入場券第一場 (13:00 – 16:00)": "https://javstarmeet.com/collections/%E8%A6%8B%E9%9D%A2%E6%9C%83/products/%E6%A3%AE%E6%97%A5%E5%90%91%E5%AD%90-%E9%A6%99%E6%B8%AF%E7%B2%89%E7%B5%B2%E8%A6%8B%E9%9D%A2%E6%9C%83-2026%E5%B9%B43%E6%9C%8822%E6%97%A5-%E5%85%A5%E5%A0%B4%E5%88%B8?variant=52000804339993",
        "森日向子見面會入場券第二場 ( 16:50 – 19:50)": "https://javstarmeet.com/collections/%E8%A6%8B%E9%9D%A2%E6%9C%83/products/%E6%A3%AE%E6%97%A5%E5%90%91%E5%AD%90-%E9%A6%99%E6%B8%AF%E7%B2%89%E7%B5%B2%E8%A6%8B%E9%9D%A2%E6%9C%83-2026%E5%B9%B43%E6%9C%8822%E6%97%A5-%E5%85%A5%E5%A0%B4%E5%88%B8?variant=52003534864665"
    },
    "森日向子 香港粉絲見面會【 2026年3月22日】- 合照券":{
        "森日向子見面會合照券第一場 (13:00 – 16:00)": "https://javstarmeet.com/collections/%E8%A6%8B%E9%9D%A2%E6%9C%83/products/%E6%A3%AE%E6%97%A5%E5%90%91%E5%AD%90-%E9%A6%99%E6%B8%AF%E7%B2%89%E7%B5%B2%E8%A6%8B%E9%9D%A2%E6%9C%83-2026%E5%B9%B43%E6%9C%8822%E6%97%A5-%E5%90%88%E7%85%A7%E5%88%B8?variant=52003619176729",
        "森日向子見面會合照券第二場 ( 16:50 – 19:50)": "https://javstarmeet.com/collections/%E8%A6%8B%E9%9D%A2%E6%9C%83/products/%E6%A3%AE%E6%97%A5%E5%90%91%E5%AD%90-%E9%A6%99%E6%B8%AF%E7%B2%89%E7%B5%B2%E8%A6%8B%E9%9D%A2%E6%9C%83-2026%E5%B9%B43%E6%9C%8822%E6%97%A5-%E5%90%88%E7%85%A7%E5%88%B8?variant=52003619209497"
    },
    "森日向子 粉絲攝影會（2026年3月22日）- 10秒個人攝影券":{
        "森日向子見面會10秒個人攝影券第一場 (13:00 – 16:00)": "https://javstarmeet.com/collections/%E8%A6%8B%E9%9D%A2%E6%9C%83/products/%E6%A3%AE%E6%97%A5%E5%90%91%E5%AD%90-%E9%A6%99%E6%B8%AF%E7%B2%89%E7%B5%B2%E8%A6%8B%E9%9D%A2%E6%9C%83-2025%E5%B9%B43%E6%9C%8825%E6%97%A5-10%E7%A7%92%E8%87%AA%E6%8B%8D%E5%88%B8?variant=52007369277721",
        "森日向子見面會10秒個人攝影券第二場 ( 16:50 – 19:50)": "https://javstarmeet.com/collections/%E8%A6%8B%E9%9D%A2%E6%9C%83/products/%E6%A3%AE%E6%97%A5%E5%90%91%E5%AD%90-%E9%A6%99%E6%B8%AF%E7%B2%89%E7%B5%B2%E8%A6%8B%E9%9D%A2%E6%9C%83-2025%E5%B9%B43%E6%9C%8825%E6%97%A5-10%E7%A7%92%E8%87%AA%E6%8B%8D%E5%88%B8?variant=52007369310489"
    },
    "森日向子 香港粉絲見面會【 2026年3月22日】- 10秒自拍券":{
        "森日向子見面會10秒自拍券第一場 (13:00 – 16:00)": "https://javstarmeet.com/collections/%E8%A6%8B%E9%9D%A2%E6%9C%83/products/%E2%9C%8D%EF%B8%8F%E6%A3%AE%E6%97%A5%E5%90%91%E5%AD%90%E9%A6%99%E6%B8%AF%E7%B2%89%E7%B5%B2%E8%A6%8B%E9%9D%A2%E6%9C%83-2026%E5%B9%B43%E6%9C%8822%E6%97%A5-%E7%B0%BD%E5%90%8D%E5%88%B8-autograph?variant=52010247455001",
        "森日向子見面會10秒自拍券第二場 ( 16:50 – 19:50)": "https://javstarmeet.com/collections/%E8%A6%8B%E9%9D%A2%E6%9C%83/products/%E2%9C%8D%EF%B8%8F%E6%A3%AE%E6%97%A5%E5%90%91%E5%AD%90%E9%A6%99%E6%B8%AF%E7%B2%89%E7%B5%B2%E8%A6%8B%E9%9D%A2%E6%9C%83-2026%E5%B9%B43%E6%9C%8822%E6%97%A5-%E7%B0%BD%E5%90%8D%E5%88%B8-autograph?variant=52010247487769"
    },
    "森日向子香港粉絲見面會（2026年3月22日）- 簽名券（Autograph）":{
        "森日向子見面會簽名券第一場 (13:00 – 16:00)": "https://javstarmeet.com/collections/%E8%A6%8B%E9%9D%A2%E6%9C%83/products/%F0%9F%93%B8-%E6%A3%AE%E6%97%A5%E5%90%91%E5%AD%90-%E7%B2%89%E7%B5%B2%E6%94%9D%E5%BD%B1%E6%9C%83-2026%E5%B9%B43%E6%9C%8815%E6%97%A5-10%E7%A7%92%E5%80%8B%E4%BA%BA%E6%94%9D%E5%BD%B1%E5%88%B8?variant=52014378909977",
        "森日向子見面會簽名券第二場 ( 16:50 – 19:50)": "https://javstarmeet.com/collections/%E8%A6%8B%E9%9D%A2%E6%9C%83/products/%F0%9F%93%B8-%E6%A3%AE%E6%97%A5%E5%90%91%E5%AD%90-%E7%B2%89%E7%B5%B2%E6%94%9D%E5%BD%B1%E6%9C%83-2026%E5%B9%B43%E6%9C%8815%E6%97%A5-10%E7%A7%92%E5%80%8B%E4%BA%BA%E6%94%9D%E5%BD%B1%E5%88%B8?variant=52014378909977"
    },
    "森日向子 香港粉絲見面會【 2026年3月22日】- 15秒Video錄影劵":{
    "森日向子15秒Video錄影劵": "https://javstarmeet.com/collections/%E8%A6%8B%E9%9D%A2%E6%9C%83/products/%E6%A3%AE%E6%97%A5%E5%90%91%E5%AD%90-%E9%A6%99%E6%B8%AF%E7%B2%89%E7%B5%B2%E8%A6%8B%E9%9D%A2%E6%9C%83-2025%E5%B9%B43%E6%9C%8825%E6%97%A5-15%E7%A7%92video%E9%8C%84%E5%BD%B1%E5%8A%B5"
    },
    "森日向子 香港粉絲見面會【 2026年3月22日】- 唇印簽名劵":{
    "森日向子唇印簽名劵": "https://javstarmeet.com/collections/%E8%A6%8B%E9%9D%A2%E6%9C%83/products/%E6%A3%AE%E6%97%A5%E5%90%91%E5%AD%90-%E9%A6%99%E6%B8%AF%E7%B2%89%E7%B5%B2%E8%A6%8B%E9%9D%A2%E6%9C%83-2025%E5%B9%B43%E6%9C%8825%E6%97%A5-%E5%94%87%E5%8D%B0%E7%B0%BD%E5%90%8D%E5%8A%B5"
    },
    "森日向子 粉絲見面會（2026年3月22號）- 教師挑戰劵":{
    "森日向子教師挑戰劵": "https://javstarmeet.com/collections/%E8%A6%8B%E9%9D%A2%E6%9C%83/products/%F0%9F%91%A9%E2%80%8D%F0%9F%8F%AB-%E6%95%99%E5%B8%AB%E6%8C%91%E6%88%B0%E5%8A%B5"
    }
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
