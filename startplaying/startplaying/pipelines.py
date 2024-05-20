# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.exceptions import DropItem

class StartplayingPipeline:
    def process_item(self, item, spider):
        if not item.get('seats_left'):
            raise DropItem(f"Missing seats in {item}")
