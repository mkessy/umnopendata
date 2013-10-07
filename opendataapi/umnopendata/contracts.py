from scrapy.contracts import Contract
from scrapy.exceptions import ContractFail

#Contracts for umnclasses spider

class FormContract(Contract):
    """
    Contract to check the correct form fields are filled for the
    class schedule search.
    """

    name = 'correct_form'

    def pre_process(self, response):
        pass

    def post_process(self, output):
        pass

class ClassContract(Contract):
    """

    """

    name = 'class_contract'

    def pre_process(self, response):
        pass

    def post_process(self, output):
        ## can add tests/assertions here
        test_class = output[0]

#        {'classes': [{'class_number': [u'22575'],
#            'class_type': u'LEC',
#            'credits': u'1',
#            'days': [u'M'],
#            'end_time': u'04:25 P.M.',
#            'instructors': [u'Simpson,Scott W', u'Rosand,Jennifer A'],
#            'location': [u'MoosT\n                  \n                  \xa02-530\n                  \n                  ''],
#            'mode': [u'instruction mode:\xa0Classroom/Onsite'],
#            'section_number': u'001',
#            'start_time': u'03:35 P.M.'}],
#            'name': [u'S'],
#            'number': [u'H'],
#            'subject': [u'Academic Health Center Shared', u'AHS'],
#            'term': u'fall_2013'}
#
        # begin tests
        print test_class
        assert(test_class['name']==u'Orientation to Health Careers')
        assert(test_class['subject']==[u'Academic Health Center Shared', 'AHS'])
        assert(test_class['number']==u'1101')
        assert(test_class['term']==u'fall_2013')
        assert(test_class['classes'][0]['class_type']==u'LEC')
        assert(test_class['classes'][0]['credits']==u'1')
        assert(test_class['classes'][0]['days']==[u'M',])
        assert(test_class['classes'][0]['start_time']==u'03:35 P.M.')
        assert(test_class['classes'][0]['end_time']==u'04:25 P.M.')
        assert(test_class['classes'][0]['instructors']==[u'Simpson,Scott W', u'Rosand,Jennifer A'])
        assert(test_class['classes'][0]['section_number']==u'001')
        assert(test_class['classes'][0]['mode']==u'Classroom/Onsite')
        assert(test_class['classes'][0]['location']==u'MoosT 2-530')

