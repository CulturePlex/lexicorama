# -*- coding: utf-8 -*-
import json
import re

from optparse import make_option

from django.db import transaction
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError

from words.models import LexicalEntry


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--sintagma',
            action='store_true',
            dest='sintagma',
            default=False,
            help='Dumps the output according to Sintagma format.'),
    )
    args = "filename"
    help = "\tDumps the lexicon into a file or standard output."
    can_import_settings = True

    def handle(self, *args, **options):
        file_name = None
        file_descr = None
        if args:
            file_name = args[0]
            try:
                file_descr = open(file_name, "w")
            except IOError, e:
                self.stdout.write("Unable to create a file: \"%s\"\n" \
                                  % file_name)
        if file_descr:
            cont = 0
            for entry in LexicalEntry.objects.all():
                file_descr.write(u"%s\n" % json.dumps(self.print_entry(entry)))
                if cont % 1000 == 0:
                    self.stdout.write(u"...%s (%s)\n" % (cont, entry.word))
                cont += 1
        else:
            for entry in LexicalEntry.objects.all():
                self.stdout.write(u"%s\n" % json.dumps(self.print_entry(entry)))

    def print_entry(self, entry):
        dic = {
            "category": entry.category,
            "lemma": entry.lemma,
            "flexion": entry.word,
            "eagle": entry.eagle,
            "frequency": entry.frequency,
            "msd": entry.get_features(),
        }
        return dic

