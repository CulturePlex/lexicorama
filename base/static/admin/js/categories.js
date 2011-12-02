(function($) {

    var fields = ['gender', 'number', 'person', 'adj_degree', 'adv_meaning',
                  'adj_interpretation', 'art_type', 'conj_type', 'noun_degree',
                  'noun_interpretation', 'noun_type', 'prep_form',
                  'pron_type', 'quan_type', 'verb_base', 'verb_conjugation',
                  'verb_mood', 'verb_reflexiveness', 'verb_tense', 'verb_class',
                  'verb_transitivity', 'verb_type'];
    var categories = {
        "adj": ['adj_degree', 'adj_interpretation', 'gender', 'number'],
        "adv": ['adv_meaning'],
        "art": ['art_type', 'gender', 'number'],
        "demadj": ['gender', 'number'],
        "dempron": ['gender', 'number'],
        "excl": ['gender', 'number'],
        "int": ['gender', 'number'],
        "conj": ['conj_type'],
        "noun": ['noun_degree', 'noun_interpretation', 'noun_type', 'gender',
                 'number'],
        "possadj": ['gender', 'number', 'person'],
        "posspron": ['gender', 'number', 'person'],
        "prep": ['prep_form'],
        "pron": ['pron_type', 'gender', 'number', 'person'],
        "quan": ['quan_type'],
        "verb": ['verb_base', 'verb_conjugation', 'verb_mood',
                 'verb_reflexiveness', 'verb_tense', 'verb_transitivity',
                 'verb_type', 'verb_class', 'number', 'person']
     }

    init = function() {
        $("#id_category").change(function(e) {
            var selected = $(this).val();
            for(var i in fields) {
                field = fields[i];
                if (selected && categories[selected].indexOf(field) >= 0) {
                    $("div."+ field).show();
                } else {
                    $("div."+ field).hide();
                }
            }
        });
        $("#id_category").change();
    }

    $(document).ready(init);
})(django.jQuery);


