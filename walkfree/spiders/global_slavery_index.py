from datetime import datetime
import pycountry
import requests
import scrapy
import json


class GlobalSlaveryIndexSpider(scrapy.Spider):
    name = "global_slavery_index"
    allowed_domains = ["www.walkfree.org"]
    start_urls = ["https://www.walkfree.org/global-slavery-index/"]

    def parse(self, response):
        link = response.url
        domain = link.split("/")[2]
        title = "Global Slavery Index"
        most_prevalent = response.css("body > section > div:nth-child(3) > div > div > div > div > div > div.minderbergColumns__column.suid-34 > div > div:nth-child(2) > div > div > p::text").get()
        img_most_prevalent = response.css("body > section > div:nth-child(3) > div > div > div > div > div > div.minderbergColumns__column.suid-34 > div > div.minderbergImage.suid-32 > div > div > span > span > img::attr(src)").get()
        
        pdf_link = response.css("body > section > div:nth-child(16) > div > div > div > div > div > div:nth-child(2) > div > div.minderbergFlex.minderbergFlex--fg-core-black.suid-208 > div > div > div.minderbergResource > div > div > div > a::attr(href)").get()
        
        least_prevalent = response.css("body > section > div:nth-child(3) > div > div > div > div > div > div:nth-child(2) > div > div:nth-child(2) > div > div > p::text").get()
        img_least_prevalent = response.css("body > section > div:nth-child(3) > div > div > div > div > div > div:nth-child(2) > div > div.minderbergImage.suid-36 > div > div > span > span > img::attr(src)").get()
        
        modern_slavery_mean = response.css("body > section > div:nth-child(4) > div > div > div.minderbergColumns.minderbergColumns--layout3.minderbergColumns--unstackedDesktop.minderbergColumns--unstackedTablet.minderbergColumns--stackedMobile.suid-44 > div > div > div:nth-child(1) > div > div.minderbergHeading.minderbergHeading--font2.minderbergHeading--size3.minderbergHeading--color-walkfree-deep-blue.suid-42 > div > div > h3 > strong::text").get()
        
        r = self.govern_response()
        if r.status_code == 200:
            data_governs = r.json()
            for data_govern in data_governs:
                crawling_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                crawling_time_epoch = int(datetime.now().timestamp())
                iso = data_govern["iso"]
                country_name = pycountry.countries.get(alpha_3=iso)
                if country_name is not None:
                    country_name = country_name.name
                govern_value = data_govern["value"]
                if govern_value is not None:
                    govern_value = round(govern_value, 1)

                data_json = {
                    "link" : link,
                    "domain" : domain,
                    "data_name" : title,
                    "title": title,
                    "modern_slavery_mean": modern_slavery_mean,
                    "most_prevalent": most_prevalent,
                    "img_most_prevalent": img_most_prevalent,
                    "least_prevalent": least_prevalent,
                    "img_least_prevalent": img_least_prevalent,
                    "full_report": pdf_link,
                    "details": {
                        "iso": iso,
                        "country_name": country_name,
                        "government_response_to_modern_slavery_percent": govern_value,
                        "imports" : None
                    },
                    "path_data_raw" : None,
                    "crawling_time" : crawling_time,
                    "crawling_time_epoch" : crawling_time_epoch
                }

                res = self.import_response(iso)
                if res.status_code == 200:
                    data_imports = res.json()
                    for data_import in data_imports:
                        if iso == data_import["country"]:
                            data_json["details"]["imports"] = data_import["products"]
                    file_name = f"{crawling_time_epoch}_{iso.lower()}.json"
                    local_path = f"F:/Work/Garapan gweh/html/walkfree/json/{file_name}"
                    data_json["path_data_raw"] = local_path
                    with open(local_path, "w") as f:
                        json.dump(data_json, f)
        else:
            print(r.status_code)
    
    def import_response(self, iso):
        cookies = {
            '_fbp': 'fb.1.1711077723857.1046228196',
            '_hjSessionUser_3450753': 'eyJpZCI6Ijc2MzU2NDM2LWY5ZWMtNTA1OS04NzM5LWQzZGZlZjJkODEyYiIsImNyZWF0ZWQiOjE3MTEwNzc3MjM5MDcsImV4aXN0aW5nIjp0cnVlfQ==',
            '_gid': 'GA1.2.338198540.1711286573',
            '_ga': 'GA1.1.514578531.1711077724',
            '_hjSession_3450753': 'eyJpZCI6IjkxNTA0Y2U2LTRiZWItNGM4ZC1hM2M1LThkODQ5MTRlOWIyYiIsImMiOjE3MTEzNDI2MTMwOTksInMiOjEsInIiOjEsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MX0=',
            '_ga_BLJ2LCP865': 'GS1.1.1711347351.13.1.1711349285.55.0.420892895',
            'AWSALB': 'w6GBst8P7dyaMROLpbNx/J176Zp8MNRKE1KqqHTPGYhH30UQjvRcuzGWYldvEJD0ywwTr/KGnImX4FV4fot99+ax3ER21JylVNi/Ijfh4gvzxjqXLGCGQEf9HND5',
            'AWSALBCORS': 'w6GBst8P7dyaMROLpbNx/J176Zp8MNRKE1KqqHTPGYhH30UQjvRcuzGWYldvEJD0ywwTr/KGnImX4FV4fot99+ax3ER21JylVNi/Ijfh4gvzxjqXLGCGQEf9HND5',
        }
        headers = {
            'accept': '*/*',
            'accept-language': 'en,id-ID;q=0.9,id;q=0.8,en-US;q=0.7',
            'cache-control': 'no-cache',
            # 'cookie': '_fbp=fb.1.1711077723857.1046228196; _hjSessionUser_3450753=eyJpZCI6Ijc2MzU2NDM2LWY5ZWMtNTA1OS04NzM5LWQzZGZlZjJkODEyYiIsImNyZWF0ZWQiOjE3MTEwNzc3MjM5MDcsImV4aXN0aW5nIjp0cnVlfQ==; _gid=GA1.2.338198540.1711286573; _ga=GA1.1.514578531.1711077724; _hjSession_3450753=eyJpZCI6IjkxNTA0Y2U2LTRiZWItNGM4ZC1hM2M1LThkODQ5MTRlOWIyYiIsImMiOjE3MTEzNDI2MTMwOTksInMiOjEsInIiOjEsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MX0=; _ga_BLJ2LCP865=GS1.1.1711347351.13.1.1711349285.55.0.420892895; AWSALB=w6GBst8P7dyaMROLpbNx/J176Zp8MNRKE1KqqHTPGYhH30UQjvRcuzGWYldvEJD0ywwTr/KGnImX4FV4fot99+ax3ER21JylVNi/Ijfh4gvzxjqXLGCGQEf9HND5; AWSALBCORS=w6GBst8P7dyaMROLpbNx/J176Zp8MNRKE1KqqHTPGYhH30UQjvRcuzGWYldvEJD0ywwTr/KGnImX4FV4fot99+ax3ER21JylVNi/Ijfh4gvzxjqXLGCGQEf9HND5',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://www.walkfree.org/global-slavery-index/',
            'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        }

        params = {
            'iso[]': [
                iso
            ],
        }

        r = requests.get(
            'https://www.walkfree.org/wp-json/minderberg/gsi/v1/imports',
            params=params,
            cookies=cookies,
            headers=headers,
        )
        
        return r
    
    def govern_response(self):
        cookies = {
            '_fbp': 'fb.1.1711077723857.1046228196',
            '_hjSessionUser_3450753': 'eyJpZCI6Ijc2MzU2NDM2LWY5ZWMtNTA1OS04NzM5LWQzZGZlZjJkODEyYiIsImNyZWF0ZWQiOjE3MTEwNzc3MjM5MDcsImV4aXN0aW5nIjp0cnVlfQ==',
            '_gid': 'GA1.2.338198540.1711286573',
            '_ga': 'GA1.1.514578531.1711077724',
            '_hjSession_3450753': 'eyJpZCI6IjkxNTA0Y2U2LTRiZWItNGM4ZC1hM2M1LThkODQ5MTRlOWIyYiIsImMiOjE3MTEzNDI2MTMwOTksInMiOjEsInIiOjEsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MX0=',
            '_ga_BLJ2LCP865': 'GS1.1.1711347351.13.1.1711349285.55.0.420892895',
            'AWSALB': 'w6GBst8P7dyaMROLpbNx/J176Zp8MNRKE1KqqHTPGYhH30UQjvRcuzGWYldvEJD0ywwTr/KGnImX4FV4fot99+ax3ER21JylVNi/Ijfh4gvzxjqXLGCGQEf9HND5',
            'AWSALBCORS': 'w6GBst8P7dyaMROLpbNx/J176Zp8MNRKE1KqqHTPGYhH30UQjvRcuzGWYldvEJD0ywwTr/KGnImX4FV4fot99+ax3ER21JylVNi/Ijfh4gvzxjqXLGCGQEf9HND5',
        }
        headers = {
            'accept': '*/*',
            'accept-language': 'en,id-ID;q=0.9,id;q=0.8,en-US;q=0.7',
            'cache-control': 'no-cache',
            # 'cookie': '_fbp=fb.1.1711077723857.1046228196; _hjSessionUser_3450753=eyJpZCI6Ijc2MzU2NDM2LWY5ZWMtNTA1OS04NzM5LWQzZGZlZjJkODEyYiIsImNyZWF0ZWQiOjE3MTEwNzc3MjM5MDcsImV4aXN0aW5nIjp0cnVlfQ==; _gid=GA1.2.338198540.1711286573; _ga=GA1.1.514578531.1711077724; _hjSession_3450753=eyJpZCI6IjkxNTA0Y2U2LTRiZWItNGM4ZC1hM2M1LThkODQ5MTRlOWIyYiIsImMiOjE3MTEzNDI2MTMwOTksInMiOjEsInIiOjEsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MX0=; _ga_BLJ2LCP865=GS1.1.1711347351.13.1.1711349285.55.0.420892895; AWSALB=w6GBst8P7dyaMROLpbNx/J176Zp8MNRKE1KqqHTPGYhH30UQjvRcuzGWYldvEJD0ywwTr/KGnImX4FV4fot99+ax3ER21JylVNi/Ijfh4gvzxjqXLGCGQEf9HND5; AWSALBCORS=w6GBst8P7dyaMROLpbNx/J176Zp8MNRKE1KqqHTPGYhH30UQjvRcuzGWYldvEJD0ywwTr/KGnImX4FV4fot99+ax3ER21JylVNi/Ijfh4gvzxjqXLGCGQEf9HND5',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://www.walkfree.org/global-slavery-index/',
            'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        }
        params = {
            'dimensionId': 'r',
            'iso[]': [
                'AFG',
                'ALB',
                'DZA',
                'AGO',
                'ATG',
                'ARG',
                'ARM',
                'AUS',
                'AUT',
                'AZE',
                'BHS',
                'BHR',
                'BGD',
                'BRB',
                'BLR',
                'BEL',
                'BLZ',
                'BEN',
                'BOL',
                'BIH',
                'BWA',
                'BRA',
                'BRN',
                'BGR',
                'BFA',
                'BDI',
                'KHM',
                'CMR',
                'CAN',
                'CPV',
                'CAF',
                'TCD',
                'CHL',
                'CHN',
                'COL',
                'COG',
                'COD',
                'CRI',
                'CIV',
                'HRV',
                'CUB',
                'CYP',
                'CZE',
                'DNK',
                'DJI',
                'DOM',
                'ECU',
                'EGY',
                'SLV',
                'GNQ',
                'ERI',
                'EST',
                'ETH',
                'FJI',
                'FIN',
                'FRA',
                'GAB',
                'GMB',
                'GEO',
                'DEU',
                'GHA',
                'GRC',
                'GTM',
                'GIN',
                'GNB',
                'GUY',
                'HTI',
                'HND',
                'HKG',
                'HUN',
                'ISL',
                'IND',
                'IDN',
                'IRN',
                'IRQ',
                'IRL',
                'ISR',
                'ITA',
                'JAM',
                'JPN',
                'JOR',
                'KAZ',
                'KEN',
                'PRK',
                'KOR',
                'XKX',
                'KWT',
                'KGZ',
                'LAO',
                'LVA',
                'LBN',
                'LSO',
                'LBR',
                'LBY',
                'LTU',
                'LUX',
                'MKD',
                'MDG',
                'MWI',
                'MYS',
                'MLI',
                'MLT',
                'MRT',
                'MUS',
                'MEX',
                'MDA',
                'MNG',
                'MNE',
                'MAR',
                'MOZ',
                'MMR',
                'NAM',
                'NPL',
                'NLD',
                'NZL',
                'NIC',
                'NER',
                'NGA',
                'NOR',
                'OMN',
                'PAK',
                'PLW',
                'PAN',
                'PNG',
                'PRY',
                'PER',
                'PHL',
                'POL',
                'PRT',
                'QAT',
                'ROU',
                'RUS',
                'RWA',
                'LCA',
                'VCT',
                'SAU',
                'SEN',
                'SRB',
                'SYC',
                'SLE',
                'SGP',
                'SVK',
                'SVN',
                'SLB',
                'SOM',
                'ZAF',
                'SSD',
                'ESP',
                'LKA',
                'SDN',
                'SUR',
                'SWZ',
                'SWE',
                'CHE',
                'SYR',
                'TWN',
                'TJK',
                'TZA',
                'THA',
                'TLS',
                'TGO',
                'TTO',
                'TUN',
                'TUR',
                'TKM',
                'UGA',
                'UKR',
                'ARE',
                'GBR',
                'USA',
                'URY',
                'UZB',
                'VUT',
                'VEN',
                'VNM',
                'YEM',
                'ZMB',
                'ZWE',
                'LIE',
                'MDV',
            ],
        }

        r = requests.get(
            'https://www.walkfree.org/wp-json/minderberg/gsi/v1/values',
            params=params,
            cookies=cookies,
            headers=headers,
        )
        
        return r
        