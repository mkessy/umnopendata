import re

def parse_class_description(desc):
    """
    Parse a course description returning the following class parameters
    in dictionary format:

    start_time
    end_time
    days
    sectionnumber
    credits
    type (LEC, DIS, IND, etc.)

    """
    class_time_re = re.compile(
            r'(?P<times>0([1-9]|1[0-2]):[0-5][0-9] (P\.M\.|A\.M\.) - 0([1-9]|1[0-2]):[0-5][0-9] (P\.M\.|A\.M\.)) , (?P<days>([MWF]|Tu|Th)(,([MWF]|Tu|Th)+)*)'
            )
    class_sec_re = re.compile(r'-(?P<section>[0-9]{3}) (?P<class_type>[A-Z]{3})')
    class_credits_re = re.compile(r'(?P<credits>([1-9] - )?[1-9]) credits?')

    cleaned_desc = []
    for line in desc:
        cleaned_desc.append(
                re.sub(r'\s+', ' ', line.replace(u'\xa0', u' '))
                )
    cleaned_desc = ''.join(cleaned_desc)
    class_params = {}

    class_time = class_time_re.search(cleaned_desc)
    if class_time:
        class_time = class_time.groupdict()
        class_start_time, class_end_time = class_time['times'].split(' - ')
        class_days = class_time['days'].split(',')
        class_params.update(
                start_time=class_start_time,
                end_time=class_end_time,
                days=class_days
                )

    class_sec = class_sec_re.search(cleaned_desc)
    if class_sec:
        class_sec = class_sec.groupdict()
        class_params.update(
                class_type=class_sec['class_type'],
                sectionnumber=class_sec['section'],
                )

    class_credits = class_credits_re.search(cleaned_desc)
    if class_credits:
        class_credits = class_credits.groupdict()
        class_params.update(
                credits=class_credits['credits'],
                )

    return class_params

def process_mode(mode):

    mode_re = re.compile(
            'instruction mode: (?P<mode>([\w-]+(\s[\w-]+)*)/?([\w-]+(\s[\w-]+)*))'
            )

    mode = mode_re.search(mode)
    if mode:
        mode = mode.groupdict()['mode']
    return mode

# move to utils?
def process_location(location):
    location = re.sub(
            r'\s+', ' ', location.replace(u'\xa0', u' ')
            )
    return location


def ProcessClasses(classes):
    """
    Cleans up the fields in a class dictionary object.
    """

    mode_re = re.compile(
            'instruction mode: (?P<mode>([\w-]+(\s[\w-]+)*)/?([\w-]+(\s[\w-]+)*))'
            )
    print classes

    processed = []
    for _class in classes:
        for key, val in _class.items():

            if key=='class_number':
                if len(val)>0:
                    _class[key] = val[0]
            if key=='instructors':
                if len(val)>0:
                    _class[key] = val
            if key=='mode':
                if len(val)>0:
                    mode = mode_re.search(val[0])
                    if mode:
                        mode = mode.groupdict()['mode']
                        _class[key] = mode
            if key=='location':
                if len(val)>0:
                    location = location[0]
                    location = re.sub(
                            r'\s+', ' ', location.replace(u'\xa0', u' ')
                            )
                    _class[key] = location
            processed.append(_class)
    return processed

