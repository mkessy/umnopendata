# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class ValidatorPipeline(object):
    """
    Validate Class item fields.
    """

    def process_item(self, item, spider):
        return item

class DuplicatesPipeline(object):
    """
    Remove duplicates
    """

    def process_item(self, item, spider):
        return item

class ItemToModelPipeline(object):
    """
    Serialize Class items into Django models
    """

    def process_item(self, item, spider):
        return item
