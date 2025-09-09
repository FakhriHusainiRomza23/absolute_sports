from django.shortcuts import render

def show_main(request):
    context = {
        'npm' : '2406436972',
        'name': 'Fakhri Husaini Romza',
        'class': 'PBP B'
    }

    return render(request, "main.html", context)

# Create your views here.
