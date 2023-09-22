from django.contrib import admin
from django.contrib.auth.admin import UserAdmin  as BaseUserAdmin
from apis.models import NewUser



class UserAdminModal(BaseUserAdmin):

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdminModal
    # that reference specific fields on auth.User.
    list_display = ('id', 'email',  'fname' ,'lname','tc','mobileNumber', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        ('User credentional', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('fname','mobileNumber','lname','tc',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdminModal
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'fname','lname','mobileNumber', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email','id',)
    filter_horizontal = ()

# Register your models here.
# Now register the new UserAdminModal...
admin.site.register(NewUser, UserAdminModal)