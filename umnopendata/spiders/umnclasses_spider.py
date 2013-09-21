from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request, FormRequest

from umnopendata.items import ClassItem, DepartmentItem
from umnopendata.utils import parse_class_description

from itertools import product
import re

class UMNClassesSpider(BaseSpider):
    """
    Spider that scrapes the UMN classes...
    """

    name = "umnclasses"
    allowed_domains = ['onestop.umn.edu', 'onestop2.umn.edu']
    start_urls = ['http://onestop2.umn.edu/courseinfo/\
classschedule_selectsubject.jsp?campus=UMNTC']

    def make_requests_from_url(self, url):
        """
        Overrides the default class method.

        ##### contracts #####
        ##### end contracts #####

        """
        return Request(url=url, callback=self.parse_schedule_form_options)


    def parse_schedule_form_options(self, response):
        """
        Returns a generator of FormRequest objects each containing formdata
        representing a search for a particular term and subject.

        ##### contracts #####
        ##### end contracts #####
        """

        hxs = HtmlXPathSelector(response)
        # selects all term option values, e.g. Fall 2013
        term_options = hxs.select('//select[@name="searchTerm"]/option/@value').extract()
        # selects all search subject option values, e.g. ACCT
        subject_options = hxs.select('//select[@name="searchSubject"]/option/@value').extract()

        for t in term_options:
            for s in subject_options:
                form_request = FormRequest.from_response(response,
                        formdata={'searchTerm':t, 'searchSubject':s},
                        formname='submitScheduleRequestForm',
                        callback=self.parse_class_schedule)
                # add term and subject meta data
                form_request.meta['term'] = t
                form_request.meta['subject'] = s
                yield form_request

    def parse_class_schedule(self, response):

        #for debugging
        from scrapy.shell import inspect_response
        inspect_response(response)

        # parse term and subject from response meta data

        # classes will be a list of dicts representing all the class fields
        # populated in the for loop below
        classes = []
        class_blocks = hxs.select('//div[contains(@class, "CourseBlock")]')

        #subject xpath from root: '//div[@id="subjetTitle"]/h1/text()'
        #term xpath from root:'//div[@class="pageSubTitle"]/text()'

        for block in class_blocks:
            class_id = block.select('./h3/a/@name').extract()
            # class_name =
            class_table_rows  = block.select('.//table[@class="sectionTable"]//tr')
            #class_table_rows = class_table.select('.//tr')
            for lec in class_table_rows:

                #select the class description, parse it to turn it into a dict
                class_dict = {}

                class_desc = lec.select('./td[@class="description"]/text()').extract()

                #replace with item loader
                class_desc = parse_class_description(class_desc)
                class_dict.update(class_desc)

                #classNumber = a list of class registration numbers
                class_number = lec.select('./td[@class="classNumber"]/text()').extract()

                #list of class instructors
                class_instrs = lec.select(
                        './td[@class="description"]//a[contains(@href, "www.umn.edu/lookup")]/text()'
                        ).extract()

                # list  of class modes (i.e. online, classroom) needs cleaning up
                class_mode = lec.select(
                        './td[@class="description"]/strong[contains(., "instruction mode")]/text()').extract()

                # list of class locations, needs cleaning up
                class_loc = lec.select(
                        './td[@class="description"]/a[contains(@onclick, "onestop.umn.edu/Maps")]/text()').extract()

            #yield class item here








