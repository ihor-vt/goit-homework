from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Author(models.Model):
    fullname = models.CharField(max_length=50, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'fullname'], name='unique fullname')
        ]

    def __str__(self):
        return f"{self.fullname}:"


class Tag(models.Model):
    tag = models.CharField(max_length=50, null=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['tag'], name='unique tag')
        ]

    def __str__(self):
        return f"{self.tag}:"


class Quote(models.Model):
    description = models.CharField(max_length=5000, null=False)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, default=1)
    tag = models.ManyToManyField(Tag, through='QuoteTag')

    def __str__(self):
        return f"{self.description}:"


class QuoteTag(models.Model):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        db_table = 'quote_tag'


class AuthorDetail(models.Model):
    user = models.OneToOneField(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.fullname
