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
    class_sec_re = re.compile(r'-?\*?(?P<section>([0-9]{3}|[A-Z][0-9]{2})) (?P<class_type>[A-Z]{3})')

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

    mode = mode_re.search(mode.replace(u'\xa0', u' '))
    if mode is not None:
        return mode.groupdict()['mode']
    return None

def process_location(location):
    location = re.sub(
            r'\s+', ' ', location.replace(u'\xa0', u' ')
            )
    return location


