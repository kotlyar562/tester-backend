from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from . forms import UserAdminCreationForm, UserAdminChangeForm
from . models import User


class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ('email', 'user_id', 'is_admin')
    list_filter = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('user_id', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active',)}),
    )
    readonly_fields = ('user_id',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
