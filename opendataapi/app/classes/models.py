from app import db

class Uclass(db.Model):
    #id = classid froms scrapy items
    id = db.Column(db.String(64), primary_key=True, nullable=False)
    term = db.Column(db.String(64))
    subject = db.Column(db.String(600), index=True)
    name = db.Column(db.String(600), index=True, nullable=False)
    number = db.Column(db.String(120), index=True)
    # backrefs cannot have same name as db tables
    lectures = db.relationship('Lecture', backref='class', lazy='dynamic')
    last_updated = db.Column(db.DateTime)

    def __repr__(self):
        return '<Uclass %r>' % (self.name)

class Lecture(db.Model):
    # insert database rows here
    # how to implement pk?
    #id = db.Column
    uclass = db.Column(
            db.String(64),
            db.ForeignKey('uclass.id'),
            primary_key=True,
            nullable=False,
            )
    sec_num = db.Column(db.String(64), primary_key=True, nullable=False)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    days = db.Column(db.String(64))
    credits = db.Column(db.String(64))
    class_type = db.Column(db.String(64))
    classnum = db.Column(db.String(64), index=True)
    mode = db.Column(db.String(600), index=True)
    instructors = db.Column(db.String(600), index=True)
    location = db.Column(db.String(120))
    last_updated = db.Column(db.DateTime)

    def __repr__(self):
        return '<lecture %r %r>' % (self.sec_num, self.class_type)


