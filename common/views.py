from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Create your views here.
def main_page(request):
    return render(request, '../templates/common/index.html')


@login_required()
def profile(request):
    return render(request, 'accounts/profile.html')


def siteMap(request):
    return render(request, '../templates/common/siteMap.html')


def contactUs(request):
    return render(request, '../templates/common/contactUs.html')


def privacyPolicy(request):
    return render(request, '../templates/common/privacyPolicy.html')
