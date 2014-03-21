#encoding: utf-8

import string

from django.db.models import Q

from django.views.generic.list_detail import object_list
from django.db import connection, transaction
from glossary.models import Term
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

class TermDetailView(DetailView):
    model = Term


def term_list(request, **kwargs):
    """
    Return a list of all terms

    """

    ec = {"a_z": string.uppercase + u"АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ"}

    terms = Term.objects.all()

    if "q" in request.GET:
        query = request.GET['q']
        ec['query'] = query
        terms = terms.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(synonyms__title__icontains=query)
        ).distinct()
        try:
            ec['starts_with'] = ec['query'][0]
        except IndexError:
            ec['starts_with'] = ''
    else:
        initial = request.GET.get("l", "a").lower()
        ec['starts_with'] = initial
        terms = terms.filter(title__istartswith=ec['starts_with'])

        used_letters = list(set(Term.objects.distinct().extra(
            select={'f_letter': "lower(substr(title,1,1))"}
        ).values_list('f_letter', flat=True)))

    return object_list(request,
                       queryset=terms,
                       extra_context={'ec': ec,
                                      'starts_with': ec['starts_with'],
                                      'a_z': ec['a_z'],
                                      'used_letters': used_letters},
                       **kwargs)
