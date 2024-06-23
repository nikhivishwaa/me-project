from django.contrib.auth.models import User


def create_user(data, username):
    user = User.objects.create_user(username=username, email=data['email'])
    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.set_password(data['password'])
    user.save()
    print("User created", user)