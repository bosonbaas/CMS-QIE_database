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
    
    fiedsets = [
        ('QIE information', {'fields': ['card_id', 'uid', 'geo_loc', 'plane_loc', 'comments']}),
    ]
    
    inlines = [AttemptInLine, LocationsInLine]
    list_display = ('card_id', 'uid',)
    ordering = ('card_id', 'uid',)
    searchfields = ('card_id')


# Registration of the models
admin.site.register(QieCard, QieAdmin)
admin.site.register(Tester)
admin.site.register(Test)
