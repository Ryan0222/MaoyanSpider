import requests
from requests.exceptions import RequestException
import re
import json
from multiprocessing import Pool

headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'Cookie': '__mta=147618056.1618365412680.1619394319019.1619394650272.10; uuid_n_v=v1; uuid=ABA321509CC411EB8D235D7A7A6C3816470E2627CEA842CAB9CE8E5DBE1B9575; _lxsdk_cuid=178ce186674c8-0f6423d0bf61d3-11114659-1fa400-178ce186674c8; _lxsdk=ABA321509CC411EB8D235D7A7A6C3816470E2627CEA842CAB9CE8E5DBE1B9575; _csrf=28ac0066c983eb776ae56a1d27087ad0883065f9556b319d1cec820ee48032c5; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1618365409,1619386378,1619390080; _lx_utm=utm_source=google&utm_medium=organic; __mta=147618056.1618365412680.1619394319019.1619394647048.10; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1619394650; _lxsdk_s=1790b6c4b02-bbc-334-a||8'
}

def get_one_page(url):
    try:
        response = requests.get(url, headers = headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None
def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
                        +'.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                        +'.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[5:],
            'score': item[5] + item[6]
        }

def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()
def main(offset):
    url = "https://maoyan.com/board/4?offset=" + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        write_to_file(item)

if __name__ == "__main__":
    pool = Pool()
    pool.map(main, [i*10 for i in range(10)])