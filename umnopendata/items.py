# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ClassItem(Item):

    term = Field()
    subject = Field()
    name = Field()
    number = Field()
    classes = Field()

    # The classes field contains a list of dicts representing
    # the actual lectures and discussions for the class. Each
    # class may have all or some of the following fields.
    #
    # section_number
    # start_time
    # end_time
    # days
    # credits
    # instructors
    # class_number
    # mode
    # location
    #


class DepartmentItem(Item):
    pass
