# -*- coding: utf-8 -*-
import json
import re

from django.db import transaction
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from words.models import LexicalEntry


class Command(BaseCommand):
    args = "prefix start end suffix"
    help = """
    Loads a lexicon file in JSON
    
    Usage:
    python manage.py loadlexicon /path/to/lexicon.json
    """
    can_import_settings = True

    def handle(self, *args, **options):
        if not args:
            raise CommandError("All the parameters must be provided.")
        file_name = args[0]
        try:
            file_descr = open(file_name, "r")
        except IOError, e:
            self.stdout.write("File not found: \"%s\"\n" % file_name)
        lines = []
        user = User.objects.get(username="admin")
        cont = 0
        with transaction.commit_on_success():
            for file_line in file_descr:
                line = json.loads(file_line)
                entry = LexicalEntry()
                entry.user = user
                entry.word = line["flexion"]
                entry.headword = line["lemma"]
                entry.category = line["category"].lower()
                for k, v in line["msd"].items():
                    if hasattr(entry, k) and v.strip():
                        try:
                            setattr(entry, k, v.strip())
                        except e:
                            print e, entry, line
                cont += 1
                if cont % 1000 == 0:
                    print u"... %s (%s) " % (cont, line["flexion"])
                entry.save()
