import scrapy
import json


class MangoSpider(scrapy.Spider):
   
    name = 'mango-spider'
    start_urls = ['https://shop.mango.com/bg-en/women/skirts-midi/midi-satin-skirt_17042020.html?c=99']

    
    #Headers used for requests 
    headers = {
        'stock-id' : '068.IN.0.false.false.v1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
        'accept': 'application/json, text/plain, */*'
    }


    def parse(self, response):
        url = 'https://shop.mango.com/services/garments/{0}99'.format(self.__get_item_id())
        yield scrapy.Request(url, callback=self.parse_app, headers=self.headers)
        
    '''
        Read responce, extract data and save to json file 
    '''
    def parse_app(self, response):
        raw_data = response.body
        data = json.loads(raw_data)
        
        with open('{}.json'.format(self.__get_item_id()), 'w') as f:
            json.dump(self.get_product_data(data, self.__get_selected_color_id()), f)
            f.close()
        
    '''
        Get all data from the item page as dict 
    '''
    def get_product_data(self, data, color_id):
        items = data['colors']['colors']
        color_name = ''
        size_list = []

        for item in items:
            if item['id'] == str(color_id):
                color_name = item['label']
                
                for i in item['sizes']:
                    if i['label'] == 'Choose your size':
                        continue
                    else:
                        size_list.append(i['label'])

        return {
            'name'  : data['name'],
            'price' : float(data['price']['price']),
            'color' : color_name,
            'sizes' : size_list 
        }
    

    def __get_item_id(self):
        return self.start_urls[0].split('_')[1].split('.')[0]
    
    def __get_default_color_id(self,data):
        return data['colors']['colors'][0]['id']

    def __get_selected_color_id(self):
        return self.start_urls[0].split('_')[1].split('.')[1].split('=')[1]