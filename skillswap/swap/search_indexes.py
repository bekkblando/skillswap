from datetime import datetime
from haystack import indexes
from .models import Skill


class SkillIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Skill

    def index_queryset(self, using=None):
        return self.get_model().objects.filter()