from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import (
        MapCompose, Join, TakeFirst, Identity
        )

from umnopendata.items import ClassItem
from umnopendata.utils import ProcessClasses

import re

#items loaders

class ClassLoader(XPathItemLoader):
    """
    Loader for the ClassItem item
    """

    default_output_processor = Identity()

    term_in = MapCompose(
            lambda x: x.lower(),
            lambda x: x.split(),
            )
    term_out = Join('_')

    subject_in = MapCompose(
            lambda x: x.strip(),
            lambda x: x.split(' - '),
            )

    # class name e.g. Intro to Algorithms
    name_in = MapCompose(
            lambda x: x.split(u'\xa0')[2],
            )
    name_out = Join()

    # class number e.g. 4041 in CSCI 4041
    number_in = MapCompose(
            lambda x: x.split(u'\xa0')[1],
            )
    number_out = Join()

    class_id_in = Join()

    #classes_in = MapCompose(ProcessClasses)

class LectureLoader(XPathItemLoader):
    """
    Loader for the LectureItem item
    """

    default_output_processor = Identity()

    # move to utils?
    def process_mode(mode):
        mode_re = re.compile(
                'instruction mode: (?P<mode>([\w-]+(\s[\w-]+)*)/?([\w-]+(\s[\w-]+)*))'
                )
        mode = mode_re.search(mode)
        if mode:
            mode = mode.groupdict()['mode']
        return mode

    # move to utils?
    def process_location(location):
        location = re.sub(
                r'\s+', ' ', location.replace(u'\xa0', u' ')
                )
        return location

#    _class = Field()
#    section_number = Field()
#    start_time = Field()
#    end_time = Field()
#    days = Field()
#    credits = Field()
#    instructors = Field()
#    class_number = Field()
#    mode = Field()
#    location = Field()

    # can add loaders for everything captured
    # in the description parsing method

    classnum_in = TakeFirst()
    instructors_in = Identity()
    mode_in = MapCompose(process_mode)
    location_in = MapCompose(process_location)










