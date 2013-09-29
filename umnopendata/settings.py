"""Development settings and globals"""

from os.path import join, abspath, dirname

# Scrapy settings for umnopendata project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

########## PATH CONFIGURATION

PROJECT_PATH = dirname(abspath(__file__))
ROOT_PATH = dirname(PROJECT_PATH)
TEST_PATH = join(PROJECT_PATH, 'tests')

########## END PATH CONFIGURATION

BOT_NAME = 'umnopendata'

SPIDER_MODULES = ['umnopendata.spiders']
NEWSPIDER_MODULE = 'umnopendata.spiders'

SPIDER_CONTRACTS = {
        'umnopendata.contracts.FormContract':10,
        'umnopendata.contracts.ClassContract':10,
        }

ITEM_PIPELINES = [
        'umnopendata.pipelines.ValidatorPipeline',
        'umnopendata.pipelines.DuplicatesPipeline',
        ]


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'umnopendata (+http://www.yourdomain.com)'
