from datetime import datetime
import requests
import scrapy
import json
import time


class SlaveryIndexSpider(scrapy.Spider):
    name = "slavery_index"
    start_urls = ["https://www.walkfree.org/global-slavery-index/downloads/"]
    custom_settings = {
        "USER_AGENT" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    }

    def parse(self, response):
        for data_id in response.css('div.minderbergResource__resource.minderbergResource__resourceModalLink'):
            id = data_id.css('::attr(data-id)').get()
            r = self.request_api(id)
            if r.status_code == 200:
                data_json = r.json()
                for translation in data_json["resource"]["translations"]:
                    try:
                        link_download = translation["file"]["url"]
                    except TypeError as e:
                        link_download = translation["link_url"]
                    yield scrapy.Request(url=link_download, callback=self.download_file)
            else:
                print(r.status_code)
                
    def download_file(self, response):  
        crawling_epoch = int(datetime.now().timestamp())
        file_name = response.url.split('/')[-1]
        ext = file_name.split('.')[-1]
        local_path = f'F:/Work/Garapan gweh/html/walkfree/downloaded/{crawling_epoch}_{file_name}'
        with open(local_path, 'wb') as f:
            f.write(response.body)
    
    def request_api(self, id):
        cookies = {
            '_fbp': 'fb.1.1711077723857.1046228196',
            '_hjSessionUser_3450753': 'eyJpZCI6Ijc2MzU2NDM2LWY5ZWMtNTA1OS04NzM5LWQzZGZlZjJkODEyYiIsImNyZWF0ZWQiOjE3MTEwNzc3MjM5MDcsImV4aXN0aW5nIjp0cnVlfQ==',
            '_gid': 'GA1.2.338198540.1711286573',
            '_ga': 'GA1.1.514578531.1711077724',
            '_hjSession_3450753': 'eyJpZCI6IjAxOGIzZGUxLTE5ZGYtNDFmOS05MDMzLWVlYTUwY2M2NjJiYSIsImMiOjE3MTEzMzcwNDc2MjUsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=',
            'AWSALB': 'Ndv8g9IfHQNYpNVQXu39as7ZWTYrwwHZhqObkdlYqLCu12+y0aJUu3BxY4hIC/5TrQr4CowaS3GKg9jGUSpY49kT505h8uvA4wFYZVqUEq5g6jjbDA2t18mI3Z7C',
            'AWSALBCORS': 'Ndv8g9IfHQNYpNVQXu39as7ZWTYrwwHZhqObkdlYqLCu12+y0aJUu3BxY4hIC/5TrQr4CowaS3GKg9jGUSpY49kT505h8uvA4wFYZVqUEq5g6jjbDA2t18mI3Z7C',
            '_ga_BLJ2LCP865': 'GS1.1.1711337047.10.1.1711337844.37.0.455002810',
        }
        headers = {
            'accept': '*/*',
            'accept-language': 'en,id-ID;q=0.9,id;q=0.8,en-US;q=0.7',
            'cache-control': 'no-cache',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            # 'cookie': '_fbp=fb.1.1711077723857.1046228196; _hjSessionUser_3450753=eyJpZCI6Ijc2MzU2NDM2LWY5ZWMtNTA1OS04NzM5LWQzZGZlZjJkODEyYiIsImNyZWF0ZWQiOjE3MTEwNzc3MjM5MDcsImV4aXN0aW5nIjp0cnVlfQ==; _gid=GA1.2.338198540.1711286573; _ga=GA1.1.514578531.1711077724; _hjSession_3450753=eyJpZCI6IjAxOGIzZGUxLTE5ZGYtNDFmOS05MDMzLWVlYTUwY2M2NjJiYSIsImMiOjE3MTEzMzcwNDc2MjUsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; AWSALB=Ndv8g9IfHQNYpNVQXu39as7ZWTYrwwHZhqObkdlYqLCu12+y0aJUu3BxY4hIC/5TrQr4CowaS3GKg9jGUSpY49kT505h8uvA4wFYZVqUEq5g6jjbDA2t18mI3Z7C; AWSALBCORS=Ndv8g9IfHQNYpNVQXu39as7ZWTYrwwHZhqObkdlYqLCu12+y0aJUu3BxY4hIC/5TrQr4CowaS3GKg9jGUSpY49kT505h8uvA4wFYZVqUEq5g6jjbDA2t18mI3Z7C; _ga_BLJ2LCP865=GS1.1.1711337047.10.1.1711337844.37.0.455002810',
            'origin': 'https://www.walkfree.org',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://www.walkfree.org/global-slavery-index/downloads/',
            'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
            'x-wp-nonce': '9acb502fb9',
        }

        data = {
            'action': 'get-resource',
            'resourceId': id,
        }

        r = requests.post(
            'https://www.walkfree.org/wp-json/minderberg/resource-list/v1/get-resource',
            cookies=cookies,
            headers=headers,
            data=data,
        )
        return r