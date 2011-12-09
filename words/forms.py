# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import gettext as _

from words.models import LexicalEntry


class SearchForm(forms.Form):
    q = forms.CharField(label=_("Word to search"), required=False,
                        max_length=100)

    def q_clean(self):
        q = super(SearchForm, self).q_clean()
        return q.strip()


class LexicalEntryForm(forms.ModelForm)

    class Meta:
        model = LexicalEntry
        exclude ("word", "frequency")
