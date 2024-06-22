import re

def validate_email(email):
    pattern1 = r'[\.\@\-]{2,}'
    isvalid = re.search(pattern1, email)

    if isvalid is not None:
        return False

    pattern2 = r'^[a-z][a-z\.\d]{1,}[a-z\d]\@(?:[a-z]|[a-z][a-z\d\-]{0,}[a-z\d]{1,})\.((?:[a-z]{2,}[\.\-]{0,1}[a-z]{2,}|[a-z]{2,}))$'
    isvalid = re.search(pattern2, email)

    if isvalid is None:
        return False

    return True
