# -*- coding: utf-8 -*-
import json

from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from words.models import LexicalEntry


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--output-file',
            type='string',
            dest='output_file',
            default=None,
            help='File name for JSON output.'),
    )
    args = "source_file"
    help = "\tProccess a lexicon file in FreeLing format."
    can_import_settings = True

    def handle(self, *args, **options):
        if not args:
            raise CommandError("All the parameters must be provided.")
        file_name = args[0]
        try:
            file_descr = open(file_name, "r")
        except IOError:
            self.stdout.write("File not found: \"%s\"\n" % file_name)
        cont = 0
        output_descr = None
        output_file = options["output_file"]
        if output_file:
            try:
                output_descr = open(output_file, "w")
            except IOError:
                self.stdout.write("Unable to create an output file: \"%s\"\n" \
                                  % output_file)
        for line in file_descr:
            if not line.strip():
                continue
            line_split = line.split(" ")
            flexion, lemma, msd = line_split[:3]
            msd = msd.strip()
            output = {}

            features = {}
            #ADJECTVE
            if msd[:2] == "AQ":
                category = "ADJ"
                #Grade
                if msd[2] == "0" or msd[2] == "A" or msd[2] == "C":
                    features["adj_degree"] = "pos"
                elif msd[2] == "S":
                    features["adj_degree"] = "sup"
                else:
                    features["adj_degree"] = "" #falta comp
                    self.stdout.write("Error en adjetivo " + flexion + ": " \
                          "grade " + msd[2] + " incorrecto.")
                #Gender
                if msd[3] == "M":
                    features["gender"] = "masc"
                elif msd[3] == "F":
                    features["gender"] = "fem"
                elif msd[3] == "C":
                    features["gender"] = "coed"
                else:
                    features["gender"] = ""
                    self.stdout.write("Error en adjetivo "+ flexion + ": " \
                          "gender " + msd[3] + " incorrecto.")
                #Interpretation
                features["adj_interp"] = ""
                #Number
                if msd[4] == "S":
                    features["number"] = "sing"
                elif msd[4] == "P":
                    features["number"] = "plur"
                elif msd[4] == "N":
                    features["number"] = "inv"
                else:
                    features["number"] = ""
                    self.stdout.write("Error en adjetivo " + flexion + ": " \
                          "number " + msd[4] + " incorrecto.")
            elif msd[0] == "V" and msd[2] == "P":
                category = "ADJyVERB"
                #Grade
                features["adj_degree"] = "pos"
                #Gender
                if msd[6] == "M" or msd[6] == "0":
                    features["gender"] = "masc"
                elif msd[6] == "F":
                    features["gender"] = "fem"
                else:
                    features["gender"] = ""
                    self.stdout.write("Error en adjetivo "+ flexion + ": " \
                          "gender " + msd[6] + " incorrecto.")
                #Interpretation
                features["adj_interp"] = ""
                #Number
                if msd[5] == "S" or msd[5] == "0":
                    features["number"] = "sing"
                elif msd[5] == "P":
                    features["number"] = "plur"
                else:
                    features["number"] = ""
                    self.stdout.write("Error en adjetivo " + flexion + ": " \
                          "number " + msd[5] + " incorrecto.")
            
            #ADVERB
            elif msd[0] == "R":
                category = "ADV"
                #Meaning
                if msd[1] == "N":
                    features["adv_mean"] = "neg"
                elif msd[1] == "G" or msd[1] == "I" or msd[1] == "R" or msd[1] == "T":
                    features["adv_mean"] = "" #faltan el resto
                else:
                    features["adv_mean"] = ""
                    self.stdout.write("Error en adverbio " + flexion + ": " \
                          "meaning " + msd[1] + " incorrecto.")
            
            #ARTICLE
            elif msd[:2] == "DA" or self.isArtIndef(msd,lemma):
                category = "ART"
                #Gender
                if msd[3] == "M":
                    features["gender"] = "masc"
                elif msd[3] == "F":
                    features["gender"] = "fem"
                elif msd[3] == "N":
                    features["gender"] = "coed"
                else:
                    features["gender"] = ""
                    self.stdout.write("Error en articulo " + flexion + ": " \
                          "gender " + msd[3] + " incorrecto.")
                #Number
                if msd[4] == "S":
                    features["number"] = "sing"
                elif msd[4] == "P":
                    features["number"] = "plur"
                else:
                    features["number"] = ""
                    self.stdout.write("Error en articulo " + flexion + ": " \
                          "number " + msd[4] + " incorrecto.")
                #Type
                if msd[:2] == "DA":
                    features["art_type"] = "def"
                else:
                    features["art_type"] = "indef"
            
            #CONJUNCTION
            elif msd[0] == "C":
                category = "CONJ"
                #Type
                if msd[1] == "C":
                    features["conj_type"] = "coord"
                elif msd[1] == "S":
                    features["conj_type"] = "subord"
                else:
                    features["conj_type"] = ""
                    self.stdout.write("Error en conjuncion " + flexion + ": " \
                          "type " + msd[1] + " incorrecto.")
            
            #DEMONSTRATIVE ADJECTIVE
            elif msd[:2] == "DD":
                category = "DEMADJ"
                #Gender
                if msd[3] == "M":
                    features["gender"] = "masc"
                elif msd[3] == "F":
                    features["gender"] = "fem"
                elif msd[3] == "C":
                    features["gender"] = "coed"
                else:
                    features["gender"] = ""
                    self.stdout.write("Error en adjetivo demostrativo " + flexion + ": " \
                          "gender " + msd[3] + " incorrecto.")
                #Number
                if msd[4] == "S":
                    features["number"] = "sing"
                elif msd[4] == "P":
                    features["number"] = "plur"
                else:
                    features["number"] = ""
                    self.stdout.write("Error en adjetivo demostrativo " + flexion + ": " \
                          "number " + msd[4] + " incorrecto.")
            
            #DEMONSTRATIVE PRONOUN
            elif msd[:2] == "PD":
                category = "DEMPRON"
                #Gender
                if msd[3] == "M":
                    features["gender"] = "masc"
                elif msd[3] == "F":
                    features["gender"] = "fem"
                elif msd[3] == "C" or msd[3] == "N":
                    features["gender"] = "coed"
                else:
                    features["gender"] = ""
                    self.stdout.write("Error en pronombre demostrativo " + flexion + ": " \
                          "gender " + msd[3] + " incorrecto.")
                #Number
                if msd[4] == "S":
                    features["number"] = "sing"
                elif msd[4] == "P":
                    features["number"] = "plur"
                else:
                    features["number"] = ""
                    self.stdout.write("Error en pronombre demostrativo " + flexion + ": " \
                          "number " + msd[4] + " incorrecto.")
            
            #EXCLAMATORY
            elif msd[:2] == "DE" or msd[:2] == "PE":
                category = "EXCL"
                #Gender
                if msd[3] == "M":
                    features["gender"] = "masc"
                elif msd[3] == "F":
                    features["gender"] = "fem"
                elif msd[3] == "C":
                    features["gender"] = "coed"
                elif msd[3] == "0":
                    features["gender"] = ""
                else:
                    features["gender"] = ""
                    self.stdout.write("Error en exclamativo " + flexion + ": " \
                          "gender " + msd[3] + " incorrecto.")
                #Number
                if msd[4] == "S":
                    features["number"] = "sing"
                elif msd[4] == "P":
                    features["number"] = "plur"
                elif msd[4] == "N":
                    features["number"] = "inv"
                elif msd[4] == "0":
                    features["number"] = ""
                else:
                    features["number"] = ""
                    self.stdout.write("Error en exclamativo " + flexion + ": " \
                          "number " + msd[4] + " incorrecto.")
            
            #INDEFINITE PRONOUN
            elif msd[:2] == "PI":
                category = "INDEFPRON"
                #Gender
                if msd[3] == "M":
                    features["gender"] = "masc"
                elif msd[3] == "F":
                    features["gender"] = "fem"
                elif msd[3] == "C":
                    features["gender"] = "coed"
                else:
                    features["gender"] = ""
                    self.stdout.write("Error en pronombre indefinido " + flexion + ": " \
                          "gender " + msd[3] + " incorrecto.")
                #Number
                if msd[4] == "S":
                    features["number"] = "sing"
                elif msd[4] == "P":
                    features["number"] = "plur"
                else:
                    features["number"] = ""
                    self.stdout.write("Error en pronombre relativo " + flexion + ": " \
                          "number " + msd[4] + " incorrecto.")
            
            #INTERROGATIVE
            elif msd[:2] == "DT" or msd[:2] == "PT":
                category = "INT"
                #Gender
                if msd[3] == "M":
                    features["gender"] = "masc"
                elif msd[3] == "F":
                    features["gender"] = "fem"
                elif msd[3] == "C":
                    features["gender"] = "coed"
                else:
                    features["gender"] = ""
                    self.stdout.write("Error en interrogativo " + flexion + ": " \
                          "gender " + msd[3] + " incorrecto.")
                #Number
                if msd[4] == "S":
                    features["number"] = "sing"
                elif msd[4] == "P":
                    features["number"] = "plur"
                elif msd[4] == "N":
                    features["number"] = "inv"
                else:
                    features["number"] = ""
                    self.stdout.write("Error en interrogativo " + flexion + ": " \
                          "number " + msd[4] + " incorrecto.")
            
            #INTERJECTION
            elif msd == "I":
                category = "INTERJ"
                #No features
            
            #NOUN
            elif msd[0] == "N":
                category = "NOUN"
                #Degree
                if msd[6] == "A":
                    features["noun_degree"] = "aum"
                elif msd[6] == "D":
                    features["noun_degree"] = "dim"
                elif msd[6] == "0":
                    features["noun_degree"] = "reg"
                else:
                    features["noun_degree"] = ""
                    self.stdout.write("Error en sustantivo " + flexion + ": " \
                          "degree " + msd[6] + " incorrecto.")
                #Gender
                if msd[2] == "M":
                    features["gender"] = "masc"
                elif msd[2] == "F":
                    features["gender"] = "fem"
                elif msd[2] == "C":
                    features["gender"] = "coed"
                else:
                    features["gender"] = ""
                    self.stdout.write("Error en sustantivo " + flexion + ": " \
                          "gender " + msd[2] + " incorrecto.")
                #Interpretation
                features["noun_interp"] = ""
                #Number
                if msd[3] == "S":
                    features["number"] = "sing"
                elif msd[3] == "P":
                    features["number"] = "plur"
                elif msd[3] == "N":
                    features["number"] = "inv"
                else:
                    features["number"] = "" #no se da este caso
                    self.stdout.write("Error en sustantivo " + flexion + ": " \
                          "number " + msd[3] + " incorrecto.")
                #Type
                if msd[1] == "C":
                    features["noun_type"] = "comm"
                elif msd[1] == "P":
                    features["noun_type"] = "prop"
                else:
                    features["noun_type"] = ""
                    self.stdout.write("Error en sustantivo " + flexion + ": " \
                          "type " + msd[1] + " incorrecto.")
            
            #POSSESSIVE ADJECTIVE
            elif msd[:2] == "DP":
                category = "POSSADJ"
                #Gender
                if msd[3] == "M":
                    features["gender"] = "masc"
                elif msd[3] == "F":
                    features["gender"] = "fem"
                elif msd[3] == "C":
                    features["gender"] = "coed"
                else:
                    features["gender"] = ""
                    self.stdout.write("Error en adjetivo posesivo " + flexion + ": " \
                          "gender " + msd[3] + " incorrecto.")
                #Number
                if msd[4] == "S":
                    features["number"] = "sing"
                elif msd[4] == "P":
                    features["number"] = "plur"
                else:
                    features["number"] = ""
                    self.stdout.write("Error en adjetivo posesivo " + flexion + ": " \
                          "number " + msd[4] + " incorrecto.")
                #Person
                if msd[2] == "1":
                    features["person"] = "1"
                elif msd[2] == "2":
                    features["person"] = "2"
                elif msd[2] == "3":
                    features["person"] = "3"
                else:
                    features["person"] = ""
                    self.stdout.write("Error en adjetivo posesivo " + flexion + ": " \
                          "person " + msd[2] + " incorrecto.")
            
            #POSSESSIVE PRONOUN
            elif msd[:2] == "PX":
                category = "POSSPRON"
                #Gender
                if msd[3] == "M":
                    features["gender"] = "masc"
                elif msd[3] == "F":
                    features["gender"] = "fem"
                elif msd[3] == "N":
                    features["gender"] = "coed"
                else:
                    features["gender"] = ""
                    self.stdout.write("Error en pronombre posesivo " + flexion + ": " \
                          "gender " + msd[3] + " incorrecto.")
                #Number
                if msd[4] == "S":
                    features["number"] = "sing"
                elif msd[4] == "P":
                    features["number"] = "plur"
                else:
                    features["number"] = ""
                    self.stdout.write("Error en pronombre posesivo " + flexion + ": " \
                          "number " + msd[4] + " incorrecto.")
                #Person
                if msd[2] == "1":
                    features["person"] = "1"
                elif msd[2] == "2":
                    features["person"] = "2"
                elif msd[2] == "3":
                    features["person"] = "3"
                else:
                    features["person"] = ""
                    self.stdout.write("Error en pronombre posesivo " + flexion + ": " \
                          "person " + msd[2] + " incorrecto.")
            
            #PREPOSITION
            elif msd[0] == "S":
                category = "PREP"
                #Form
                if msd[2] == "S":
                    features["prep_form"] = "simp"
                elif msd[2] == "P":
                    features["prep_form"] = "contr"
                else:
                    features["prep_form"] = ""
                    self.stdout.write("Error en preposicion " + flexion + ": " \
                          "form " + msd[2] + " incorrecto.")
            
            #PRONOUN
            elif msd[:2] == "PP":
                category = "PRON"
                #Case
                if self.isPronNom(msd,lemma):
                    features["pron_case"] = "nom"
                elif msd[5] == "A":
                    features["pron_case"] = "acc"
                elif msd[5] == "D":
                    features["pron_case"] = "dat"
                elif msd[5] == "O":
                    features["pron_case"] = "obl"
                elif msd[5] == "0" and not self.isPronNom(msd,lemma):
                    features["pron_case"] = "accydat"
                else:
                    features["case"] = ""
                    self.stdout.write("Error en pronombre personal " + flexion + ": " \
                          "pron_case " + msd[5] + " incorrecto.")
                #Gender
                if msd[3] == "M":
                    features["gender"] = "masc"
                elif msd[3] == "F":
                    features["gender"] = "fem"
                elif msd[3] == "C" or msd[3] == "N":
                    features["gender"] = "coed"
                else:
                    features["gender"] = ""
                    self.stdout.write("Error en pronombre personal " + flexion + ": " \
                          "gender " + msd[3] + " incorrecto.")
                #Number
                if msd[4] == "S":
                    features["number"] = "sing"
                elif msd[4] == "P":
                    features["number"] = "plur"
                elif msd[4] == "N":
                    features["number"] = "inv"
                else:
                    features["number"] = ""
                    self.stdout.write("Error en pronombre personal " + flexion + ": " \
                          "number " + msd[4] + " incorrecto.")
                #Person
                if msd[2] == "1":
                    features["person"] = "1"
                elif msd[2] == "2":
                    features["person"] = "2"
                elif msd[2] == "3":
                    features["person"] = "3"
                elif msd[2] == "0":
                    features["person"] = ""
                else:
                    features["person"] = ""
                    self.stdout.write("Error en pronombre personal " + flexion + ": " \
                          "person " + msd[2] + " incorrecto.")
                #Politeness
                if msd[7] == "0":
                    features["pron_polite"] = "reg"
                elif msd[7] == "P":
                    features["pron_polite"] = "pol"
                else:
                    features["pron_polite"] = ""
                    self.stdout.write("Error en pronombre personal " + flexion + ": " \
                          "pron_polite " + msd[7] + " incorrecto.")
            
            #RELATIVE PRONOUN
            elif msd[:2] == "PR":
                category = "RELPRON"
                #Gender
                if msd[3] == "M":
                    features["gender"] = "masc"
                elif msd[3] == "F":
                    features["gender"] = "fem"
                elif msd[3] == "C":
                    features["gender"] = "coed"
                else:
                    features["gender"] = ""
                    self.stdout.write("Error en pronombre relativo " + flexion + ": " \
                          "gender " + msd[3] + " incorrecto.")
                #Number
                if msd[4] == "S":
                    features["number"] = "sing"
                elif msd[4] == "P":
                    features["number"] = "plur"
                elif msd[4] == "N":
                    features["number"] = "inv"
                else:
                    features["number"] = ""
                    self.stdout.write("Error en pronombre relativo " + flexion + ": " \
                          "number " + msd[4] + " incorrecto.")
            
            #QUANTIFIER
            elif msd[:2] == "AO" or msd[:2] == "DI" and not self.isArtIndef(msd,lemma):
                category = "QUAN"
                #Gender
                if msd[3] == "M":
                    features["gender"] = "masc"
                elif msd[3] == "F":
                    features["gender"] = "fem"
                elif msd[3] == "C":
                    features["gender"] = "coed"
                else:
                    features["gender"] = ""
                    self.stdout.write("Error en cuantificador " + flexion + ": " \
                          "gender " + msd[3] + " incorrecto.")
                #Number
                if msd[4] == "S":
                    features["number"] = "sing"
                elif msd[4] == "P":
                    features["number"] = "plur"
                else:
                    features["number"] = ""
                    self.stdout.write("Error en cuantificador " + flexion + ": " \
                          "number " + msd[4] + " incorrecto.")
                #Type
                if msd[:2] == "AO":
                    features["quan_type"] = "ord"
                else:
                    features["quan_type"] = "indef" #faltan card, mult, part y dist
            
            #VERB
            elif msd[0] == "V":
                category = "VERB"
                #Base
                if self.isVerboCop(msd,lemma):
                    features["verb_base"] = "cop"
                else:
                    features["verb_base"] = "pred"
                #Class
                features["verb_class"] = self.remTildes(lemma[len(lemma)-2:])
                #Conjugation
                features["verb_conj"] = ""
                #Mood
                if msd[2] == "I":
                    features["verb_mood"] = "ind"
                elif msd[2] == "S":
                    features["verb_mood"] = "sub"
                elif msd[2] == "M":
                    features["verb_mood"] = "imp"
                elif msd[2] == "N":
                    features["verb_mood"] = "inf"
                elif msd[2] == "G":
                    features["verb_mood"] = "ger"
                elif msd[2] == "P":
                    features["verb_mood"] = "par"
                else:
                    features["verb_mood"] = ""
                    self.stdout.write("Error en verbo " + flexion + ": " \
                          "mood " + msd[2] + " incorrecto.")
                #Number
                if msd[5] == "S":
                    features["number"] = "sing"
                elif msd[5] == "P":
                    features["number"] = "plur"
                elif msd[5] == "0":
                    features["number"] = ""
                else:
                    features["number"] = ""
                    self.stdout.write("Error en verbo " + flexion + ": " \
                          "number " + msd[5] + " incorrecto.")
                #Person
                if msd[4] == "1":
                    features["person"] = "1"
                elif msd[4] == "2":
                    features["person"] = "2"
                elif msd[4] == "3":
                    features["person"] = "3"
                elif msd[4] == "0":
                    features["person"] = ""
                else:
                    features["person"] = ""
                    self.stdout.write("Error en verbo " + flexion + ": " \
                          "person " + msd[4] + " incorrecto.")
                #Reflexiveness
                features["verb_refl"] = ""
                #Tense
                if msd[3] == "P":
                    features["verb_tense"] = "pres"
                elif msd[3] == "I":
                    features["verb_tense"] = "imperf"
                elif msd[3] == "F":
                    features["verb_tense"] = "fut"
                elif msd[3] == "S":
                    features["verb_tense"] = "pret"
                elif msd[3] == "C":
                    features["verb_tense"] = "cond"
                elif msd[3] == "0":
                    features["verb_tense"] = ""
                else:
                    features["verb_tense"] = ""
                    self.stdout.write("Error en verbo " + flexion + ": " \
                          "tense " + msd[3] + " incorrecto.")
                #Transitivity
                features["verb_trans"] = ""
                #Type
                if self.isVerboAux(msd,lemma):
                    features["verb_type"] = "aux"
                else:
                    features["verb_type"] = "main"

            #OTRO VALOR
            else:
                self.stdout.write("Error, entrada no clasificada: " + line)

            #RESULTADO
            if category == "ADJyVERB":
                #Datos adjetivo
                output["lemma"] = unicode(lemma.decode("latin1"))
                output["flexion"] = unicode(flexion.decode("latin1"))
                output["category"] = "ADJ"
                output["eagle_code"] = msd
                output["msd"] = features
                self.print_entry(json.dumps(output), output_descr)
                
                #Datos verbo
                output["lemma"] = unicode(lemma.decode("latin1"))
                output["flexion"] = unicode(flexion.decode("latin1"))
                output["category"] = "VERB"
                output["eagle_code"] = msd
                output["msd"] = self.getFeaturesVerb(msd, lemma, flexion)
                self.print_entry(json.dumps(output), output_descr)
            else:
                output["lemma"] = unicode(lemma.decode("latin1"))
                output["flexion"] = unicode(flexion.decode("latin1"))
                output["category"] = category
                output["eagle_code"] = msd
                output["msd"] = features
                if category == "PRON" and features["pron_case"] == "accydat":
                    output["msd"]["pron_case"] = "acc"
                    self.print_entry(json.dumps(output), output_descr)
                    output["msd"]["pron_case"] = "dat"
                    self.print_entry(json.dumps(output), output_descr)
                else:
                    self.print_entry(json.dumps(output), output_descr)

            cont += 1
            if cont % 1000 == 0:
                self.stdout.write(u"... %s (%s)\n" \
                                  % (cont, flexion.decode("latin1")))
        file_descr.close()

    def print_entry(self, entry, output_descr):
        if output_descr:
            output_descr.write(entry + u"\n")
        else:
            self.stdout.write(entry + u"\n")

    def isArtIndef(self, msd, lemma):
        if msd[:2] == "DI" and lemma == "uno":
            result = True
        else:
            result = False
        return result

    def isPronPersonal(self, msd):
        if msd[:2] == "PP":
            result = True
        else:
            result = False
        return result

    def isPronNom(self, msd, lemma):
        if self.isPronPersonal(msd) and \
           (lemma == "yo" or \
            unicode(lemma.decode("latin1")) == u"tú" or \
            unicode(lemma.decode("latin1")) == u"él" or \
            lemma == "nosotros" or lemma == "vosotros" or lemma == "ellos"):
            result = True
        else:
            result = False
        return result

    def isVerbo(self, msd):
        if msd[0] == "V":
            result = True
        else:
            result = False
        return result

    def isVerboCop(self, msd, lemma):
        if self.isVerbo(msd) and \
           (lemma == "ser" or lemma == "estar" or lemma == "parecer"):
            result = True
        else:
            result = False
        return result

    def isVerboAux(self, msd, lemma):
        if self.isVerbo(msd) and lemma == "haber":
            result = True
        else:
            result = False
        return result

    def remTildes(self, s):
        result = unicode(s.decode("latin1")). \
                 replace(u"á","a").replace(u"é","e").replace(u"í","i")
        return result

    def getFeaturesVerb(self, msd, lemma, flexion):
        features = {}
        #Base
        if self.isVerboCop(msd, lemma):
            features["verb_base"] = "cop"
        else:
            features["verb_base"] = "pred"
        #Class
        features["verb_class"] = self.remTildes(lemma[len(lemma)-2:])
        #Conjugation
        features["verb_conj"] = ""
        #Mood
        if msd[2] == "I":
            features["verb_mood"] = "ind"
        elif msd[2] == "S":
            features["verb_mood"] = "sub"
        elif msd[2] == "M":
            features["verb_mood"] = "imp"
        elif msd[2] == "N":
            features["verb_mood"] = "inf"
        elif msd[2] == "G":
            features["verb_mood"] = "ger"
        elif msd[2] == "P":
            features["verb_mood"] = "par"
        else:
            features["verb_mood"] = ""
            self.stdout.write("Error en verbo " + flexion + ": " \
                  "mood " + msd[2] + " incorrecto.")
        #Number
        if msd[5] == "S":
            features["number"] = "sing"
        elif msd[5] == "P":
            features["number"] = "plur"
        elif msd[5] == "0":
            features["number"] = ""
        else:
            features["number"] = ""
            self.stdout.write("Error en verbo " + flexion + ": " \
                  "number " + msd[5] + " incorrecto.")
        #Person
        if msd[4] == "1":
            features["person"] = "1"
        elif msd[4] == "2":
            features["person"] = "2"
        elif msd[4] == "3":
            features["person"] = "3"
        elif msd[4] == "0":
            features["person"] = ""
        else:
            features["person"] = ""
            self.stdout.write("Error en verbo " + flexion + ": " \
                  "person " + msd[4] + " incorrecto.")
        #Reflexiveness
        features["verb_refl"] = ""
        #Tense
        if msd[3] == "P":
            features["verb_tense"] = "pres"
        elif msd[3] == "I":
            features["verb_tense"] = "imperf"
        elif msd[3] == "F":
            features["verb_tense"] = "fut"
        elif msd[3] == "S":
            features["verb_tense"] = "pret"
        elif msd[3] == "C":
            features["verb_tense"] = "cond"
        elif msd[3] == "0":
            features["verb_tense"] = ""
        else:
            features["verb_tense"] = ""
            self.stdout.write("Error en verbo " + flexion + ": " \
                  "tense " + msd[3] + " incorrecto.")
        #Transitivity
        features["verb_trans"] = ""
        #Type
        if self.isVerboAux(msd,lemma):
            features["verb_type"] = "aux"
        else:
            features["verb_type"] = "main"
        
        return features
