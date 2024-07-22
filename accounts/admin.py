from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustumUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustumUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser 

    # Django Course Stracture
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('age', )}),
    )

    # default stracture... you can type fieldsets and get the stracture recommned. 
    # fieldsets = UserAdmin.fieldsets + (
    #     (None, {
    #         'fields': (
    #             'age',
    #         ),
    #     }),
    # )


    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('age', )}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

