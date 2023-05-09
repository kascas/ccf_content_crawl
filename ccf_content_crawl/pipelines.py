# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class CcfContentCrawlPipeline:
    def __init__(self) -> None:
        self.fc = open('./conference.csv', 'w', encoding='utf-8')
        self.fj = open('./journal.csv', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        types=item['types']
        if types=='Journal':
            self.fj.write('\t'.join([item['classes'], item['src_abbr'], item['src'], item['types'], item['level'], item['publisher'], item['url']]) + '\n')
        else:
            self.fc.write('\t'.join([item['classes'], item['src_abbr'], item['src'], item['types'], item['level'], item['publisher'], item['url']]) + '\n')
        return item

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.fc.close()
        self.fj.close()