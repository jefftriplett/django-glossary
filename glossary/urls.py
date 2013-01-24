from django.conf.urls.defaults import *
from .views import TermDetailView, term_list


urlpatterns = patterns('',
    url(regex=r'^$',
        view=term_list,
        name="glossary-list"),
    url(regex='^(?P<slug>[-\w]+)/$',
        view=TermDetailView.as_view(),
        name='glossary-detail'),
)
