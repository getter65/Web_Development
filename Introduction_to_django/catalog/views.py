from django.shortcuts import render


def home(request):
    return render(request, 'catalog/home.html')


def contacts(request):

    if request.method == 'POST':
        for_feature_table = {
            'name': request.POST.get('name'),
            'phone': request.POST.get('phone'),
            'message': request.POST.get('message')
        }
        print(for_feature_table)
    return render(request, 'catalog/contacts.html')
