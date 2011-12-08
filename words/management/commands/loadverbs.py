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
    Loads verbs files from DRAE into LexicalEntry objects

    Usage:
    python manage.py loadverbs /tmp/verbs/verb 2 100 .txt
    """
    can_import_settings = True

    def handle(self, *args, **options):
        try:
            prefix = args[0]
            start = int(args[1])
            end = int(args[2])
            suffix = args[3]
        except IndexError:
            raise CommandError("All the parameters must be provided.")
        spaces = re.compile(r"[ ]+")
        user = User.objects.get(username="admin")
        atones_pronouns = ["me", "te", "se", "nos", "os"]
        defective = [u"abarse", u"abocanar", u"acaecer", u"acantelear",
                     u"acontecer", u"adir", u"alborecer", u"algarecear",
                     u"antojarse", u"atañer", u"atardecer", u"brisar",
                     u"cascarrinar", u"cellisquear", u"cercear", u"chaparrear",
                     u"clarecer", u"concernir", u"diluviar", u"empecer",
                     u"empedernir", u"encelajarse", u"garuar", u"granizar",
                     u"harinear", u"mollinear", u"mollinizar", u"molliznear",
                     u"neblinear", u"neviscar", u"obstar", u"orvallar", u"paramar",
                     u"paramear", u"pintear", u"podrir", u"raspahilar", u"repodrid",
                     u"respahilar", u"rocear", u"rosar", u"tardecer", u"usucapir",
                     u"ventiscar", u"ventisquear", u"zaracear"]
        for i in xrange(start, end + 1):
            with transaction.commit_on_success():
                file_name = "%s%s%s" % (prefix, i, suffix)
                file_descr = ""
                try:
                    file_descr = open(file_name, "r")
                except IOError:
                    self.stdout.write("File not found: \"%s\"\n" % file_name)
                lines = []
                for file_line in file_descr:
                    if file_line.startswith("|"):
                        line = " ".join(spaces.split(file_line.replace("_", " ").strip())).split("|")[1:-1]
                        lines.append(line)
                non_personal, personal, imperative = self.split_mood(lines)
                headword = ""
                reflexiveness = ""
                klass = ""
                vtype = LexicalEntry.VERB_TYPE_MAIN
                for row in non_personal:
                    row_type = row[0].strip().lower()
                    if u"infinitivo" in row_type:
                        verb = unicode(row[1].strip().decode("utf8"))
                        headword = verb
                        entry = {
                            "word": verb,
                            "headword": headword,
                            "category": LexicalEntry.CATEGORY_VERB,
                        }
                        if verb == u"haber":
                            entry["verb_type"] = LexicalEntry.VERB_TYPE_AUXILIAR
                        else:
                            entry["verb_type"] = LexicalEntry.VERB_TYPE_MAIN
                        entry["verb_mood"] = LexicalEntry.VERB_MOOD_INFINITIVE
                        if verb.endswith(u"arse")  or verb.endswith(u"árse"):
                            entry["verb_class"] = LexicalEntry.VERB_CLASS_AR
                            entry["verb_reflexiveness"] = LexicalEntry.VERB_REFL_REFLEXIVE
                        elif verb.endswith(u"erse")  or verb.endswith(u"érse"):
                            entry["verb_class"] = LexicalEntry.VERB_CLASS_ER
                            entry["verb_reflexiveness"] = LexicalEntry.VERB_REFL_REFLEXIVE
                        elif verb.endswith(u"irse")  or verb.endswith(u"írse"):
                            entry["verb_class"] = LexicalEntry.VERB_CLASS_IR
                            entry["verb_reflexiveness"] = LexicalEntry.VERB_REFL_REFLEXIVE
                        elif verb.endswith(u"ar") or verb.endswith(u"ár"):
                            entry["verb_class"] = LexicalEntry.VERB_CLASS_AR
                            entry["verb_reflexiveness"] = None  # LexicalEntry.VERB_REFL_NONREFLEXIVE
                        elif verb.endswith(u"er") or verb.endswith(u"ér"):
                            entry["verb_class"] = LexicalEntry.VERB_CLASS_ER
                            entry["verb_reflexiveness"] = None  # LexicalEntry.VERB_REFL_NONREFLEXIVE
                        elif verb.endswith(u"ir") or verb.endswith(u"ír"):
                            entry["verb_class"] = LexicalEntry.VERB_CLASS_IR
                            entry["verb_reflexiveness"] = None  # LexicalEntry.VERB_REFL_NONREFLEXIVE
                        if verb:
                            reflexiveness = entry["verb_reflexiveness"]
                            klass = entry["verb_class"]
                            vtype = entry["verb_type"]
                            # entry.save()
                            self.print_entry(entry, user)
                    elif u"participio" in row_type:
                        verbs = unicode(row[1].strip().decode("utf8"))
                        if u"," in verbs:
                            for verb in verbs.split(","):
                                verb = verb.strip()
                                entry = {
                                    "word": verb,
                                    "headword": headword,
                                    "category": LexicalEntry.CATEGORY_VERB,
                                }
                                entry["verb_mood"] = LexicalEntry.VERB_MOOD_PARTICIPLE
                                entry["verb_reflexiveness"] = reflexiveness
                                entry["verb_class"] = klass
                                entry["verb_type"] = vtype
                                # entry.save()
                                self.print_entry(entry, user)
                        elif verbs:
                            entry = {
                                "word": verbs,
                                "headword": headword,
                                "category": LexicalEntry.CATEGORY_VERB,
                            }
                            entry["verb_mood"] = LexicalEntry.VERB_MOOD_PARTICIPLE
                            entry["verb_reflexiveness"] = reflexiveness
                            entry["verb_class"] = klass
                            entry["verb_type"] = vtype
                            # entry.save()
                            self.print_entry(entry, user)
                    elif u"gerundio" in row_type:
                        verbs = unicode(row[1].strip().decode("utf8"))
                        if "etc." in verbs:
                            verb_stem = verbs.replace("etc.", "").split(",")[0].strip()[:-2]
                            for verb_suffix in atones_pronouns:
                                entry = {
                                    "word": u"%s%s" % (verb_stem, verb_suffix),
                                    "headword": headword,
                                    "category": LexicalEntry.CATEGORY_VERB,
                                }
                                entry["verb_mood"] = LexicalEntry.VERB_MOOD_GERUND
                                entry["verb_reflexiveness"] = reflexiveness
                                entry["verb_class"] = klass
                                entry["verb_type"] = vtype
                                # entry.save()
                                self.print_entry(entry, user)
                        elif verbs:
                            entry = {
                                "word": verbs,
                                "headword": headword,
                                "category": LexicalEntry.CATEGORY_VERB,
                            }
                            entry["verb_mood"] = LexicalEntry.VERB_MOOD_GERUND
                            entry["verb_reflexiveness"] = reflexiveness
                            entry["verb_class"] = klass
                            entry["verb_type"] = vtype
                            # entry.save()
                            self.print_entry(entry, user)
                for i, flexions in enumerate(personal):
                    mood = LexicalEntry.VERB_MOOD_INDICATIVE
                    if i == 2:
                        mood = LexicalEntry.VERB_MOOD_SUBJUNCTIVE
                    tense = LexicalEntry.VERB_TENSE_PRESENT
                    person_count = 0
                    for words in flexions:
                        words = unicode(words.strip().decode("utf8")).lower()
                        if len(words) > 0:
                            if u"presente" in words:
                                tense = LexicalEntry.VERB_TENSE_PRESENT
                                person_count = 0
                            elif u"condicional" in words or u"pospretérito" in words:
                                tense = LexicalEntry.VERB_TENSE_CONDITIONAL
                                person_count = 0
                            elif u"futuro" in words:
                                tense = LexicalEntry.VERB_TENSE_FUTURE
                                person_count = 0
                            elif u"imperfecto" in words or u"copretérito" in words:
                                tense = LexicalEntry.VERB_TENSE_IMPERFECT
                                person_count = 0
                            elif u"perfecto" in words:
                                tense = LexicalEntry.VERB_TENSE_PRETERIT
                                person_count = 0
                            else:
                                number = LexicalEntry.NUMBER_SINGULAR
                                if person_count > 3:
                                    number = LexicalEntry.NUMBER_PLURAL
                                if headword in defective:
                                    person = 3
                                else:
                                    person = str((person_count % 3) + 1)
                                for verb in words.replace(" o ", " / ").replace(" u ", " / ").split("/"):
                                    if u" " in verb:
                                        for pron in atones_pronouns:
                                            if u"%s " % pron in verb:
                                                verb = verb.replace(pron, "", 1)
                                    verb = verb.strip()
                                    if verb and verb not in atones_pronouns:
                                        entry = {
                                            "word": verb,
                                            "headword": headword,
                                            "category": LexicalEntry.CATEGORY_VERB,
                                        }
                                        entry["verb_mood"] = mood
                                        entry["verb_reflexiveness"] = reflexiveness
                                        entry["verb_class"] = klass
                                        entry["number"] = number
                                        entry["person"] = person
                                        entry["verb_tense"] = tense
                                        entry["verb_type"] = vtype
                                        # entry.save()
                                        self.print_entry(entry, user)
                                person_count += 1
                for flexions in imperative:
                    flexions = flexions.replace("(tú / vos)", "")
                    flexions = flexions.replace("(tú)", "")
                    flexions = flexions.replace("(vos)", "")
                    flexions = flexions.replace("(vosotros / ustedes)", "")
                    flexions = flexions.replace("(vosotros)", "")
                    flexions = flexions.replace("(ustedes)", "")
                    flexions = flexions.replace(" o ", " / ")
                    flexions = flexions.replace(" u ", " / ")
                    for i, verb in enumerate(flexions.split("/")):
                        verb = unicode(verb.strip().decode("utf8")).lower()
                        if i == 0:
                            number = LexicalEntry.NUMBER_SINGULAR
                        else:
                            number = LexicalEntry.NUMBER_PLURAL
                        verb = verb.strip()
                        entry = {
                            "word": verb,
                            "headword": headword,
                            "category": LexicalEntry.CATEGORY_VERB,
                        }
                        entry["verb_mood"] = LexicalEntry.VERB_MOOD_IMPERATIVE
                        entry["verb_reflexiveness"] = reflexiveness
                        entry["verb_class"] = klass
                        entry["number"] = number
                        entry["person"] = LexicalEntry.PERSON_SECOND
                        entry["verb_type"] = vtype
                        # entry.save()
                        self.print_entry(entry, user)

    def split_mood(self, lines):
        lines_len = len(lines)
        non_personal_pos = None
        indicative_pos = None
        imperative_pos = None
        for i in range(0, lines_len):
            row_len = len(lines[i])
            for j in range(0, row_len):
                item = unicode(lines[i][j].decode("utf8")).lower().strip()
                if u"no personales" in item:
                    non_personal_pos = i
                elif "indicativo" in item:
                    indicative_pos = i
                elif "imperativo" in item:
                    imperative_pos = i
        personal_lines = []
        non_personal = zip(*(lines[non_personal_pos + 1:indicative_pos]))
        if imperative_pos is not None:
            personal_lines = lines[indicative_pos + 1:imperative_pos]
            imperative = zip(*(lines[imperative_pos + 1:]))[0]
        else:
            personal = lines[indicative_pos + 1:]
            imperative = []
        # Handle verbs without Subjunctive Present
        for personal_line in personal_lines:
            if len(personal_line) < 3:
                personal_line.append("")
        personal = zip(*personal_lines)
        return non_personal, personal, imperative

    def print_entry(self, entry, user):
        dic = {
            "category": entry.pop("category"),
            "lemma": entry.pop("headword"),
            "flexion": entry.pop("word"),
            "msd": entry,
        }
        self.stdout.write(json.dumps(dic) + u"\n")
    #self.stdout.write(u"%30s: %s\\n" % (entry, entry.get_features()))
    #            self.stdout.write('Non personal: "%s"\n' % non_personal)
    #            self.stdout.write('Personal: "%s"\n' % personal)
    #            self.stdout.write('Imperative: "%s"\n' % imperative)
