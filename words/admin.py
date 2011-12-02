# -*- coding: utf-8 -*-
from django.contrib import admin


class LexicalEntryAdmin(admin.ModelAdmin):

    class Media:
        js = ("admin/js/categories.js", )

    readonly_fields = ('frequency', )
    exclude = ('user', 'frequency')
    search_fields = ('word', 'headword', 'user__name',
                     'description')
    list_display = ('word', 'headword', 'category', 'features',
                    'frequency', 'user', 'date')
    list_filter = ('user', 'date', 'category')
    date_hierarchy = 'date'
    # list_editable = ('headword', 'category', 'gender', 'number', 'person')
    save_as = False

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

    def features(self, obj, *args, **kwargs):
        return obj.get_features_display()
    features.allow_tags = True
