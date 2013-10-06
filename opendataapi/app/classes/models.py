from app import db

class Uclass(db.Model):
    #id = classid from scrapy item
    id = db.Column(db.String(64), primary_key = True)
    term = db.Column(db.String(64), index=True)
    subject = db.Column(db.String(120), index=True)
    name = db.Column(db.String(600), index=True)
    number = db.Column(db.String(120), index=True)
    lectures = db.relationship('Lecture', backref='uclass', lazy='dynamic')


class Lecture(db.Model):
    # insert database rows here
    pass

#class ClassItem(Item):
#    """
#    This item represents a class, e.g CSCI 4041
#    """
#
#    term = Field()
#    classid = Field() # unique for each class
#    subject = Field()
#    name = Field()
#    number = Field()
#    classes = Field() # list of pks(database sense) for related LectureItems
#
#
#class LectureItem(Item):
#    """
#    This item represents a lecture, recitation, lab etc tied to a
#    particular class. For example, a LectureItem would represent recitation
#    section 2 (DIS 002) for CSCI 4041, which would be represented by a ClassItem
#    """
#
#    sectionnumber = Field()
#    start_time = Field()
#    class_type = Field()
#    end_time = Field()
#    days = Field()
#    credits = Field()
#    instructors = Field()
#    classnum = Field()
#    mode = Field()
#    location = Field()
#
#
