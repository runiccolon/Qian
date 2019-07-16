# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class DaomuPipeline(object):
    def process_item(self, item, spider):
        print(item['zh_content'])
        print('*'*50)
        # 把小说内容保存到本地文件
        filename = '../盗墓笔记/{}-{}-{}.txt'.format(
            item['juan_name'],
            item['zh_num'],
            item['zh_name']
        )
        f = open(filename,'w',encoding='utf-8')
        f.write(item['zh_content'])
        f.close()

        return item
