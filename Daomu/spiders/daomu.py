# -*- coding: utf-8 -*-
import scrapy
from ..items import DaomuItem

class DaommuSpider(scrapy.Spider):
    name = 'daomu'
    allowed_domains = ['www.daomubiji.com']
    start_urls = ['http://www.daomubiji.com/']

    # 一级页面解析函数,提取盗墓笔记1-8链接,发给调度器入队列
    def parse(self, response):
        one_link_list = response.xpath('//ul[@class="sub-menu"]/li/a/@href').extract()
        # 把请求发给调度器
        for one_link in one_link_list:
            yield scrapy.Request(
                url=one_link,
                callback=self.parse_two_link
            )


    # 解析二级页面函数
    def parse_two_link(self,response):
        # 基准xpath(每个章节节点对象列表)
        article_list = response.xpath('/html/body/section/div[2]/div/article')
        # for遍历,继续调用xpath()
        for article in article_list:
            # 创建item对象,用于交给管道 yield item
            item = DaomuItem()
            info = article.xpath('./a/text()').extract_first().split()
            # info: ['七星鲁王宫','第一章','血尸']
            # 卷名
            item['juan_name'] = info[0]

            #章节数量
            item['zh_num'] = info[1]

            #章节名称
            item['zh_name'] = info[2]

            #章节链接
            item['zh_link'] = article.xpath('./a/@href').get()

            # 把链接交给调度器入队列
            yield scrapy.Request(
                url=item['zh_link'],
                callback=self.parse_three_link,
                # meta在不同函数之间传递参数
                # meta->调度器->下载器->作为response一个属性
                # 传递给下一个解析函数
                meta={'item':item}
            )


    # 解析三级页面,小说内容
    def parse_three_link(self,response):
        # response.meta:获取字典:{'item',item}
        item = response.meta['item']
        note_list = response.xpath('/html/body/section/div[1]/div/article/p/text()').extract()
        # note_list:['段落1','段落2','段落3']
        item['zh_content'] = '\n'.join(note_list).replace('\u3000','')

        # 交给管道(一定要把所有数据获取完后再 yield item)
        yield item
