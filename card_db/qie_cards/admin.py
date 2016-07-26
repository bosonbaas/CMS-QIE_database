from django.contrib import admin
from .models import QieCard, Attempt, Tester, Test, Location, ReadoutModule

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


class ReadoutAdmin(admin.ModelAdmin):
    """ Provides the layout for ReadoutModule editing """
    
    fieldsets = [
        (None, {'fields': ['assembler', 'date', 'rm_number']}),
        ("Card Pack", {'fields':['card_pack_number',
                                 'card_1',
                                 'card_2',
                                 'card_3',
                                 'card_4',
                                 'mtp_optical_cable',
                                 'sipm_control_card',
                                ]}),
        ("LV Assembly", {'fields':[]}),
        ("Thermal Assembly", {'fields':[]}),
        ("SiPM Assembly", {'fields':['sipm_array_1',
                                     'sipm_array_2',
                                     'sipm_array_3',
                                     'sipm_array_4',
                                     'sipm_array_5',
                                     'mixed_sipm_array',
                                     'odu_type',
                                     'odu_number', 
                                    ]}),
        ("Jtag", {'fields':[]}),
        ("RM Outer Shell", {'fields':['minsk']}),
        ]
    
    list_display = ('rm_number',)
    ordering = ('rm_number',)
    searchfields = ('rm_number')



# Registration of the models
admin.site.register(QieCard, QieAdmin)
admin.site.register(Tester)
admin.site.register(Test, TestAdmin)
admin.site.register(ReadoutModule, ReadoutAdmin)
