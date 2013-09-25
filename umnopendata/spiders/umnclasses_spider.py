from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request, FormRequest

from umnopendata.items import ClassItem, LectureItem
from umnopendata.utils import parse_class_description
from umnopendata.loaders import ClassLoader, LectureLoader
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

        # debugging
        #from scrapy.shell import inspect_response
        #inspect_response(response)
        # end debugging

        # instantiate xpath selector and item loaders
        hxs = HtmlXPathSelector(response)

        class_blocks = hxs.select(
                '//div[contains(@class, "CourseBlock")]'
                )

        subject_xpath = '//div[@id="subjetTitle"]/h1/text()'
        term_xpath = '//div[@class="pageSubTitle"]/text()'

        for block in class_blocks:

            class_loader = ClassLoader(item=ClassItem(), response=response)
            # the term is the first part of a class_id
            class_loader.add_xpath(
                    'classid',
                    term_xpath,
                    # processor
                    )

            class_loader.add_xpath('term', term_xpath)
            class_loader.add_xpath('subject', subject_xpath)

            # change the loaders xpath to the current block
            class_loader.selector = block
            class_loader.add_xpath('name', './h3[a/@name]/text()')
            class_loader.add_xpath('number', './h3[a/@name]/text()')
            # the class id is the second part of a class_id
            class_loader.add_xpath('classid', './h3/a[@name]/@name')

            classes = []
            class_table_rows  = block.select(
                    './/table[@class="sectionTable"]//tr'
                    )
            for lec in class_table_rows:

                lecture_loader = LectureLoader(item=LectureItem(), response=response)
                lecture_loader.selector = lec

                # parse the class description, see utils.parse_class_description
                class_desc = lec.select(
                        './td[@class="description"]/text()'
                        ).extract()
                class_desc = parse_class_description(class_desc)

                lecture_loader.add_value(None, class_desc)

                # classNum = a list of class registration numbers
                lecture_loader.add_xpath(
                        'classnum',
                        './td[@class="classNumber"]/text()'
                        )

                #list of class instructors
                lecture_loader.add_xpath(
                        'instructors',
                        './td[@class="description"]//a[contains(@href, "www.umn.edu/lookup")]/text()'
                        )

                # list  of class modes (i.e. online, classroom) needs cleaning up
                lecture_loader.add_xpath(
                        'mode',
                        './td[@class="description"]/strong[contains(., "instruction mode")]/text()'
                        )

                # list of class locations, needs cleaning up
                lecture_loader.add_xpath(
                        'location',
                        './td[@class="description"]/a[contains(@onclick, "onestop.umn.edu/Maps")]/text()'
                        )

                class_loader.add_value('classes', lecture_loader.load_item())

            yield class_loader.load_item()

            # set the lecture items' _class field with the class_id
            # created by the class item


