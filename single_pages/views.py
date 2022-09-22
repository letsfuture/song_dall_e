from django.shortcuts import render
from .forms import ModelForm
from .models import Predictions
from .preprocessing import text_preprocessing
from .summary import KoBART2Image

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
        'single_pages/create.html',
    )

def predict_model(request):
    if request.method == 'POST':
        form = ModelForm(request.POST)
        if form.is_valid():
            lyrics = form.cleaned_data['lyrics']
            result = text_preprocessing(lyrics)
            summary = KoBART2Image(result)
            Predictions.objects.create(lyrics=lyrics,
                                       lyrics_post=result,
                                       summary=summary)

            return render(request, 'single_pages/create.html', {'form': form, 'lyrics': lyrics, 'lyrics_post': result, 'summary': summary})
    else:
        form = ModelForm()

    return render(request, 'single_pages/create.html', {'form': form})
