from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, CalculatorAccessRole
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name', 'phone_number','verified', 'is_staff')
    list_filter = ('email', 'phone_number', 'is_staff', 'is_restricted', 'first_name')
    readonly_fields = ('date_joined', 'last_login',)
    fieldsets = (
                 (None, {'fields':('email', 'password')}),
                 ('Personal info', {'fields': ('first_name', 'last_name','phone_number', 'verified',)}),
                 ('Account Activity', {'fields': ('date_joined', 'last_login')}),
                 ('Permissions', {'fields':('is_staff', 'is_active', 'is_restricted', 'calc_access')}))

    add_fieldsets = (
            (
            None, {
            'classes':('wide',), 
            'fields':('email', 'password1', 'password2', 'is_staff', 'is_active', 'calc_access')
            }),
            (
            'Personal Information', {
            'classes':('wide',), 
            'fields':('phone_number', 'first_name', 'last_name')
            }),
        )

    search_fields = ('email', 'first_name', 'last_name', 'phone_number', 'calc_access')

    ordering = ('date_joined',)

@admin.register(CalculatorAccessRole)
class CalculatorAccessRoleAdmin(admin.ModelAdmin):
    list_display = ('role_name', 'created_at', 'walls', 'windows', 'roof', 'occupants', 'equipments', 'no_of_user')
    search_fields = ('role_name',)
    readonly_fields = ('created_at',)

    
    def no_of_user(self, rolename):
        result = CustomUser.objects.filter(calc_access__role_name = rolename).count()
        return result
   


admin.site.register(CustomUser, CustomUserAdmin)

# admin.site.register(CalculatorAccessRole, CalculatorAccessRoleAdmin)

admin.site.site_title = "CHG site admin (DEV)"
admin.site.site_header = "CHG administration"
admin.site.index_title = "Site administration"