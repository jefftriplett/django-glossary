from django.db import models
from django.core.urlresolvers import reverse

class Term(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    class Meta:
        ordering = ['title']

    def get_absolute_url(self):
        name = "glossary-detail"
        kwargs = {
            "slug": self.slug,
        }

        return reverse(name, kwargs=kwargs)


    def __unicode__(self):
        return unicode(self.title)


class Synonym(models.Model):
    title = models.CharField(max_length=250)
    term = models.ForeignKey(Term, related_name="synonyms")

    def __unicode__(self):
        return u"%s (synonym for %s)" % (self.title, self.term.title)
