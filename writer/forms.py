from django.forms import ModelForm

from . models import Article
from account.models import CustomUser


class ArticleForm(ModelForm):

    class Meta:
        model = Article
        fields = ['title', 'content', 'is_premium']
