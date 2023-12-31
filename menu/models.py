from django.db import models
from django.urls import reverse

class BaseAbstractModel(models.Model):

    is_visible = models.BooleanField(default=True,verbose_name='Visibility')
    order = models.IntegerField(default=10,verbose_name='Order')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


    class Meta:
        abstract = True



class Menu(BaseAbstractModel):

    title = models.CharField(max_length=25,verbose_name='Menu Title')
    slug = models.SlugField(max_length=250,verbose_name='Slug',null=True,
                            help_text='Use it in template tag for displaying menu')
    named_url = models.CharField(max_length=250,verbose_name='Named URL',blank=True,
                                 help_text='Named Url from your urls.py file')

    class Meta:
        verbose_name = 'menu'
        verbose_name_plural = 'menu'

    def __str__(self):
        return self.title

    def get_full_path(self):
        if self.named_url:
            url = reverse(self.named_url)
        else:
            url = '/{}/'.format(self.slug)
        return url


class MenuItem(BaseAbstractModel):


    menu = models.ForeignKey(Menu,related_name='items',
                            verbose_name='menu',blank=True,null=True,
                             on_delete=models.CASCADE)
    parent = models.ForeignKey('self',blank=True,null = True,
                               related_name='items',
                               verbose_name='parent menu item',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=100,verbose_name='Item Title')
    url = models.CharField(max_length=250,verbose_name='Link',blank=True)
    named_url = models.CharField(max_length=250,verbose_name='Named URL',blank=True,help_text='Named url from your urls.py file')

    class Meta:

        verbose_name = 'menu item'
        verbose_name_plural = 'menu items'
        ordering = ('order',)

    def get_url(self):
        if self.named_url:
            url = reverse(self.named_url)
        elif self.url:
            url = self.url
        else:
            url = '/'
        return url

    def __str__(self):
        return self.title
