# -*- coding: utf-8 -*-
import json
import re

from optparse import make_option

from django.db import transaction
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError

from words.models import LexicalEntry


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--exceptions-file',
            type='string',
            dest='exceptions_file',
            default=None,
            help='File name for log wrods in CREA but not in the lexicon.'),
    )
    args = "crea_file"
    help = "\tLoads frequencies from a CREA file."
    can_import_settings = True

    def handle(self, *args, **options):
        if not args:
            raise CommandError("All the parameters must be provided.")
        file_name = args[0]
        file_descr = None
        try:
            file_descr = open(file_name, "r")
        except IOError, e:
            self.stdout.write("File not found: \"%s\"\n" % file_name)
        cont = 1
        entries = []
        excep_descr = None
        exceptions_file = options["exceptions_file"]
        if exceptions_file:
            try:
                excep_descr = open(exceptions_file, "w")
            except IOError:
                self.stdout.write("Unable to create a file: \"%s\"\n" \
                                  % exceptions_file)
        for file_line in file_descr:
            line = unicode(file_line.strip().decode("utf8"))
            pos, word, abs_freq, freq = line.split("\t")
            word = word.strip()
            freq = float(freq)
            entries.append((LexicalEntry.objects.filter(word=word), freq))
            if not entries and excep_descr:
                dic = {
                    "word": word,
                    "frequency": freq,
                }
                excep_descr.write(json.dumps(dic) + "\n")
            if cont % 1000 == 0:
                with transaction.commit_on_success():
                    for elements, frequency in entries:
                        elements.update(frequency=frequency)
                entries = []
                self.stdout.write(u"...%s (%s)\n" % (cont, word))
            cont += 1
        file_descr.close()
        excep_descr.close()
