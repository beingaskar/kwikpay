from django.contrib import admin


class NonEditableAdmin(admin.ModelAdmin):
    """ Model Admin extended to prevent creation, updation and deletion.
    """

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class NonEditableTabularInlineAdmin(admin.TabularInline):
    """ TabularInline Admin extended to prevent creation, updation and
    deletion.
    """

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
            return False

    def has_delete_permission(self, request, obj=None):
        return False


