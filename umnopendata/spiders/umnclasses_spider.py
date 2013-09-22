from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request, FormRequest

from umnopendata.items import ClassItem
from umnopendata.utils import parse_class_description, ProcessClasses
from umnopendata.loaders import ClassLoader
from umnopendata.contracts import FormContract, ClassContract

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

        ##### CONTRACTS #####

        #@url
        #@returns items 0 0
        #@returns requests 1 10
        # response checks
        #@correct_form
        # end response checks

        ##### END CONTRACTS #####

        """
        return Request(url=url, callback=self.parse_schedule_form_options)


    def parse_schedule_form_options(self, response):
        """
        Returns a generator of FormRequest objects each containing formdata
        representing a search for a particular term and subject.

        ##### contracts #####
        @url http://onestop2.umn.edu/courseinfo/classschedule_selectsubject.jsp?campus=UMNTC
        @returns requests 10
        @correct_form
        ##### end contracts #####
        """

        hxs = HtmlXPathSelector(response)
        # selects all term option values, e.g. Fall 2013
        term_options = hxs.select(
                '//select[@name="searchTerm"]/option/@value'
                ).extract()
        # selects all search subject option values, e.g. ACCT
        subject_options = hxs.select(
                '//select[@name="searchSubject"]/option/@value'
                ).extract()

        for t in term_options:
            for s in subject_options:
                form_request = FormRequest.from_response(
                        response,
                        formdata={'searchTerm':t, 'searchSubject':s},
                        formname='submitScheduleRequestForm',
                        callback=self.parse_class_schedule,
                        )
                yield form_request

    def parse_class_schedule(self, response):
        """
        @url http://onestop2.umn.edu/courseinfo/viewClassScheduleTermAndSubject.do?campus=UMNTC&searchTerm=UMNTC%2C1139%2CFall%2C2013%2Cfalse&searchSubject=AHS%7CAcademic+Health+Center+Shared+-+AHS&searchFullYearEnrollmentOnly=false&Submit=View
        @returns items 1
        @class_contract
        """

        # for debugging
        from scrapy.shell import inspect_response
        inspect_response(response)
        # end debugging

        hxs = HtmlXPathSelector(response)
        loader = ClassLoader(item=ClassItem(), response=response)
        loader.add_xpath('subject', '//div[@id="subjetTitle"]/h1/text()')
        loader.add_xpath('term', '//div[@class="pageSubTitle"]/text()')

        class_blocks = hxs.select('//div[contains(@class, "CourseBlock")]')

        for block in class_blocks:

            # change the loaders xpath to the current block
            loader.selector = block
            loader.add_xpath('name', './h3[a/@name]/text()')
            loader.add_xpath('number', './h3[a/@name]/text()')


            classes = []
            class_table_rows  = block.select(
                    './/table[@class="sectionTable"]//tr'
                    )
            for lec in class_table_rows:

                class_dict = {}

                # parse the class description, see utils.parse_class_description
                class_desc = lec.select(
                        './td[@class="description"]/text()'
                        ).extract()
                class_desc = parse_class_description(class_desc)
                class_dict.update(class_desc)

                #classNumber = a list of class registration numbers
                class_number = lec.select(
                        './td[@class="classNumber"]/text()'
                        ).extract()
                class_dict.update(class_number=class_number)

                #list of class instructors
                class_instrs = lec.select(
                        './td[@class="description"]//a[contains(@href, "www.umn.edu/lookup")]/text()'
                        ).extract()
                class_dict.update(instructors=class_instrs)

                # list  of class modes (i.e. online, classroom) needs cleaning up
                class_mode = lec.select(
                        './td[@class="description"]/strong[contains(., "instruction mode")]/text()'
                        ).extract()
                class_dict.update(mode=class_mode)

                # list of class locations, needs cleaning up
                class_loc = lec.select(
                        './td[@class="description"]/a[contains(@onclick, "onestop.umn.edu/Maps")]/text()'
                        ).extract()
                class_dict.update(location=class_loc)

                loader.add_value('classes', class_dict)
                # append class_dict to classes list

            loader.add_value('classes', classes, ProcessClasses)
            return loader.load_item()

            #yield class item here



