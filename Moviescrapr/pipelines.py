# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

class GoojaraPipeline:
    def process_item(self, item,spider):
        # Process the item as needed
        for key, value in item.items():
            if isinstance(value, str):
                item[key] = value.strip().replace('\n', ' ')
        return item
    
