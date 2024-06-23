from django.contrib import messages
from home import validators 

def signup_request_validation(request, **kwargs)->dict:
    first_name = request.POST.get('firstname', '').lower().strip()
    last_name = request.POST.get('lastname', '').lower().strip()
    email = request.POST.get('email', '').lower()
    password = request.POST.get('password', '').strip()
    repassword = request.POST.get('repassword', '').strip()

    flags:list[bool] = [True, True, True, True, True]
    result = {
              "isvalid" : True,
              "data":{
                      "email": email,
                      "password":  password,
                      "first_name": first_name,
                      "last_name": last_name,
            }
        }

    if email and password and first_name:
        if not validators.validate_first_name(first_name):
            flags[0] = False  
            messages.error(request, "First Name must be alphabetical and minimum of 3 character")

        if len(last_name):
            if not validators.validate_last_name(last_name):
                flags[1] = False  
                messages.error(request, "remove extra spaces or number from Last Name")

        if not validators.validate_email(email):
            flags[2] = False
            messages.error(request, "Invalid Email Address")

        if not validators.validate_password(password):
            flags[3] = False  
            messages.error(request, "Password length must be 8 to 30 long and contain alphanumeric (a-z, A-Z, 0-9) and @, !, $, %, ^, &, *, (, ), +, -, ?, /")

        if password != repassword:
            flags[4] = False  
            messages.error(request, "Confirm Password should be same as password")

    else:
        messages.error(request, "Please fill all the *required fields")

    if sum(flags) == 5:
        return result

    else:
        result['isvalid'] = False
        return result


