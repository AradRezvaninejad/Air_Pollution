from modeltranslation.translator import register, TranslationOptions
from .models import EducationCard, Article


@register(EducationCard)
class EducationCardTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(Article)
class ArticleTranslationOptions(TranslationOptions):
    fields = ('title', 'summary')