# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from items import ClassItem, LectureItem
from datetime import datetime

class ValidatorPipeline(object):
    """
    Validate Class item fields.
    """

    def process_item(self, item, spider):
        # will raise key error if item field isn't present since
        # none values aren't passed as valid params, catch
        # the key error and raise DropItem
        if isinstance(item, ClassItem):
            try:
                if not item['term']:
                    raise DropItem("Missing term in %s " % item)
                if not item['classid']:
                    raise DropItem("Missing classid in %s " % item)
                if not item['subject']:
                    raise DropItem("Missing subject in %s " % item)
                if not item['name']:
                    raise DropItem("Missing name in %s " % item)
                if not item['number']:
                    raise DropItem("Missing number in %s " % item)
            except KeyError as xcpt:
                raise DropItem("Required field missing: %s " % xcpt)

        # if isinstance(item, LectureItem):
        # validate item Lecture items
        return item

class DuplicatesPipeline(object):
    """
    Remove duplicates
    """
    def __init__(self):
        self.classes_seen = set()

    def process_item(self, item, spider):

        if item['classid'] in self.classes_seen:
            raise DropItem("Duplicate class found: %s" % item)
        else:
            self.classes_seen.add(item['classid'])
            return item

class ItemToModelPipeline(object):
    """
    Serialize Class and Lecture items into flask db models
    """
#    id = db.Column(db.String(64), primary_key=True, nullable=False)
#    term = db.Column(db.String(64))
#    subject = db.Column(db.String(600), index=True)
#    name = db.Column(db.String(600), index=True, nullable=False)
#    number = db.Column(db.String(120), index=True)
#    # backrefs cannot have same name as db tables
#    lectures = db.relationship('Lecture', backref='class', lazy='dynamic')
#    last_updated = db.Column(db.DateTime)

    def __init__(self):

        from app.classes.models import Uclass, Lecture
        from app import db

        self._class = Uclass
        self.lecture = Lecture
        self.db = db

    def process_item(self, item, spider):

        if isinstance(item, ClassItem):
            UclassModel = Uclass()
            UclassModel.id = item.classid
            UclassModel.subject = item.subject
            UclassModel.name = item.name
            UclassModel.number = item.number
            UclassModel.last_updated = datetime.utcnow()


















