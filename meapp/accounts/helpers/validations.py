from django.core.exceptions import ValidationError
from . import validators as v

class SignupDataValidation:
    def __init__(self, kwargs:dict):
        self.email = kwargs.get('email', '')
        self.phone_number = kwargs.get('phone_number', '')
        self.first_name = kwargs.get('first_name', '')
        self.last_name = kwargs.get('last_name', '')
        self.password = kwargs.get('password', '')
        self.repassword = kwargs.get('repassword', '')
        self.errors = []
        self.data = {}
        
    
    def run_validator(self, data:str, validator)->str:
        validated_data = data
        try:
            validated_data = validator(data)
        except ValidationError as e:
            self.errors.append(e)
        return validated_data

    def is_valid(self):
        all = self.email + self.phone_number + self.first_name + self.last_name + self.password + self.repassword 
        if len(all) == 0:
            self.errors.append("Please fill all the *required fields")
            return False

        self.data['email'] =  self.run_validator(data = self.email, validator = v.validate_email)
        self.data['phone_number'] =  self.run_validator(data = self.phone_number, validator = v.validate_phone_number)
        self.data['first_name'] =  self.run_validator(data = self.first_name, validator = v.validate_first_name)
        self.data['last_name'] =  self.run_validator(data = self.last_name, validator = v.validate_last_name)
        self.password =  self.run_validator(data = self.password, validator = v.validate_password)
        
        if self.password != self.repassword:
            self.errors.append('Confirm Password should be same as password')
            return False

        if len(self.errors):
            return False

        return True 
