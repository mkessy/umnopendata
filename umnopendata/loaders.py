from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import (
        MapCompose, Join, TakeFirst, Identity
        )

from umnopendata.items import ClassItem
from umnopendata.utils import ProcessClasses

#items loaders

class ClassLoader(XPathItemLoader):

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

    name_in = MapCompose(
            lambda x: x.split(u'\xa0')[2],
            )
    name_out = Join()

    number_in = MapCompose(
            lambda x: x.split(u'\xa0')[1],
            )
    number_out = Join()

    #classes_in = MapCompose(ProcessClasses)

