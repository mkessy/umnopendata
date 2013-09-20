from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request, FormRequest

from umnopendata.items import ClassItem, DepartmentItem

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
        ##### contracts #####
        ##### end contracts #####

        """
        return Request(url=url, callback=self.parse_schedule_form_options)

    def parse_class_description(desc):
        """
        Parse a course description returning the following class parameters
        in dictionary format.
        """

        class_time_re = re.compile(
                r'(?P<times>0([1-9]|1[0-2]):[0-5][0-9] (P\.M\.|A\.M\.) - 0([1-9]|1[0-2]):[0-5][0-9] (P\.M\.|A\.M\.)) , (?P<days>([MWF]|Tu|Th)(,([MWF]|Tu|Th)+)*)'
        )

        class_sec_re = re.compile(r'-(?P<section>[0-9]{3}) (?P<class_type>[A-Z]{3})')
        class_credits_re = re.compile(r'(?P<credits>)([1-9] - )?[1-9]) credits? )')

        cleaned_desc = []
        for line in desc:
            cleaned_desc.append(
                    re.sub(r'\s+', ' ', line.replace(u'\xa0', u' '))
                    )
        cleaned_desc = ''.join(cleaned_desc)
        # now that the description is cleaned, we can do regex
        # matching for the desired fields

(?<=0([1-9]|1[0-2]):[0-5][0-9] (P\.M\.|A\.M\.) - 0([1-9]|1[0-2]):[0-5][0-9] (P\.M\.|A\.M\.) , )([MWF]|Tu|Th)(,([MWF]|Tu|Th)+)*
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
                # add term and subject meta data here
                yield form_request

    def parse_class_schedule(self, response):

        from scrapy.shell import inspect_response
        inspect_response(response)
        # select class subject+level hxs.select('//h3/a/@name').extract()
        # class_instrs = hxs.select('//td[@class="description"]/a[contains(@href,"www.umn.edu/lookup")]/text()').extract()

        class_blocks = hxs.select('//div[contains(@class, "CourseBlock")]')
        #iterate over the class blocks selecting instructor list for each class
            # class_instructors = class_block.select('.//td[@class="description"]/a[contains(@href, "www.umn.edu")]/text()').extract()
            # class_id = class_block.select('./h3/a/@name').extract()
            # grab the sectionTable

        for block in class_blocks:
            class_id = block.select('./h3/a/@name').extract()
            class_table_rows  = block.select('.//table[@class="sectionTable"]//tr')
            #class_table_rows = class_table.select('.//tr')
            for lec in class_table_rows:
                # get class no. , class description
                #classNumber = a list
                class_number = lec.select('./td[@class="classNumber"]/text()').extract()
                #list of class instructors
                class_instrs = lec.select(
                        './td[@class="description"]//a[contains(@href, "www.umn.edu/lookup")]/text()'
                        ).extract()

                pass

        pass



