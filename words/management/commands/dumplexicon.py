# -*- coding: utf-8 -*-
import json

from optparse import make_option

from django.core.management.base import BaseCommand

from words.models import LexicalEntry


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--sintagma',
            action='store_true',
            dest='sintagma',
            default=False,
            help='Dumps the output according to Sintagma format.'),
        make_option('--no-polite-verbs',
            action='store_true',
            dest='no_polite_verbs',
            default=False,
            help='Dumps excluding polite forms of verbs.'),
        make_option('--only-verbs',
            action='store_true',
            dest='only_verbs',
            default=False,
            help='Dumps only the verbs.'),
        make_option('--increment',
            type='long',
            dest='increment',
            default=10000,
            help='Increment value for splitting the query up.'),
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
            except IOError:
                self.stdout.write("Unable to create a file: \"%s\"\n" \
                                  % file_name)
        filter_kwargs = {}
        if options["only_verbs"]:
            filter_kwargs = {
                "category": LexicalEntry.CATEGORY_VERB,
            }
        exclude_kwargs = {}
        if options["no_polite_verbs"]:
            exclude_kwargs = {
                "category": LexicalEntry.CATEGORY_VERB,
                "polite": LexicalEntry.POLITE_POLITE
            }
        increment = options.get("increment", 75000)
        min_rows = 0
        max_rows = LexicalEntry.objects.filter(**filter_kwargs).exclude(**exclude_kwargs).count() + increment
        if options["sintagma"]:
            if file_descr:
                cont = 0
                while min_rows <= max_rows:
                    for entry in LexicalEntry.objects.filter(**filter_kwargs).exclude(**exclude_kwargs)[min_rows:min_rows + increment]:
                        file_descr.write("%s\n" % self.print_entry_sintagma(entry))
                        if cont % 1000 == 0:
                            try:
                                self.stdout.write(u"...%s (%s)\n" % (cont, entry.word))
                            except:
                                print u"...%s (%s)" % (cont, entry.word)
                        cont += 1
                    min_rows += increment
                file_descr.close()
            else:
                while min_rows <= max_rows:
                    for entry in LexicalEntry.objects.filter(**filter_kwargs).exclude(**exclude_kwargs)[min_rows:min_rows + increment]:
                        try:
                            self.stdout.write("%s\n" % self.print_entry_sintagma(entry))
                        except:
                            print "%s\n" % self.print_entry_sintagma(entry)
                    min_rows += increment
        else:
            if file_descr:
                cont = 0
                while min_rows <= max_rows:
                    for entry in LexicalEntry.objects.filter(**filter_kwargs).exclude(**exclude_kwargs)[min_rows:min_rows + increment]:
                        file_descr.write(u"%s\n" % json.dumps(self.print_entry(entry)))
                        if cont % 1000 == 0:
                            try:
                                self.stdout.write(u"...%s (%s)\n" % (cont, entry.word))
                            except:
                                print u"...%s (%s)" % (cont, entry.word)
                        cont += 1
                    min_rows += increment
                file_descr.close()
            else:
                while min_rows <= max_rows:
                    for entry in LexicalEntry.objects.filter(**filter_kwargs).exclude(**exclude_kwargs)[min_rows:min_rows + increment]:
                        try:
                            self.stdout.write(u"%s\n" \
                                              % json.dumps(self.print_entry(entry)))
                        except:
                            print u"%s" % json.dumps(self.print_entry(entry))
                    min_rows += increment

    def print_entry(self, entry):
        dic = {
            "category": entry.category,
            "lemma": entry.lemma,
            "word": entry.word,
            "eagle": entry.eagle,
            "frequency": entry.frequency,
            "features": entry.get_features(),
        }
        return dic
    
    def print_entry_sintagma(self, entry):
        #output = "(\"" + entry.word + "\", " + entry.category.upper() + "0, " + self.print_features_sintagma(entry) + ")"
        output = "(\"%s\", %s0, %s)" % (entry.word, entry.category.upper(), self.print_features_sintagma(entry))
        return output.encode("latin1")
    
    def print_features_sintagma(self, entry):
        output = "("
        features = entry.get_features()
        keys = features.keys()
        for key in keys:
            val = features[key]
            if val:
                #output += key + ":\'" + val + "\', "
                output += "%s:\'%s\', " % (key, val)
        #output += "lemma:\'" + entry.lemma + "\', flexion:\'" + entry.word + "\')"
        output += "lemma:\'%s\', flexion:\'%s\')" % (entry.lemma, entry.word)
        #output += "lemma:\'" + entry.lemma + "\')"
        #output += "lemma:\'%s\')" % entry.lemma
        return output
