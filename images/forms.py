from urllib import request

rom django import forms
from .models import Image
from django.utils.text import slugify


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')
        widgets = {
            'url': forms.HiddenInput,
        }

    def clean_url(self):
        url = self.cleaned_data['url']
        vaild_extensions = ['jpg', 'jpeg']
        extension = url.rsplit('.', 1)[-1].lower()
        if extension not in vaild_extensions:
            raise forms.ValidationError('The given URL does not match vaild image extension.')
        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        image = super(ImageCreateForm).save(commit=False)
        image_url = self.cleaned_data['url']
        image_name = '{}.{}'.format(slugify(image.title), image_url.rsplit('.', 1)[1])

        # 根据url下载图片
        res = request.urlopen(image_url)
        image.image.save()
