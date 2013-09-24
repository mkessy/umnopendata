# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.contrib.loader.processor import (
        MapCompose, Join, TakeFirst, Identity
        )
from scrapy.item import Item, Field

class ClassItem(Item):
    """
    This item represents a class, e.g CSCI 4041

    """

    term = Field()
    classid = Field() # unique for each class
    subject = Field()
    name = Field()
    number = Field()
    classes = Field() # list of pks(database sense) for related LectureItems


class LectureItem(Item):
    """
    This item represents a lecture, recitation, lab etc tied to a
    particular class. For example, a LectureItem would represent recitation
    section 2 (DIS 002) for CSCI 4041, which would be represented by a ClassItem
    """

    sectionnumber = Field()
    start_time = Field()
    class_type = Field()
    end_time = Field()
    days = Field()
    credits = Field()
    instructors = Field()
    classnum = Field()
    mode = Field()
    location = Field()





