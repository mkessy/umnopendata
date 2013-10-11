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

                if len(item['classes']) != 0:
                    for lec in item['classes']:
                        if not lec.get('sectionnumber'):
                            raise DropItem(
                                    "Lecture missing section num in %s " % item
                                    )
                            print item

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

    def __init__(self):
        pass

        from app.classes.models import Uclass, Lecture
        from app import db
        self.Uclass = Uclass
        self.Lecture = Lecture
        self.db = db

    def process_item(self, item, spider):

        if isinstance(item, ClassItem):

            # check if class is already in db, if not create it
            uclass_model = self.Uclass.query.get(item['classid'])
            if not uclass_model:
                uclass_model = self.Uclass()
                uclass_model.id = item['classid']

            uclass_model.term = item.get( 'term' )
            uclass_model.subject = item.get( 'subject' )
            uclass_model.name = item.get( 'name' )
            uclass_model.number = item.get( 'number' )
            uclass_model.last_updated = datetime.utcnow()

            self.db.session.add(uclass_model)

            lectures = []
            if(len(item['classes']) != 0):
                # check if lecture is already in db, if not create it
                # note that lecture has a composite pk of its parent class
                # and section number
                for lec in item['classes']:
                    lecture_model = self.Lecture.query.get(
                            ident=(uclass_model.id,lec['sectionnumber'])
                            )
                    if not lecture_model:
                        lecture_model = self.Lecture()
                        lecture_model.uclass = uclass_model.id
                        lecture_model.sec_num = lec['sectionnumber']

                    lecture_model.class_type = lec.get( 'class_type' )
                    lecture_model.start_time = lec.get( 'start_time' )
                    lecture_model.end_time = lec.get( 'end_time' )
                    lecture_model.days = lec.get( 'days' )
                    lecture_model.instructors = lec.get( 'instructors' )
                    lecture_model.classnum = lec.get( 'classnum' )
                    lecture_model.location = lec.get( 'location' )
                    lecture_model.mode = lec.get('mode')
                    lecture_model.credits = lec.get('credits')
                    lecture_model.last_updated = datetime.utcnow()
                    lectures.append(lecture_model)
                self.db.session.add_all(lectures)
        self.db.session.commit()
        return item

