from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import (
        Compose, MapCompose, Join, TakeFirst, Identity
        )
from umnopendata.items import ClassItem
from umnopendata.utils import process_mode, process_location

import re

#items loaders

class ClassLoader(XPathItemLoader):
    """
    Loader for the ClassItem item
    """

    default_output_processor = Identity()
    term_in = MapCompose(lambda x: x.lower(), lambda x: x.split(),)
    term_out = Join('_')
    subject_in = MapCompose(lambda x: x.strip(),lambda x: x.split(' - '),)
    # class name e.g. Intro to Algorithms
    name_in = MapCompose(lambda x: x.split(u'\xa0')[2],)
    name_out = Join()
    # class number e.g. 4041 in CSCI 4041
    number_in = MapCompose(lambda x: x.split(u'\xa0')[1],)
    number_out = Join()
    classid_in = MapCompose(lambda x: x.lower(),lambda x: x.replace(' ', ''))
    classid_out = Join('')


class LectureLoader(XPathItemLoader):
    """
    Loader for the LectureItem item
    """
    # would be more concise to define Join as default
    default_output_processor = Join('')
    # can add loaders for everything captured
    # in the description parsing method
    sectionnumber_in = TakeFirst()
    class_type_in = TakeFirst()
    credits_in = TakeFirst()
    days_in = TakeFirst()
    classnum_in = TakeFirst()
    start_time_in_= TakeFirst()
    end_time_in = TakeFirst()
    instructors_in = Identity()
    # remove duplicate instructors
    instructors_out = Compose(lambda x: list(set(x)))
    mode_in = MapCompose(process_mode)
    location_in = MapCompose(process_location,lambda x: x.strip(),)
    # remove duplicate locations
    location_out = Compose(lambda x: list(set(x)))


