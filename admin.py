# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.sites.models import Site

from words.models import LexicalEntry
from words.admin import LexicalEntryAdmin


class AdminSite(admin.AdminSite):

    def has_permission(self, request):
        return request.user.is_superuser or request.user.is_staff


def setup_admin():
    admin_site.register(User, UserAdmin)
    admin_site.register(Group, admin.ModelAdmin)
    admin_site.register(Site, admin.ModelAdmin)

    admin_site.register(LexicalEntry, LexicalEntryAdmin)

admin_site = AdminSite(name=settings.PROJECT_NAME)
setup_admin()
