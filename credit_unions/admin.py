from django.contrib import admin
from .models import CreditUnion
# Register your models here.
class CreditUnionAdmin(admin.ModelAdmin):
    # Fields to display in the main change list view
    list_display = ('name', 'contact_email', 'address')
    
    # Fields that can be used for searching
    search_fields = ('name', 'contact_email')
    
    # Fields to use for filtering in the sidebar
    list_filter = ('address',)

# If you don't need customization, you can use the simple registration:
admin.site.register(CreditUnion, CreditUnionAdmin)