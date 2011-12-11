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
        make_option('--no-verbs',
            action='store_true',
            dest='no_verbs',
            default=False,
            help='Ignore any verb in the load processself.'),
        make_option('--only-verbs',
            action='store_true',
            dest='only_verbs',
            default=False,
            help='Loads only verbs.'),

    )
    args = "prefix start end suffix"
    help = "\tLoads a lexicon file in JSON."
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
        user = User.objects.all()[0]
        cont = 0
        join_args = " ".join(args[1:])
        with transaction.commit_on_success():
            for file_line in file_descr:
                line = json.loads(file_line)
                category = line["category"].lower()
                if ((options["only_verbs"] and category == "verb")
                    or (options["no_verbs"] and category != "verb")):
                    entry = LexicalEntry()
                    entry.user = user
                    entry.word = line["flexion"]
                    entry.lemma = line["lemma"]
                    entry.eagle = line.get("eagle_code", line.get("eagle", None))
                    entry.frequency = line.get("frequency", 0.0)
                    entry.category = category
                    for k, v in line["msd"].items():
                        try:
                            if v and hasattr(entry, k) and v.strip():
                                try:
                                    setattr(entry, k, v.strip())
                                except e:
                                    print e, entry, line
                        except Exception:
                            raise Exception("%s" % line)
                    cont += 1
                    if cont % 1000 == 0:
                        self.stdout.write(u"... %s (%s)\n" \
                                          % (cont, line["flexion"]))
                    try:
                        entry.save()
                    except IntegrityError, e:
                        self.stdout.write(u"-- ERROR: %s.\n\t%s\n" \
                                          % (line, e))

