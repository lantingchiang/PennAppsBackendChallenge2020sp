from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, JsonResponse, Http404
from . import scraper
from .models import Club, Category, CustomUser
from django.views.decorators.csrf import csrf_exempt


# home page
def index(request):
    return render(request, "index.html")


@csrf_exempt # made crsf exempt to test with postman
def view_clubs(request):
    """
    Page for viewing clubs upon GET request and creating/editing club upon POST request
    """
    # send club data as json object upon get request
    if request.method == 'GET':
        clubs = Club.objects.all()
        club_list = []
    
        for c in clubs:
            club_list.append({
                "Club name": c.club_name,
                "Favorite count": c.likers.count()
            })

        return JsonResponse({"Status": 200, "Clubs": club_list})

    elif request.method == 'POST':
        # call helper function to create/edit club
        create_club(request)
        return redirect('/')

    else:
        return JsonResponse({"Status": 405, "Error": "Only POST and GET requests allowed."}, status=405)


def create_club(request):
    """
    Creates new Club instance or updates fields of existing Club instance with information obtained from form
    """
    club_name = request.POST.get('club_name')
    description = request.POST.get('description')
    tag1 = request.POST.get('tag1')
    tag2 = request.POST.get('tag2')
    tag3 = request.POST.get('tag3')
    tags = []
    # add tag to array if it isn't empty string
    if tag1:
        tags.append(tag1)
        if tag2: 
            tags.append(tag2)
            if tag3:
                tags.append(tag3)

    club = Club.objects.filter(club_name=club_name) 

    # update club information if club already exists
    if club.exists():
        c = club[0]
        c.club_name = club_name
        c.description = description
        c.save(force_update=True)
    else :
        Club(club_name=club_name, description=description).save()
    # store new tags and establish M2M relationships            
    scraper.store_tags(tags, Club.objects.filter(club_name=club_name)[0])

def api_user(request, username):
    """
    Queries the db with captured username from url and sends user info
    as json object
    """
    if request.method == 'GET':
        try:
            user = get_object_or_404(CustomUser, username=username)
            user_dict = {
                "username": user.username,
                "registered email": user.email,
            }
        except Http404:
            raise Http404("No such user")
        return JsonResponse(user_dict)

    else:
        return JsonResponse({"Status": 405, "Error": "Only POST requests allowed."}, status=405)

@csrf_exempt
def api_favorite(request):
    """
    Allos users to favorite a Club instance
    """
    if request.method == 'POST':
        try:
            user = get_object_or_404(CustomUser, username=request.POST.get("username"))
        except Http404:
            raise Http404("No such user")
        try:
            club = get_object_or_404(Club, club_name=request.POST.get('club_name'))
        except Http404:
            raise Http404("No such club")
        
        club.likers.add(user)
        club.save()
        return redirect('/')
    else:
        return JsonResponse({"Status": 405, "Error": "Only POST requests allowed."}, status=405)

@csrf_exempt
def api_comment(request):
    """
    This function handles POST requests from users posting comments for a club
    """
    if request.method == 'POST':
        club_name = request.POST.get('club_name')
        author = request.POST.get('author')
        comment = request.POST.get('comment')
        date = request.POST.get('date')

        try:
            target_club = get_object_or_404(Club, club_name=club_name)
        except Http404:
            raise Http404("No such club")

        new_comment = Comment(club=target_club, post_by=author, comment=comment, date=date)
        new_comment.save()
            
        return redirect('/')
    else:
        return JsonResponse({"Status": 405, "Error": "Only POST requests allowed."}, status=405)




