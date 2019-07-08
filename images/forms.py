from urllib import request

from django import forms
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
        print("url:", url)
        vaild_extensions = ['jpg', 'jpeg']
        extension = url.rsplit('.', 1)[1].lower()
        print("extension:", extension)
        if extension not in vaild_extensions:
            raise forms.ValidationError('The given URL does not match vaild image extension.')
        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        image = super(ImageCreateForm, self).save(commit=False)
        image_url = self.cleaned_data['url']
        print('oring_url:', image_url)
        image_name = '{}.{}'.format(slugify(image.title), image_url.rsplit('.', 1)[1].lower())

        # 根据url下载图片
        print("image_url:", image_url)
        res = request.urlopen(image_url)
        content = res.read()
        print("response:", res)
        image.image.save(image_name, content, save=False)

        if commit:
            image.save()
        return image
