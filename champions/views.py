from django.shortcuts import render

def get_champion(request):
	return render(request, 'champions/champion.html')