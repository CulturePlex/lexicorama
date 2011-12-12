# -*- coding: utf-8 -*-
from urllib import urlencode

from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db import connection, DatabaseError
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from words.forms import SearchForm, SearchOptionsForm, LexicalEntryForm
from words.models import LexicalEntry

def search(request):
    data = request.GET.copy()
    search_form = SearchForm(label_suffix="", data=data)
    search_options_form = SearchOptionsForm(data=data)
    entry_form = LexicalEntryForm()
    q = None
    entries = []
    query_time = 0.0
    start_list = 1
    regexp_error = False
    if data:
        entry_form = LexicalEntryForm(data=data)
        if (search_form.is_valid() and search_options_form.is_valid()
            and entry_form.is_valid()):
            q = search_form.cleaned_data["q"]
            options = search_options_form.cleaned_data
            params = entry_form.get_data()
            if q:
                to_search = "word"
                if options["in_lemma"]:
                    to_search = "lemma"
                key = "%s__%s" % (to_search, options.get("match") or "iexact")
                params[key] = q
                entry_list = LexicalEntry.objects.filter(**params)
                # Grouping by not documented API
                # entry_list.query.group_by = ['lemma']
                paginator = Paginator(entry_list, 15)
                # Make sure page request is an int. If not, deliver first page.
                try:
                    page = int(request.GET.get('page', '1'))
                except ValueError:
                    page = 1
                # If page request (9999) is out of range, deliver last page of results.
                try:
                    entries = paginator.page(page)
                except (EmptyPage, InvalidPage):
                    entries = paginator.page(paginator.num_pages)
                except DatabaseError:
                    entry_list = LexicalEntry.objects.none()
                    paginator = Paginator(entry_list, 15)
                    entries = paginator.page(1)
                    regexp_error = True
                if connection.queries:
                    query_time = connection.queries[-1]["time"]
                start_list = ((entries.number - 1) * entries.paginator.per_page) + 1
    data.pop("page", None)
    url_path = urlencode(data)
    return render_to_response('search.html',
                              {"search_form": search_form,
                               "search_options_form": search_options_form,
                               "entry_form": entry_form,
                               "entries": entries,
                               "query_time": query_time,
                               "start_list": start_list,
                               "url_path": url_path,
                               "regexp_error": regexp_error,
                               "q": q},
                              context_instance=RequestContext(request))
