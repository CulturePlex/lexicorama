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


class SearchOptionsForm(forms.Form):
    in_lemma = forms.BooleanField(label=_("In Lemma"), required=False)
    MATCH_CHOICES = (
        ("iexact", _("Exactly the Word")),
        ("regexp", _("A Regular Expression")),
        ("icontains", _("Contained Word")),
    )
    match = forms.ChoiceField(label=_("Matching"), required=False,
                              choices=MATCH_CHOICES)


class LexicalEntryForm(forms.ModelForm):

    class Media:
        js = (
            "admin/js/categories.js",
            "js/chosen.jquery.min.js",
            "js/words.js",
        )
        css = {
            "all": ("css/chosen.css", ),
        }

    class Meta:
        model = LexicalEntry
        exclude = ("word", "frequency", "lemma", "definition", "user", "eagle")
        widgets = {"category": forms.Select(attrs={"class": "category"})}
        for field in LexicalEntry.CATEGORY_FIELDS.values():
            for value in field:
                widgets[value] = forms.RadioSelect(attrs={"class": "facet"})

    def __init__(self, *args, **kwargs):
        super(LexicalEntryForm, self).__init__(*args, **kwargs)
        for field_name, field_value in self.fields.items():
            if field_name != "category":
                # field_value.choices[0] = ("", "None")
                field_value.choices = field_value.choices[1:]
            else:
                field_value.required = False

    def get_data(self):
        cleaned_data = self.cleaned_data
        if "category" in cleaned_data:
            if cleaned_data["category"]:
                data = {"category": cleaned_data["category"]}
            else:
                data = {}
            if cleaned_data["category"] in LexicalEntry.CATEGORY_FIELDS:
                for field in LexicalEntry.CATEGORY_FIELDS[cleaned_data["category"]]:
                    if field in cleaned_data and cleaned_data[field]:
                        data[field] = cleaned_data[field]
            return data
        else:
            return cleaned_data
