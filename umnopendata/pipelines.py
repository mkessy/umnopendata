# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class ValidatorPipeline(object):
    """
    Validate Class item fields.
    """

    def process_item(self, item, spider):

        # will raise key error if item field isn't present since
        # none values aren't passed as valid params, catch
        # the key error and raise DropItem

        if not item['term']:
            raise DropItem("Missing term in %s " % item)
        if not item['classid']:
            raise DropItem("Missing classid in %s " % item)
        if not item['subject']:
            raise DropItem("Missing subject in %s " % item)
        if not item['name']:
            raise DropItem("Missing name in %s " % item)
        if not item['number']:
            raise DropItem("Missing number in %s " % item)

        return item

class DuplicatesPipeline(object):
    """
    Remove duplicates
    """

    def __init__(self):
        self.classes_seen = set()

    def process_item(self, item, spider):
        if item['classid'] in self.classes_seen:
            raise DropItem("Duplicate found: %s" % item)
        else:
            self.classes_seen.add(item['classid'])
            return item

class ItemToModelPipeline(object):
    """
    Serialize Class and Lecture items into Django models
    """

    def process_item(self, item, spider):

        return item








