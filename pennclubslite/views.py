from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from . import scraper
from django.http import JsonResponse
from django.core import serializers
from .models import Club, Category, CustomUser


# home page
def main(request):
    return HttpResponse("Welcome to Penn Club Review!")

def api(request):
    return HttpResponse("Welcome to the Penn Club Review API!")

def api_clubs(request):
    # send club data as json object upon get request
    if request.method == 'GET':
        #scraper.store_clubs()
        clubs = Club.objects.all()
        clubs_json = serializers.serialize('json', clubs)
        return JsonResponse(clubs_json, safe=False)
    elif reqest.method == 'POST':
        return HttpResponse('post_api_clubs')
    
    return HttpResponse("Welcome to the Penn Club Review API!.")

def api_user(request, username):
    return HttpResponse("not implemented yet")

def api_favorite(request):
    return HttpResponse("not implemented yet")

