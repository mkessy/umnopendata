
from ..spiders.umnclasses_spider import UMNClassesSpider
from .test_utils import generate_responses

import unittest
from pprint import pprint

class TestSpider(unittest.TestCase):

    def setUp(self):
        # set up the spider
        self.spider = UMNClassesSpider()

    def test_parse(self):
        responses = generate_responses()
        # choose the correct response for the tests you made in
        # in _test_items
        response = responses['AHS.html']
        items = list(self.spider.parse_class_schedule(response))
        self._test_fields_exist(items)
        self._test_items(items)

    def _test_fields_exist(self, items):
        """
        Test that all required fields are present
        """
        for item in items:
            self.assertIsNotNone(item['term'])
            self.assertIsNotNone(item['classid'])
            self.assertIsNotNone(item['subject'])
            self.assertIsNotNone(item['name'])
            self.assertIsNotNone(item['number'])


    # this whole way of testing is really bad style and needs to be
    # refactored
    def _test_items(self, items):
        # tests that the correct items are returned
        # in the correct format

        #term = Field()
        #classid = Field() # unique for each class
        #subject = Field()
        #name = Field()
        #number = Field()
        #classes = Field(
            #sectionnumber = Field()
            #start_time = Field()
            #class_type = Field()
            #end_time = Field()
            #days = Field()
            #credits = Field()
            #instructors = Field()
            #classnum = Field(
            #        input_processor=TakeFirst(),
            #        )
            #mode = Field()
            #location = Field()

        # assertIsNotNone, assertEqual, assertIsInstance, assertIn
        # items are what is expected

        item = items[0] # AHS 1101
        pprint(item, indent=2)

        # correctness of fields
        self.assertEqual(item['term'], u'fall_2013')
        self.assertEqual(item['classid'], 'fall2013ahs1101')
        self.assertEqual(item['name'], u'Orientation to Health Careers')
        self.assertEqual(item['number'], u'1101')
        self.assertEqual(len(item['classes']), 1)

        self.assertEqual(
                item['classes'][0]['sectionnumber'],
                u'001')
        self.assertEqual(
                item['classes'][0]['start_time'],
                u'03:35 P.M.'
                )
        self.assertEqual(
                item['classes'][0]['end_time'],
                u'04:25 P.M.'
                )
        self.assertEqual(
                item['classes'][0]['class_type'],
                u'LEC')

        self.assertEqual(
                item['classes'][0]['days'],
                u'M')

        self.assertEqual(
                item['classes'][0]['instructors'],
                [u'Simpson,Scott W', u'Rosand,Jennifer A']
                )
        self.assertEqual(
                item['classes'][0]['classnum'],
                u'22575'
                )
        self.assertEqual(
                item['classes'][0]['mode'],
                u'Classroom/Onsite')

        self.assertEqual(
                item['classes'][0]['credits'],
                u'1')
           # add location test

        # tests for AHS 4300
        item = items[7]

        self.assertEqual(item['term'], u'fall_2013')
        self.assertEqual(item['classid'], 'fall2013ahs4300')
        self.assertEqual(item['name'], u'Directed Study')
        self.assertEqual(item['number'], u'4300')
        self.assertEqual(len(item['classes']), 2)

        self.assertEqual(
                item['classes'][0]['sectionnumber'],
                u'001')

        self.assertEqual(
                item['classes'][0]['class_type'],
                u'IND')

        self.assertEqual(
                item['classes'][0]['instructors'],
                [u'Todd,Tricia']
                )
        self.assertEqual(
                item['classes'][0]['classnum'],
                u'27238'
                )
        self.assertEqual(
                item['classes'][0]['mode'],
                u'Independent/Directed Study')

        self.assertEqual(
                item['classes'][0]['credits'],
                u'1 - 3')

if __name__ == '__main__':
    unittest.main()


