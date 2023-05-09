import scrapy
from ccf_content_crawl.items import SrcItem
import re


class CCFContentSpider(scrapy.Spider):
    name = "ccf_content_crawl"
    except_list = [
        'https://www.ccf.org.cn/Academic_Evaluation/By_category/',
        'https://www.ccf.org.cn/ccftjgjxskwml/',
        'https://www.ccf.org.cn/Academic_Evaluation/Contact_Us/'
    ]

    def start_requests(self):
        yield scrapy.Request('https://www.ccf.org.cn/Academic_Evaluation/By_category/', callback=self.parse)

    def parse(self, response):
        entries = response.xpath("//div[@class='main m-b-md']//div[@class='snv']//ul[@style='float:right']/li/a")
        for entry in entries:
            url = response.urljoin(entry.xpath('./@href').extract_first())
            if url not in self.except_list:
                yield scrapy.Request(url, callback=self.parse_item)

    def parse_item(self, response):

        def generate_item(root, classes, types, level):
            entries = root.xpath("./li[position()>1]")
            item_list = []
            for entry in entries:
                item = SrcItem()
                item['src_abbr'] = entry.xpath("./div[2]/text()").extract_first()
                item['src'] = entry.xpath("./div[3]/text()").extract_first().replace('\n', ' ')
                item['publisher'] = entry.xpath("./div[4]/text()").extract_first()
                item['url'] = entry.xpath("./div[5]/a/@href").extract_first()
                item['classes'] = classes
                item['types'] = types
                item['level'] = level

                item['src_abbr'] = re.sub(r'[^\x00-\x7F\u4e00-\u9fa5]', '', item['src_abbr'])
                item['src'] = re.sub(r'[^\x00-\x7F\u4e00-\u9fa5]', '', item['src'])
                item['publisher'] = re.sub(r'[^\x00-\x7F\u4e00-\u9fa5]', '', item['publisher'])
                item['url'] = re.sub(r'[^\x00-\x7F\u4e00-\u9fa5]', '', item['url'])
                item['classes'] = re.sub(r'[^\x00-\x7F\u4e00-\u9fa5]', '', item['classes'])
                item['types'] = re.sub(r'[^\x00-\x7F\u4e00-\u9fa5]', '', item['types'])
                item['level'] = re.sub(r'[^\x00-\x7F\u4e00-\u9fa5]', '', item['level'])
                item_list.append(item)
            return item_list

        entry = response.xpath("//div[@class='m-text-mg']")
        classes = entry.xpath('./h4[2]/text()').extract_first().replace('●', '').replace('(', '').replace(')', '').strip()
        j_a, j_b, j_c = entry.xpath("./ul[1]"), entry.xpath("./ul[2]"), entry.xpath("./ul[3]")
        c_a, c_b, c_c = entry.xpath("./ul[4]"), entry.xpath("./ul[5]"), entry.xpath("./ul[6]")

        for item in generate_item(j_a, classes, 'Journal', 'A'):
            yield item
        for item in generate_item(j_b, classes, 'Journal', 'B'):
            yield item
        for item in generate_item(j_c, classes, 'Journal', 'C'):
            yield item
        for item in generate_item(c_a, classes, 'Conference', 'A'):
            yield item
        for item in generate_item(c_b, classes, 'Conference', 'B'):
            yield item
        for item in generate_item(c_c, classes, 'Conference', 'C'):
            yield item
