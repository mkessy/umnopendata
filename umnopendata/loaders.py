from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import MapCompose, Join, TakeFirst

from umnopendata.items import ClassItem

#items loaders

class ClassLoader(XPathItemLoader):

    default_output_processor = TakeFirst()

    term_in = MapCompose(
            lambda x: x.lower(),
            lambda x: x.split(),
            )
    term_out = Join('_')

    subject_in = MapCompose(
            lambda x: x.strip(),
            lambda x: x.split(' - '),
            )

    classes_in = ProcessClasses

