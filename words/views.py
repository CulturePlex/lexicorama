# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from words.forms import SearchForm
from words.models import LexicalEntry

def search(request):
    search_form = SearchForm(label_suffix="", data=request.GET.copy())
    q = None
    entries = []
    if search_form.is_valid():
        q = search_form.cleaned_data["q"]
        if q:
            entries = LexicalEntry.objects.filter(word__iregex=q)
    return render_to_response('search.html',
                              {"search_form": search_form,
                               "entries": entries,
                               "q": q},
                              context_instance=RequestContext(request))
