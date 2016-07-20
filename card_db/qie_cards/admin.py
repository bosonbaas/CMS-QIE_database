from django.contrib import admin
from .models import QieCard, Attempt, Tester, Test, Location

# This file describes the layout of the admin pages.


class AttemptInLine(admin.StackedInline):
    """ Provides the inline layout for Attempts """
    
    model = Attempt
    date_hierarchy = 'date_tested'
    ordering = ('test_type', 'attempt_number', 'date_tested')
    extra = 0


class LocationsInLine(admin.StackedInline):
    """ Provides the inline layout for Attempts """
    
    model = Location
    date_hierarchy = 'date_received'
    ordering = ('date_received',)
    extra = 0


class QieAdmin(admin.ModelAdmin):
    """ Provides the layour for QieCard editing """
    
    fieldsets = [
        ('QIE information', {'fields': ['barcode', 'uid', 'bridge_major_ver', 'bridge_minor_ver', 'bridge_other_ver', 'igloo_major_ver', 'igloo_minor_ver', 'comments']}),
    ]
    
    inlines = [AttemptInLine, LocationsInLine]
    list_display = ('barcode', 'uid',)
    ordering = ('barcode', 'uid',)
    searchfields = ('barcode')
    
    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('barcode', 'uid') + ('bridge_major_ver', 'bridge_minor_ver') +  ('bridge_other_ver', 'igloo_major_ver') + ('igloo_minor_ver', None)
        return self.readonly_fields


class TestAdmin(admin.ModelAdmin):
    """ Provides the layout for the Test editing """
    list_display = ('name', 'description',)
    ordering = ('name',)
    searchfields = ('name')
    
    fieldsets = [
        ('Test Information', {'fields': ['name', 'abbreviation', 'description', 'required']}),
    ]

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('abbreviation', 'required') 
        return self.readonly_fields

# Registration of the models
admin.site.register(QieCard, QieAdmin)
admin.site.register(Tester)
admin.site.register(Test, TestAdmin)
