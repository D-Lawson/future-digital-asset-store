from django.db import models


class Category(models.Model):
    """
    Model for Category
    """
    class Meta:
        """ Meta class for category model """
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    display_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    def get_display_name(self):
        return self.display_name


class Asset(models.Model):
    """
    Model for Asset
    """
    category = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    popularity = models.DecimalField(
        max_digits=6, decimal_places=0, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    print_sizes = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    def increment_popularity(self):
        """
        Update the popularity
        """
        self.popularity = self.popularity + 1
        self.save()
