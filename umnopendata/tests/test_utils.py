from os.path import join, basename
from glob import glob

from scrapy.http import TextResponse, Response, Request

from umnopendata.settings import TEST_PATH


# get file paths for all html files prefixed with test_
# these will serve as the source files for mock responses


def fake_response_from_file(file_name, url=None):
    """
    Creates a mock Scrapy HTTP response from a HTML file
    file_name: The abs path to the html file
    url: The URL of the response
    returns: A list of scrapy HTTP responses which can be used for
    unit testing.
    """

    if not url:
        url = 'http://www.example.com'

    req = Request(url=url)
    with open(file_name, 'r') as f:
        html_content = f.read()

    response = TextResponse(
            url=url,
            request=req,
            body=html_content,
            )
    #    response.encoding = 'utf-8'
    return response

test_htmls = glob(join(TEST_PATH, 'test_*.html'))

def generate_responses():
    """
    Returns an iterable of Scrapy responses base on the html test files
    found in the TEST_PATH
    """

    return {basename(f).split('_')[1]:fake_response_from_file(f)
            for f in test_htmls}


