#-*-coding:utf-8-*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import requests
import fake_useragent

ua = fake_useragent.UserAgent()

hd ={'USER_AGENT' :ua.random}

class LlssAll_abstrct_Pipeline(object):
    def process_item(self, item, spider):
        print('\ntrying to write results into files\n')
        if not os.path.isdir('./abstract/'):
            os.mkdir('./abstract')
        path = './abstract/abstract_' + '_' + str(item['post_date']) + '_' + item['title'] + '.txt'
        with open(path, 'a', encoding='utf-8') as f:
            f.write('=' * 75)
            f.write('\nmagnet-links:\n')
            for m in item['magnet_without_prefix']:
                if str(m[0:4])!='http':
                    f.write('magnet:?xt=urn:btih:' + str(m) + '\n')
            for m in item['magnet_with_prefix']:
                f.write(str(m) + '\n')
            f.write('='*75+'\nabstract:\n')
            for a in item['abstract']:
                f.write(str(a))
            f.write('='*75+'\n\n')
        print('done\n')
        return item

class LlssAll_image_Pipeline(object):
    def process_item(self, item, spider):
        print('\ntrying to download images:\n')
        if not os.path.isdir('./image/'):
            os.mkdir('./image')
        path = './image/' + '_' + str(item['post_date']) + '_' + item['title'] + '/'
        if not os.path.isdir(path):
            os.mkdir(path)
        for i in range(0,len(item['image_urls'])):
            tmp_path = path + str(i) + str(item['image_type'][i])
            with open(tmp_path,'wb') as f:
                data = requests.get(str(item['image_urls'][i]),timeout = 1,headers = hd)
                f.write(data.content)
        print('done\n')
        return item
