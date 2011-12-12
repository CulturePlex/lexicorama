# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class LexicalEntry(models.Model):
    word = models.CharField(_("Word"), max_length=100, db_index=True)
    lemma = models.CharField(_("Lemma"), max_length=100)
    definition = models.TextField(_("Definition"), null=True, blank=True)
    user = models.ForeignKey(User, verbose_name=_("User"),
                             related_name="words")
    date = models.DateTimeField(_("Date"), auto_now=True)
    frequency = models.FloatField(_("Frequency"), default=0)
    eagle = models.CharField(_("EAGLE"), max_length=20, null=True, blank=True)
    CATEGORY_FIELDS = {
        "adj": ['adj_degree', 'adj_interp', 'gender', 'number'],
        "adv": ['adv_meaning'],
        "art": ['art_type', 'gender', 'number'],
        "demadj": ['gender', 'number'],
        "dempron": ['gender', 'number'],
        "excl": ['gender', 'number'],
        "indefpron": ['gender', 'number'],
        "interj": [],
        "int": ['gender', 'number'],
        "conj": ['conj_type'],
        "noun": ['noun_degree', 'noun_interp', 'noun_type',
                 'gender', 'number'],
        "possadj": ['gender', 'number', 'person'],
        "posspron": ['gender', 'number', 'person'],
        "prep": ['prep_form'],
        "pron": ['pron_case', 'gender', 'number', 'person', 'pron_polite'],
        "relpron": ['gender', 'number'],
        "quan": ['quan_type', 'gender', 'number'],
        "verb": ['verb_base', 'verb_conj', 'verb_mood',
                 'verb_prnl', 'verb_tense', 'verb_trans',
                 'verb_type', 'verb_class', 'number', 'person'],
    }
    CATEGORY_ADJECTIVE = "adj"
    CATEGORY_ADVERB = "adv"
    CATEGORY_ARTICLE = "art"
    CATEGORY_CONJUCTION = "conj"
    CATEGORY_DEMONSTRATIVE_ADJECTIVE = "demadj"
    CATEGORY_DEMONSTRATIVE_PRONOUN = "dempron"
    CATEGORY_EXCLAMATIVE = "excl"
    CATEGORY_INDEFINITE_PRONOUN = "indefpron"
    CATEGORY_INTERROGATIVE = "int"
    CATEGORY_NOUN = "noun"
    CATEGORY_POSSESIVE_ADJECTIVE = "possadj"
    CATEGORY_POSSESIVE_PRONOUN = "posspron"
    CATEGORY_PREPOSITION = "prep"
    CATEGORY_PERSONAL_PRONOUN = "pron"
    CATEGORY_RELATIVE_PRONOUN = "relpron"
    CATEGORY_QUANTIFIER = "quan"
    CATEGORY_VERB = "verb"
    CATEGORY_INTERJECTION = "interj"
    CATEGORY_CHOICES = (
        (CATEGORY_ADJECTIVE, _("Adjective")),
        (CATEGORY_ADVERB, _("Adverb")),
        (CATEGORY_ARTICLE, _("Article")),
        (CATEGORY_CONJUCTION, _("Conjuction")),
        (CATEGORY_DEMONSTRATIVE_ADJECTIVE, _("Demonstrative Adjective")),
        (CATEGORY_DEMONSTRATIVE_PRONOUN, _("Demonstrative Pronoun")),
        (CATEGORY_EXCLAMATIVE, _("Exclamative")),
        (CATEGORY_INDEFINITE_PRONOUN, _("Indefinite Pronoun")),
        (CATEGORY_INTERJECTION, _("Interjection")),
        (CATEGORY_INTERROGATIVE, _("Interrogative")),
        (CATEGORY_NOUN, _("Noun")),
        (CATEGORY_POSSESIVE_ADJECTIVE, _("Possesive Adjective")),
        (CATEGORY_POSSESIVE_PRONOUN, _("Possesive Pronoun")),
        (CATEGORY_PREPOSITION, _("Preposition")),
        (CATEGORY_PERSONAL_PRONOUN, _("Personal Pronoun")),
        (CATEGORY_RELATIVE_PRONOUN, _("Relative Pronoun")),
        (CATEGORY_QUANTIFIER, _("Quantifier")),
        (CATEGORY_VERB, _("Verb")),
    )
    category = models.CharField(_("Category"), max_length=10,
                                choices=CATEGORY_CHOICES)
    # Common properties
    GENDER_COED = "coed"
    GENDER_FEMENINE = "fem"
    GENDER_MASCULINE = "masc"
    GENDER_CHOICES = (
        ("coed", _("Coed")),
        ("fem", _("Femenine")),
        ("masc", _("Masculine")),
    )
    gender = models.CharField(_("Gender"), max_length=10, blank=True,
                              choices=GENDER_CHOICES, null=True)
    NUMBER_PLURAL = "plur"
    NUMBER_SINGULAR = "sing"
    NUMBER_INVARIABLE = "inv"
    NUMBER_CHOICES = (
        (NUMBER_PLURAL, _("Plural")),
        (NUMBER_SINGULAR, _("Singular")),
        (NUMBER_INVARIABLE, _("Invariable"))
    )
    number = models.CharField(_("Number"), max_length=10, blank=True,
                              choices=NUMBER_CHOICES, null=True)
    PERSON_FIRST = "1"
    PERSON_SECOND = "2"
    PERSON_THIRD = "3"
    PERSON_CHOICES = (
        (PERSON_FIRST, _("First")),
        (PERSON_SECOND, _("Second")),
        (PERSON_THIRD, _("Third")),
    )
    person = models.CharField(_("Person"), max_length=10,
                              choices=PERSON_CHOICES, blank=True, null=True)
    # Adjectives
    # is_adjective = models.BooleanField(_("Adjective"), default=False)
    ADJ_DEGREE_COMPARATIVE = "comp"
    ADJ_DEGREE_POSITIVE = "pos"
    ADJ_DEGREE_SUPERLATIVE = "sup"
    ADJ_DEGREE_CHOICES = (
        (ADJ_DEGREE_COMPARATIVE, _("Comparative")),
        (ADJ_DEGREE_POSITIVE, _("Positive")),
        (ADJ_DEGREE_SUPERLATIVE, _("Superlative")),
    )
    adj_degree = models.CharField(_("Degree"), max_length=10,
                                        choices=ADJ_DEGREE_CHOICES, blank=True,
                                        null=True)
    ADJ_INTERP_QUANTIFIABLE = "quant"
    ADJ_INTERP_DESCRIPTIVE = "descr"
    ADJ_INTERP_CHOICES = (
        (ADJ_INTERP_QUANTIFIABLE, _("Quantificable")),
        (ADJ_INTERP_DESCRIPTIVE, _("Descriptive")),
    )
    adj_interp = models.CharField(_("Interpretation"), max_length=10,
                                  choices=ADJ_INTERP_CHOICES, blank=True,
                                  null=True)
    # Adverbs
    # is_adverb = models.BooleanField(_("Adverb"), default=False)
    ADV_MEANING_PLACE = "place"
    ADV_MEANING_TIME = "time"
    ADV_MEANING_MANNER = "mann"
    ADV_MEANING_NEGATION = "neg"
    ADV_MEANING_CONFIRMATION = "conf"
    ADV_MEANING_INCLUSION = "incl"
    ADV_MEANING_EXCLUSION = "excl"
    ADV_MEANING_OPPOSITION = "opp"
    ADV_MEANING_ORDER = "ord"
    ADV_MEANING_CHOICES = (
        (ADV_MEANING_PLACE, _("Place")),
        (ADV_MEANING_TIME, _("Time")),
        (ADV_MEANING_MANNER, _("Manner")),
        (ADV_MEANING_NEGATION, _("Negation")),
        (ADV_MEANING_CONFIRMATION, _("Confirmation")),
        (ADV_MEANING_INCLUSION, _("Inclusion")),
        (ADV_MEANING_EXCLUSION, _("Exclusion")),
        (ADV_MEANING_OPPOSITION, _("Opposition")),
        (ADV_MEANING_ORDER, _("Order")),
    )
    adv_meaning = models.CharField(_("Meaning"), max_length=10,
                                      choices=ADV_MEANING_CHOICES, blank=True,
                                      null=True)
    # Articles
    # is_article = models.BooleanField(_("Article"), default=False)
    ART_TYPE_DEFINITE = "def"
    ART_TYPE_INDEFINITE = "indef"
    ART_TYPE_CHOICES = (
        (ART_TYPE_DEFINITE, _("Definite")),
        (ART_TYPE_INDEFINITE, _("Indefinite")),
    )
    art_type = models.CharField(_("Type"), max_length=10,
                                    choices=ART_TYPE_CHOICES, blank=True,
                                    null=True)
    # Conjuctions
    # is_conjuction = models.BooleanField(_("Conjuction"), default=False)
    CONJ_TYPE_COORDINATE = "coord"
    CONJ_TYPE_SUBORDINATE = "subord"
    CONJ_TYPE_CHOICES = (
        (CONJ_TYPE_COORDINATE, _("Coordinate")),
        (CONJ_TYPE_SUBORDINATE, _("Subordinate")),
    )
    conj_type = models.CharField(_("Type"), max_length=10,
                                       choices=CONJ_TYPE_CHOICES, blank=True,
                                       null=True)
    # Demonstrative Adjectives
    # is_demonstrative_adjective = models.BooleanField(_("Demonstrative Adj."),
    #                                                  default=False)
    # Demostrative Pronouns
    # is_demonstrative_pronoun = models.BooleanField(_("Demonstrative Pronoun."),
    #                                                  default=False)
    # Exclamatives
    # is_exclamative = models.BooleanField(_("Exclamative"), default=False)
    # Interrogatives
    # is_interrogative = models.BooleanField(_("Interrogative"), default=False)
    # Nouns
    # is_noun = models.BooleanField(_("Noun"), default=False)
    NOUN_DEGREE_DIMINUTIVE = "dim"
    NOUN_DEGREE_AUMENTATIVE = "aum"
    NOUN_DEGREE_REGULAR = "reg"
    NOUN_DEGREE_CHOICES = (
        (NOUN_DEGREE_DIMINUTIVE, _("Diminutive")),
        (NOUN_DEGREE_AUMENTATIVE, _("Aumentative")),
        (NOUN_DEGREE_REGULAR, _("Regular")),
    )
    noun_degree = models.CharField(_("Degree"), max_length=10,
                                   choices=NOUN_DEGREE_CHOICES, blank=True,
                                   null=True)
    NOUN_INTERP_COUNTABLE = "count"
    NOUN_INTERP_MASSIVE = "mass"
    NOUN_INTERP_CHOICES = (
        (NOUN_INTERP_COUNTABLE, _("Countable")),
        (NOUN_INTERP_MASSIVE, _("Massive")),
    )
    noun_interp = models.CharField(_("Interpretation"), max_length=10,
                                   choices=NOUN_INTERP_CHOICES, blank=True,
                                   null=True)
    NOUN_TYPE_COMMON = "comm"
    NOUN_TYPE_PROPER = "prop"
    NOUN_TYPE_CHOICES = (
        (NOUN_TYPE_COMMON, _("Common")),
        (NOUN_TYPE_PROPER, _("Proper")),
    )
    noun_type = models.CharField(_("Type"), max_length=10,
                                 choices=NOUN_TYPE_CHOICES, blank=True,
                                 null=True)
    # Possesive Adjectives
    # is_possesive_adjective = models.BooleanField(_("Possesive Adj."),
    #                                              default=False)
    # Possesive Pronouns
    # is_possesive_pronoun = models.BooleanField(_("Possesive Pronoun."),
    #                                            default=False)
    # Prepositions
    # is_preposition = models.BooleanField(_("Preposition"), default=False)
    PREP_FORM_SIMPLE = "simp"
    PREP_FORM_CONTRACTED = "contr"
    PREP_FORM_CHOICES = (
        (PREP_FORM_SIMPLE, _("Simple")),
        (PREP_FORM_CONTRACTED, _("Contracted")),
    )
    prep_form = models.CharField(_("Form"), max_length=10,
        choices=PREP_FORM_CHOICES, blank=True, null=True)
    # Pronouns
    # is_pronoun = models.BooleanField(_("Pronoun"), default=False)
    PRON_CASE_NOMINATIVE = "nom"
    PRON_CASE_ACCUSATIVE = "acc"
    PRON_CASE_DATIVE = "dat"
    PRON_CASE_OBLIQUE = "obl"
    PRON_CASE_CHOICES = (
        (PRON_CASE_NOMINATIVE , _("Nominative")),
        (PRON_CASE_ACCUSATIVE, _("Accusative")),
        (PRON_CASE_DATIVE, _("Dative")),
        (PRON_CASE_OBLIQUE, _("Oblique")),
    )
    pron_case = models.CharField(_("Case"), max_length=10,
                                 choices=PRON_CASE_CHOICES, blank=True,
                                 null=True)
    PRON_POLITE_REGULAR = "reg"
    PRON_POLITE_POLITE = "pol"
    PRON_POLITE_CHOICES = (
        (PRON_POLITE_REGULAR , _("Nominative")),
        (PRON_POLITE_POLITE, _("Accusative")),
    )
    pron_polite = models.CharField(_("Politeness"), max_length=10,
                                    choices=PRON_POLITE_CHOICES, blank=True,
                                    null=True)
    # Quantifiers
    # is_quantifier = models.BooleanField(_("Quantifier"), default=False)
    QUAN_TYPE_CARDINAL = "card"
    QUAN_TYPE_ORDINAL = "ord"
    QUAN_TYPE_MULTIPLIER = "mult"
    QUAN_TYPE_PARTITIVE = "part"
    QUAN_TYPE_DISTRIBUTIVE = "dist"
    QUAN_TYPE_INDEFINITE = "indef"
    QUAN_TYPE_CHOICES = (
        (QUAN_TYPE_CARDINAL, _("Cardinal")),
        (QUAN_TYPE_ORDINAL, _("Ordinal")),
        (QUAN_TYPE_MULTIPLIER, _("Multiplier")),
        (QUAN_TYPE_PARTITIVE, _("Partitive")),
        (QUAN_TYPE_DISTRIBUTIVE, _("Distributive")),
        (QUAN_TYPE_INDEFINITE, _("Indefinite")),
    )
    quan_type = models.CharField(_("Type"), max_length=10,
                                         choices=QUAN_TYPE_CHOICES, blank=True,
                                         null=True)
    # Verbs
    # is_verb = models.BooleanField(_("Verb"), default=False)
    VERB_BASE_COPULATIVE = "cop"
    VERB_BASE_PREDICATIVE = "pred"
    VERB_BASE_CHOICES = (
        (VERB_BASE_COPULATIVE, _("Copulative")),
        (VERB_BASE_PREDICATIVE, _("Predicative")),
    )
    verb_base = models.CharField(_("Base"), max_length=10,
                                 choices=VERB_BASE_CHOICES, blank=True,
                                 null=True)
    VERB_CONJ_REGULAR = "reg"
    VERB_CONJ_IRREGULAR = "irreg"
    VERB_CONJ_CHOICES = (
        (VERB_CONJ_REGULAR, _("Regular")),
        (VERB_CONJ_IRREGULAR, _("Irregular")),
    )
    verb_conj = models.CharField(_("Conjugation"), max_length=10,
                                 choices=VERB_CONJ_CHOICES, blank=True,
                                 null=True)
    VERB_MOOD_INDICATIVE = "ind"
    VERB_MOOD_SUBJUNCTIVE = "sub"
    VERB_MOOD_IMPERATIVE = "imp"
    VERB_MOOD_INFINITIVE = "inf"
    VERB_MOOD_GERUND = "ger"
    VERB_MOOD_PARTICIPLE = "par"
    VERB_MOOD_CHOICES = (
        (VERB_MOOD_INDICATIVE, _("Indicative")),
        (VERB_MOOD_SUBJUNCTIVE, _("Subjunctive")),
        (VERB_MOOD_IMPERATIVE, _("Imperative")),
        (VERB_MOOD_INFINITIVE, _("Infinitive")),
        (VERB_MOOD_GERUND, _("Gerund")),
        (VERB_MOOD_PARTICIPLE, _("Participle")),
    )
    verb_mood = models.CharField(_("Mood"), max_length=10,
                                 choices=VERB_MOOD_CHOICES, blank=True,
                                 null=True)
    VERB_PRNL_PRONOMINAL = "prnl"
    VERB_PRNL_NONPRONOMINAL = "nonprnl"
    VERB_PRNL_CHOICES = (
        (VERB_PRNL_PRONOMINAL, _("Pronominal")),
        (VERB_PRNL_NONPRONOMINAL, _("Non Pronominal")),
    )
    verb_prnl = models.CharField(_("Pronominality"),
                                 max_length=10,
                                 choices=VERB_PRNL_CHOICES,
                                 blank=True, null=True)
    VERB_TENSE_PRESENT = "pres"
    VERB_TENSE_PRETERIT = "pret"
    VERB_TENSE_IMPERFECT = "imperf"
    VERB_TENSE_FUTURE = "fut"
    VERB_TENSE_CONDITIONAL = "cond"
    VERB_TENSE_CHOICES = (
        (VERB_TENSE_PRESENT, _("Present")),
        (VERB_TENSE_PRETERIT, _("Preterit")),
        (VERB_TENSE_IMPERFECT, _("Imperfect")),
        (VERB_TENSE_FUTURE, _("Future")),
        (VERB_TENSE_CONDITIONAL, _("Conditional")),
    )
    verb_tense = models.CharField(_("Tense"), max_length=10,
        choices=VERB_TENSE_CHOICES, blank=True, null=True)
    VERB_TRANS_TRANSITIVE = "trans"
    VERB_TRANS_INTRANSITIVE = "intrans"
    VERB_TRANS_CHOICES = (
        (VERB_TRANS_TRANSITIVE, _("Transitive")),
        (VERB_TRANS_INTRANSITIVE, _("Intransitive")),
    )
    verb_trans = models.CharField(_("Transivity"), max_length=10,
                                  choices=VERB_TRANS_CHOICES, blank=True,
                                  null=True)
    VERB_TYPE_MAIN = "main"
    VERB_TYPE_AUXILIAR = "aux"
    VERB_TYPE_CHOICES = (
        (VERB_TYPE_MAIN, _("Main")),
        (VERB_TYPE_AUXILIAR, _("Auxiliary")),
    )
    verb_type = models.CharField(_("Type"), max_length=10,
                                 choices=VERB_TYPE_CHOICES, blank=True,
                                 null=True)
    VERB_CLASS_AR = "ar"
    VERB_CLASS_ER = "er"
    VERB_CLASS_IR = "ir"
    VERB_CLASS_CHOICES = (
        (VERB_CLASS_AR, _("First (-ar)")),
        (VERB_CLASS_ER, _("Second (-er)")),
        (VERB_CLASS_IR, _("Third (-ir)")),
    )
    verb_class = models.CharField(_("Class"), max_length=10,
                                  choices=VERB_CLASS_CHOICES, blank=True,
                                  null=True)

    class Meta:
        ordering = ["lemma", "word", "frequency", "date"]
        unique_together = (
            ('word', 'lemma', 'category', 'adj_degree', 'adj_interp',
                'gender', 'number'),
            ('word', 'lemma', 'category', 'adv_meaning'),
            ('word', 'lemma', 'category', 'art_type', 'gender', 'number'),
            # ('word', 'lemma', 'category', 'gender', 'number'),
            ('word', 'lemma', 'category', 'conj_type'),
            ('word', 'lemma', 'category', 'noun_degree', 'noun_interp',
                'noun_type', 'gender', 'number'),
            # ('word', 'lemma', 'category', 'gender', 'number', 'person'),
            ('word', 'lemma', 'category', 'prep_form'),
            ('word', 'lemma', 'category', 'pron_case', 'gender', 'number',
                'person', 'pron_polite'),
            ('word', 'lemma', 'category', 'quan_type', 'gender', 'number'),
            ('word', 'lemma', 'category', 'verb_base', 'verb_conj',
                'verb_mood','verb_prnl', 'verb_tense', 'verb_trans',
                'verb_type', 'verb_class', 'number', 'person')
        )
        verbose_name = _("Lexical Entry")
        verbose_name_plural = _("Lexical Entries")

    def __unicode__(self):
        return u"%s (%s)" % (self.word, self.category)

    def get_features(self):
        features = {}
        for feature in self.CATEGORY_FIELDS[self.category]:
            features[feature] = getattr(self, feature, None)
        return features

    def get_features_display(self):
        features = []
        for feature in self.CATEGORY_FIELDS[self.category]:
            feature_value = getattr(self, feature, None)
            feature_display =  self._meta.get_field(feature).verbose_name
            if feature_value:
                feature_value_display = getattr(self, "get_%s_display"
                                                        % feature)()
                feature = u"<strong style='color: #666'>%s</strong>: %s" \
                          % (feature_display, feature_value_display)
            else:
                feature = u"%s: (None)" % (feature_display)
            features.append(feature)
        return u", ".join(features)
