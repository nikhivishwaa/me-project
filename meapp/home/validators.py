import re

def validate_email(email:str)->bool:
    pattern1 = r'[\.\@\-]{2,}'
    isvalid = re.search(pattern1, email)

    if isvalid is not None:
        return False

    pattern2 = r'^[a-z][a-z\.\d]{1,}[a-z\d]\@(?:[a-z]|[a-z][a-z\d\-]{0,}[a-z\d]{1,})\.((?:[a-z]{2,}[\.\-]{0,1}[a-z]{2,}|[a-z]{2,}))$'
    isvalid = re.search(pattern2, email)

    if isvalid is None:
        return False

    return True

def validate_password(password:str)->bool:
    pattern1 = r'^[a-zA-Z0-9\@\$\^\(\)\?\~\.\/]{8,30}$'
    isvalid = re.search(pattern1, password)

    if isvalid is None:
        return False

    pattern2 = r'[A-Z]+'
    pattern3 = r'[a-z]+'
    pattern4 = r'[0-9]+'
    pattern5 = r'[\@\$\^\(\)\?\~\.\/\&\*\+\-]+'

    if re.search(pattern2, password) is None:
        return False
    if re.search(pattern3, password) is None:
        return False
    if re.search(pattern4, password) is None:
        return False
    if re.search(pattern5, password) is None:
        return False

    return True

def validate_first_name(first_name:str)->bool:
    if first_name.isalpha() and len(first_name) >= 3:
        return True

    return False
def validate_last_name(last_name:str)->bool:
    if last_name.isalpha():
        return True
    
    pattern1 = r'\s{2,}'
    pattern2 = r'^[a-z\s]{3,}$'
    if re.search(pattern1, last_name) is None and re.search(pattern2, last_name) is not None:
        return True

    return False

