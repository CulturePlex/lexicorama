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
    args = "drae_file"
    help = "\tLoads DRAE transitivity, pronominality and interjections."
    can_import_settings = True

    def handle(self, *args, **options):
        if not args:
            raise CommandError("All the parameters must be provided.")
        file_name = args[0]
        try:
            file_descr = open(file_name, "r")
        except IOError, e:
            self.stdout.write("File not found: \"%s\"\n" % file_name)
        drae = json.loads("".join(file_descr.readlines()))
        file_descr.close()
        cont = 0
        user = User.objects.all()[0]
        with transaction.commit_on_success():
            category_interj = LexicalEntry.CATEGORY_INTERJECTION
            interjections = [d["lemma"] for d in
                             LexicalEntry.objects.filter(category=category_interj).values("lemma")]
            for lemma in drae:
                transitive = LexicalEntry.VERB_TRANS_TRANSITIVE
                intransitive =  LexicalEntry.VERB_TRANS_INTRANSITIVE
                pronominal = LexicalEntry.VERB_PRNL_PRONOMINAL
                nonpronominal = LexicalEntry.VERB_PRNL_NONPRONOMINAL
                word = lemma["lema"]
                if ("verbo pronominal" in lemma["abrvs"]
                    and "verbo transitivo" not in lemma["abrvs"]
                    and "verbo intransitivo" not in lemma["abrvs"]):
                    entries = LexicalEntry.objects.filter(word=word)
                    entries.update(verb_prnl=pronominal)
                elif ("verbo transitivo" in lemma["abrvs"]
                      and "verbo intransitivo" not in lemma["abrvs"]):
                    if "verbo pronominal" not in lemma["abrvs"]:
                        entries = LexicalEntry.objects.filter(word=word)
                        entries.update(verb_trans=transitive,
                                       verb_prnl=nonpronominal)
                    else:
                        entries = LexicalEntry.objects.filter(word=word)
                        entries.update(verb_trans=transitive)
                elif ("verbo transitivo" not in lemma["abrvs"]
                      and "verbo intransitivo" in lemma["abrvs"]):
                    if "verbo pronominal" not in lemma["abrvs"]:
                        entries = LexicalEntry.objects.filter(word=word)
                        entries.update(verb_trans=transitive,
                                       verb_prnl=nonpronominal)
                    else:
                        entries = LexicalEntry.objects.filter(word=word)
                        entries.update(verb_trans=intransitive)
                elif (u"interjección" in lemma["abrvs"]
                    and word not in interjections):
                    entry = LexicalEntry()
                    entry.category = category_interj
                    entry.user = user
                    entry.lemma = word
                    entry.word = word
                    entry.save()
                if cont % 1000 == 0:
                    try:
                        self.stdout.write(u"...%s (%s)\n" % (cont, word))
                    except:
                        print u"...%s (%s)\n" % (cont, word)
                cont += 1
