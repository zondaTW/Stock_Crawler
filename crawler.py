import argparse
import requests
import json


class GetStock:
    def __init__(self, stock_num):
        self.stock_key = self.find_stock_key(stock_num)

    def find_stock_key(self, stock_num):
        get_stock_req = requests.get(f"http://mis.tse.com.tw/stock/api/getStock.jsp?ch={stock_num}.tw")
        msg_array = json.loads(get_stock_req.text)['msgArray']
        stock_key = None
        if msg_array:
            stock_key = msg_array[0]['key']
        else:
            print(f"Stock number({stock_num}) not exists.")
        return stock_key


class GetStockInfo:
    def __init__(self, stock_key):
        self.stock_info = self.get_stock_info(stock_key)

    def get_stock_info(self, stock_key):
        if not stock_key:
            return None
        get_stock_info_req = requests.get(f"http://mis.tse.com.tw/stock/api/getStockInfo.jsp?ex_ch={stock_key}")
        stock_info_json = json.loads(get_stock_info_req.text)
        stock_info = None
        if stock_info_json['rtmessage'] != "Information Data Not Found":
            stock_info = stock_info_json['msgArray'][0]
        else:
            print(f"Stock key({stock_key}) not exists.")
        return stock_info

    def __str__(self):
        if not self.stock_info:
            return ""
        chinese_space = chr(12288)
        dict_map = {
            '股票號碼': 'c',
            '日期': 'd',
            '公司名稱': 'nf',
            '開盤': 'o',
            '最高': 'h',
            '最低': 'l',
        }
        return '\n'.join([f'{title:{chinese_space}<7}: {self.stock_info[key]}' for title, key in dict_map.items()])


class StockCrawler(GetStock, GetStockInfo):
    def __init__(self, stock_num):
        GetStock.__init__(self, stock_num)
        GetStockInfo.__init__(self, self.stock_key)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stock Crawler")
    required_arg = parser.add_argument_group('required arguments')
    required_arg.add_argument("-n", "--number", help="Stock number", dest="stock_num", required=True)
    args = parser.parse_args()

    print(StockCrawler(args.stock_num))