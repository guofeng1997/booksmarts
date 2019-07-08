from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm


# Create your views here.
@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            messages.success(request, '图片添加成功！')
            # return redirect(new_item.get_absolte_url())
            return HttpResponse('OK')
        else:
            print("验证没有通过！！！")
            print(form.errors)
    else:
        form = ImageCreateForm(data=request.GET)
        return render(request, 'images/image/create.html', {'section': 'images', 'form': form})
