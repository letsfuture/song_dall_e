from django.shortcuts import render

def landing(request):
    return render(
        request,
        'single_pages/landing.html'
    )

def about_us(request):
    return render(
        request,
        'single_pages/about_us.html'
    )

def how_to_use(request):
    return render(
        request,
        'single_pages/how_to_use.html'
    )

def create(request):
    return render(
        request,
        'single_pages/create.html'
    )