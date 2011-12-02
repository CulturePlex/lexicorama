# -*- coding: utf-8 -*-
import re

from django.core.management.base import BaseCommand, CommandError

from words.models import LexicalEntry


class Command(BaseCommand):
    args = "prefix start end suffix"
    help = """
    Loads verbs files from DRAE into LexicalEntry objects
    
    Usage:
    python manage.py load_verbs /tmp/verbs/verb 2 100 .txt
    """
    can_import_settings = True

    def handle(self, *args, **options):
        try:
            prefix = args[0]
            start = int(args[1])
            end = int(args[2])
            suffix = args[3]
        except IndexError, e:
            raise CommandError("All the parameters must be provided.")
        spaces = re.compile(r"[ ]+")
        for i in xrange(start, end + 1):
            file_name = "%s%s%s" % (prefix, i, suffix)
            file_descr = ""
            try:
                file_descr = open(file_name, "r")
            except IOError, e:
                self.stdout.write("File not found: \"%s\"\n" % file_name)
            lines = []
            for file_line in file_descr:
                if file_line.startswith("|"):
                    line = " ".join(spaces.split(file_line.replace("_", " ").strip())).split("|")[1:-1]
                    lines.append(line)
            non_personal = zip(*(lines[1:3]))
            headword = ""
            reflexiveness = ""
            klass = ""
            for row in non_personal:
                row_type = row[0].strip().lower()
                if "infinitivo" in row_type:
                    verb = unicode(row[1].strip().decode("utf8"))
                    headword = verb
                    entry = LexicalEntry()
                    entry.word = verb
                    entry.headword = headword
                    entry.category = LexicalEntry.CATEGORY_VERB
                    entry.mood = LexicalEntry.VERB_MOOD_INFINITIVE
                    if verb.endswith("arse"):
                        entry.verb_class = LexicalEntry.VERB_CLASS_AR
                        entry.verb_reflexiveness = LexicalEntry.VERB_REFL_REFLEXIVE
                    elif verb.endswith("erse"):
                        entry.verb_class = LexicalEntry.VERB_CLASS_ER
                        entry.verb_reflexiveness = LexicalEntry.VERB_REFL_REFLEXIVE
                    elif verb.endswith("irse"):
                        entry.verb_class = LexicalEntry.VERB_CLASS_IR
                        entry.verb_reflexiveness = LexicalEntry.VERB_REFL_REFLEXIVE
                    elif verb.endswith("ar"):
                        entry.verb_class = LexicalEntry.VERB_CLASS_AR
                        entry.verb_reflexiveness = LexicalEntry.VERB_REFL_NONREFLEXIVE
                    elif verb.endswith("er"):
                        entry.verb_class = LexicalEntry.VERB_CLASS_ER
                        entry.verb_reflexiveness = LexicalEntry.VERB_REFL_NONREFLEXIVE
                    elif verb.endswith("ir"):
                        entry.verb_class = LexicalEntry.VERB_CLASS_IR
                        entry.verb_reflexiveness = LexicalEntry.VERB_REFL_NONREFLEXIVE
                    reflexiveness = entry.verb_reflexiveness
                    klass = entry.verb_class
                    self.stdout.write(u"%s:\t\t%s\n" % (entry, entry.get_features()))
                elif "participio" in row_type:
                    verb = unicode(row[1].strip().decode("utf8"))
                    entry = LexicalEntry()
                    entry.word = verb
                    entry.headword = headword
                    entry.category = LexicalEntry.CATEGORY_VERB
                    entry.mood = LexicalEntry.VERB_MOOD_PARTICIPLE
                    entry.verb_reflexiveness = reflexiveness
                    entry.verb_class = klass
                    self.stdout.write(u"%s:\t\t%s\n" % (entry, entry.get_features()))
                elif "gerundio" in row_type:
                    verbs = unicode(row[1].strip().decode("utf8"))
                    if "etc." in verbs:
                        verb_stem = verbs.replace("etc.", "").split(",")[0].strip()[:-2]
                        for verb_suffix in ["", "me", "te", "se", "nos", "os"]:
                            entry = LexicalEntry()
                            entry.word = u"%s%s" % (verb_stem, verb_suffix)
                            entry.headword = headword
                            entry.category = LexicalEntry.CATEGORY_VERB
                            entry.mood = LexicalEntry.VERB_MOOD_GERUND
                            entry.verb_reflexiveness = reflexiveness
                            entry.verb_class = klass
                            self.stdout.write(u"%s:\t\t%s\n" % (entry, entry.get_features()))

#            personal = zip(*(lines[4:25]))
#            imperative = zip(*(lines[26:]))
#            self.stdout.write('Non personal: "%s"\n' % non_personal)
#            self.stdout.write('Personal: "%s"\n' % personal)
#            self.stdout.write('Imperative: "%s"\n' % imperative)
