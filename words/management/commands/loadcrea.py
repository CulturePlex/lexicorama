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
    args = "crea_file"
    help = "\tLoads frequencies from a CREA file."
    can_import_settings = True

    def handle(self, *args, **options):
        if not args:
            raise CommandError("All the parameters must be provided.")
        file_name = args[0]
        try:
            file_descr = open(file_name, "r")
        except IOError, e:
            self.stdout.write("File not found: \"%s\"\n" % file_name)
        cont = 0
        with transaction.commit_on_success():
            for file_line in file_descr:
                line = unicode(file_line.strip().decode("utf8"))
                pos, word, abs_freq, freq = line.split("\t")
                word = word.strip()
                freq = float(freq)
                entries = LexicalEntry.objects.filter(word=word)
                entries.update(frequency=freq)
                #if not entries:
                #    dic = {
                #        "word": word,
                #        "frequency": freq,
                #    }
                #    self.stdout.write(json.dumps(dic) + "\n")
                if cont % 1000 == 0:
                    self.stdout.write(u"...%s (%s)\n" % (cont, word))
                cont += 1
            file_descr.close()
