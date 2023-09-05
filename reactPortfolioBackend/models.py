from django.db import models

# Create your models here.

class Categories(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self) -> str:
        return self.name


class landingPageData(models.Model) :
    picture = models.ImageField(upload_to="static")
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    price  = models.IntegerField()
    category = models.ForeignKey(Categories, on_delete = models.CASCADE)

    def __str__(self)-> str:
        return self.title