# coding:utf-8
# author:alex lin
import re
import uuid
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from sinahouse.items import SinaHouseItem
from sinahouse import settings


class SinaHouseSpider(CrawlSpider):
    name = 'sinahouse'
    allowed_domains = ['house.sina.com.cn']
    start_urls = ['http://data.house.sina.com.cn/sc/search/?keyword=&charset=utf8',]
    rules = [
            Rule(LinkExtractor(allow = ('.*\.cn/\w+\d+\?wt_source.*?bt.*')),callback='parse_item',follow=False), #楼盘链接提取
            Rule(LinkExtractor(allow = ('^http://data.house.sina.com.cn/\w+/search/$')),process_links="parse_city_links"), #各个城市链接提取
            Rule(LinkExtractor(allow = ('/\w+/search-\d*/.*'))), #下一页链接
 
            ]

#     ,process_links="parse_city_next_links"
#    下一页链接url提取出来实际是相对路径,LinkExtractor自动补全了url路径 故省略
#     def parse_city_next_links(self,links):
#         for link in links:
#             link.url = "http://data.house.sina.com.cn" + link.url
#         return links
    def parse_city_links(self,links):
        for link in links:
            link.url = link.url +'?keyword=&charset=utf8'
        return links
        
    def parse_item(self,response):
        item = SinaHouseItem()
        item['source_id'] = settings.SOURCE
#       item['save_path'] = settings.IMAGE_PATH
        item['community_name'] = response.xpath('/html/body/div[1]/div[9]/div[1]/h2/text()').extract_first()
        item['index_url'] = response.url
        item['open_date'] = '-'.join(re.findall('(\d+)',response.xpath(u"//*[@id='callmeBtn']/ul/li[4]/span[2]/text()").extract_first(default=u'待定').strip()))
        item['check_in_date'] = '-'.join(re.findall('(\d+)',response.xpath(u'(//*[@id="callmeBtn"]//div[@title])[2]/@title').extract_first(default=u'待定')))
        item['developer'] = response.xpath(u"//div[@class='info wm']/ul/li[3]/text()").extract_first(default=u'未知').strip()
        item['property_manage_com'] = response.xpath(u"//li[contains(span,'物业公司')]/text()").extract_first(default=u'未知').strip()
        item['address'] = response.xpath(u'//*[@id="callmeBtn"]/ul/li[2]/span[2]/text()').extract_first(default=u'未知').strip()
        item['area_name'] = response.xpath("//span[@class='fl']/a[3]//text()").extract_first(default=u'未知').strip()
        item['city_name'] = response.xpath("//span[@class='fl']/a[1]//text()").extract_first(default=u'未知').replace(u'房产','').strip()
        item['cover_url'] = [response.xpath("//*[@id='con_tab1_con_3']/a/img/@lsrc").extract_first(),str(uuid.uuid4()).replace('-','')]
        item['household_size'] = response.xpath("//div[@class='info wm']/ul/li[5]/text()").extract_first(default=u'未知').replace(u'户','').strip()
        item['property_manage_fee'] = response.xpath("//div[@class='info wm']/ul/li[7]/text()").extract_first(default=u'未知').strip()
        item['construction_area'] = response.xpath("//div[@class='info wm']/ul/li[9]/text()").extract_first(default=u'未知').strip()
        item['property_type'] = response.xpath("//div[@class='info wm']/ul/li[6]/text()").extract_first(default=u'未知').strip()
        item['decoration'] = response.xpath("//div[@class='info wm']/ul/li[12]/text()").extract_first(default=u'未知').strip()
        item['per_square_price'] = response.xpath("//*[@id='callmeBtn']/ul/li[1]/em[1]/text()").extract_first(default=u'未知').strip()
        
        yield item
