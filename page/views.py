from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Club, Category, Leader, Review, Student
from .forms import PostForm, LoginForm, EditForm, InterviewForm
from django.db import models
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from . import CASClient
from django.urls import reverse
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required
import json


def post_list(request):
    return render(request, 'page/splash-page.html')

@login_required(login_url='/login/')
def post_detail(request, pk):
    club = get_object_or_404(Club, pk=pk)
    reviews = club.review_set.all()
    interviews = club.interview_set.all()
    
    accept = False
    email = club.email.split('@')
    if request.user.student.netid == email[0]:
        accept = True
    else:
        leaders = club.leader_set.all()
        for leader in leaders:
            emailL = leader.email.split('@')
            if request.user.student.netid == emailL[0]:
                accept = True

    review1 = None
    review2 = None
    if reviews.count() > 1:
        review1 = reviews[reviews.count()-1]
        review2 = reviews[reviews.count()-2]
    elif reviews.count() == 1:
        review1 = reviews[0]

    interview1 = None
    interview2 = None
    if interviews.count() > 1:
        interview1 = interviews[interviews.count()-1]
        interview2 = interviews[interviews.count()-2]
    elif interviews.count() == 1:
        interview1 = interviews[0]

    review_count = reviews.count()
    star_result = 0
    if (review_count != 0):
        star_result = club.total_stars;

    if (review_count):
        if ((club.fun_count / review_count) >= .5):
            happy_result = 1
        elif ((club.fun_count / review_count) < .5):
            happy_result = 0
    else:
        happy_result = 0

    if (review_count):
        if ((club.meaning_count / review_count) >= .5):
            mean_result = 1
        elif ((club.meaning_count / review_count) < .5):
            mean_result = 0
    else:
        mean_result = 0

    interview_count = interviews.count()
    if (interview_count):
        if ((club.positive_count / interview_count) >= .5):
            positive_result = 1
        elif ((club.positive_count / interview_count) < .5):
            positive_result = 0
    else:
        positive_result = 0

    if (interview_count):
        if ((club.hard_count / interview_count) >= .5):
            hard_result = 1
        elif ((club.hard_count / interview_count) < .5):
            hard_result = 0
    else:
       hard_result = 0


    photo_count = 0
    photo1 = None
    photo2 = None
    photo3 = None
    if club.photo1:
        photo_count += 1
        photo1 = club.photo1
        if club.photo2:
            photo_count += 1
            photo2 = club.photo2
            if club.photo3:
                photo_count += 1
                photo3 = club.photo3
        else:
            if club.photo3:
                photo_count += 1
                photo2 = club.photo3
    elif club.photo2:
        photo_count += 1
        photo1 = club.photo2
        if club.photo3:
            photo_count += 1
            photo2 = club.photo3
    else:
        if club.photo3:
            photo_count += 1
            photo1 = club.photo3

    if club in request.user.student.clubs_interested.all():
        interest = True
    else:
        interest = False

    return render(request, 'page/post_detail2.html', {'club': club, 'review_count': review_count, 
        'fun_count': club.fun_count, 'mean_count': club.meaning_count, 'happy_result': happy_result, 
        'mean_result': mean_result, 'star_count': star_result, 
        'count':photo_count, 'photo1':photo1, 'photo2':photo2, 'photo3':photo3, 
        'review1':review1, 'review2': review2, 'positive_result':positive_result,
        'hard_result':hard_result, 'interview1':interview1, 'interview2':interview2, 'accept':accept, 'interest':interest})

@login_required(login_url='/login')
def express_interest(request, pk):
    club = get_object_or_404(Club, pk=pk)
    if club in request.user.student.clubs_interested.all():
        request.user.student.clubs_interested.remove(club)
        express = 0
    else:
        request.user.student.clubs_interested.add(club)
        express = 1
    data = json.dumps(express)
    return HttpResponse(data, content_type='application/json')

@login_required(login_url='/login/')
def top20(request):
    clubs = Club.objects.all()
    clubs = clubs.order_by('-total_stars', 'name')[:20]
    return render(request, 'page/top20.html', {'clubs': clubs})

@login_required(login_url='/login/')
def all_reviews(request, pk):
    #if request.user.student.clubs_reviewed.count() == 0 and request.user.student.club_interviews_reviewed.count() == 0:
    #    messages.info(request, "You must review just one club or interview experience before you can have access to the all reviews page!")
    #    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    time = 0
    club = get_object_or_404(Club, pk=pk)

    reviews = club.review_set.all()
    review_count = reviews.count()

    if (review_count):
        if ((club.fun_count / review_count) >= .5):
            happy_result = 1
        elif ((club.fun_count / review_count) < .5):
            happy_result = 0
    else:
        happy_result = 0

    if (review_count):
        if ((club.meaning_count / review_count) >= .5):
            mean_result = 1
        elif ((club.meaning_count / review_count) < .5):
            mean_result = 0
    else:
        mean_result = 0

    reviews.time = reviews.order_by('-created_at')
    reviews.rating = reviews.order_by('-rating')

    if 'sort' in request.GET:
        sort = request.GET['sort']
        if sort == "1":
            time = 1
            return render(request, 'page/all_reviews.html', {'club': club, 'review_count': review_count, 
                'fun_count': club.fun_count, 'mean_count': club.meaning_count,
                'happy_result': happy_result, 'mean_result': mean_result, 
                'reviews' : reviews.time, 'time' : time})

        elif sort == "2":
            time = 2
            return render(request, 'page/all_reviews.html', {'club': club, 'review_count': review_count, 
                'fun_count': club.fun_count, 'mean_count': club.meaning_count, 'happy_result': happy_result, 
                'mean_result': mean_result, 'reviews' : reviews.rating, 
                'time' : time})

    else:
        return render(request, 'page/all_reviews.html', {'club': club, 'review_count': review_count, 'fun_count': club.fun_count, 'mean_count': club.meaning_count, 'happy_result': happy_result, 'mean_result': mean_result, 'reviews' : reviews.time, 'time' : time})
    return render(request, 'page/all_reviews.html', {'club': club, 'reviews': reviews})

@login_required(login_url='/login/')
def all_interviews(request, pk):
    #if request.user.student.clubs_reviewed.count() == 0 and request.user.student.club_interviews_reviewed.count() == 0:
    #    messages.info(request, "You must review just one club or interview experience before you can have access to this page!")
    #    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    club = get_object_or_404(Club, pk=pk)

    interviews = club.interview_set.all()
    interview_count = interviews.count()

    if (interview_count):
        if ((club.positive_count / interview_count) >= .5):
            positive_result = 1
        elif ((club.positive_count / interview_count) < .5):
            positive_result = 0
    else:
        positive_result = 0

    if (interview_count):
        if ((club.hard_count / interview_count) >= .5):
            hard_result = 1
        elif ((club.hard_count / interview_count) < .5):
            hard_result = 0
    else:
        hard_result = 0

    return render(request, 'page/all_interviews.html', {'club': club, 'interview_count': interview_count,
        'positive_count': club.positive_count, 'hard_count': interview_count - club.hard_count,
        'positive_result': positive_result, 'hard_result': hard_result, 
        'interviews' : interviews})

@login_required(login_url='/login/')
def post_list_full(request, num):
    count = 75 * int(num);
    clubs = Club.objects.all()

    if (clubs.count() <= (count+75)):
        clubs = clubs.order_by('name')[count:]
    else:
        clubs = clubs.order_by('name')[count:count+75]

    notFirst = 1;
    notLast = 1;
    if num == 0:
        notFirst = 0;
    elif num == 4:
        notLast = 0;

    numPrev = int(num)-1;
    numNext = int(num)+1;
    if numPrev < 0:
        numPrev = 0;
        notFirst = 0;
    elif numNext > 4:
        notLast = 0;

    return render(request, 'page/post_list_full.html', {'clubs': clubs, 'num': num,
        'numPrev': numPrev, 'numNext': numNext, 'notFirst': notFirst, 'notLast': notLast},)

@login_required(login_url='/login/')
def my_clubs(request):
    email = request.user.student.netid + "@princeton.edu"
    clubs = Club.objects.filter(email=email).distinct() | Club.objects.filter(leader__email=email).distinct()
    clubs_interested = request.user.student.clubs_interested.all()
    return render(request, 'page/my_clubs.html', {'clubs': clubs, 'clubs_interested':clubs_interested, 'count': clubs.count()})

@login_required(login_url='/login/')
def review_increment(request, pk_Club, pk_Review):
    review = get_object_or_404(Review, pk=pk_Review)
    if request.user.student.review_upvotes.filter(pk=review.pk):
        review.rating -=1
        request.user.student.review_upvotes.remove(review)
    else:
        review.rating += 1
        if request.user.student.review_downvotes.filter(pk=review.pk):
            review.rating += 1
            request.user.student.review_downvotes.remove(review)
        request.user.student.review_upvotes.add(review)
    review.save()
    request.user.student.save()
    data = json.dumps(review.rating)
    return HttpResponse(data, content_type='application/json')

@login_required(login_url='/login/')
def review_decrement(request, pk_Club, pk_Review):
    review = get_object_or_404(Review, pk=pk_Review)
    if request.user.student.review_downvotes.filter(pk=review.pk):
        review.rating += 1
        request.user.student.review_downvotes.remove(review)
    else:
        review.rating -= 1
        if request.user.student.review_upvotes.filter(pk=review.pk):
            review.rating -= 1
            request.user.student.review_upvotes.remove(review)
        request.user.student.review_downvotes.add(review)
    review.save()
    request.user.student.save()
    data = json.dumps(review.rating)
    return HttpResponse(data, content_type='application/json')

@login_required(login_url='/login/')
def post_new(request, pk):
    if request.user.student.clubs_reviewed.filter(pk=pk):
        messages.info(request, 'You cannot review a club twice!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                club = get_object_or_404(Club, pk=pk)
                review = form.save(commit=False)
                review.student = request.user.student
                review.club = club
                club.fun_count += review.fun
                club.meaning_count += review.meaningful
                review_count = club.review_set.count()
                if review_count != 0:
                    club.total_stars = club.total_stars * review_count
                    club.total_stars += review.stars
                    club.total_stars = club.total_stars / (review_count+1)
                else: 
                    club.total_stars = review.stars
                review.save()
                club.save()
                request.user.student.clubs_reviewed.add(club)
                request.user.student.save()
                return redirect('post_detail', pk=pk)
        else:
            form = PostForm()
            club = get_object_or_404(Club, pk=pk)
        return render(request, 'page/post_edit.html', {'form': form, 'user': request.user, 'club': club})

@login_required(login_url='/login/')
def interview_new(request, pk):
    if request.user.student.club_interviews_reviewed.filter(pk=pk):
        messages.info(request, "You already wrote about your interview experience with this club!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        if request.method == "POST":
            form = InterviewForm(request.POST)
            if form.is_valid():
                club = get_object_or_404(Club, pk=pk)
                interview = form.save(commit=False)
                interview.student = request.user.student
                interview.club = club
                club.positive_count += interview.positive
                club.hard_count += interview.hard
                interview.save()
                club.save()
                request.user.student.club_interviews_reviewed.add(club)
                request.user.student.save()
                return redirect('post_detail', pk=pk)
        else:
            form = InterviewForm()
            club = get_object_or_404(Club, pk=pk)
        return render(request, 'page/interview_edit.html', {'form': form, 'user': request.user, 'club': club})


@login_required(login_url='/login/')
def edit_page(request, pk):
    club = get_object_or_404(Club, pk=pk)
    LeaderInlineFormSet = inlineformset_factory(Club, Leader, fields=('name','title','email'), min_num=1)
    email = club.email.split('@')
    if not request.user.student.netid == email[0]:
        leaders = club.leader_set.all()
        accept = False
        for leader in leaders:
            emailL = leader.email.split('@')
            if request.user.student.netid == emailL[0]:
                accept = True
        if accept == False:
            messages.info(request, 'You cannot edit a club other than your own!')
            return HttpResponseRedirect(reverse('post_detail', args=[pk]))
    if request.method == "POST":
        form = EditForm(request.POST, request.FILES, instance=club)
        formset = LeaderInlineFormSet(request.POST, request.FILES, instance=club)
        if form.is_valid() and formset.is_valid():
            if request.FILES.get('photo1') != None:
                club.photo1 = request.FILES.get('photo1')
                club.save()
            elif request.POST.get('delete1'):
                club.photo1.delete()
            if request.FILES.get('photo2') != None:
                club.photo2 = request.FILES.get('photo2')
                club.save()
            elif request.POST.get('delete2'):
                club.photo2.delete()
            if request.FILES.get('photo3') != None:
                club.photo3 = request.FILES.get('photo3')
                club.save()
            elif request.POST.get('delete3'):
                club.photo3.delete()
            form.save()
            formset.save()
            return redirect('post_detail', pk=pk)
    else:
        form = EditForm({'name': club.name, 'desc': club.desc, 'website': club.website, 'email': club.email})
        formset = LeaderInlineFormSet(instance=club) 
    return render(request, 'page/club_edit.html', {'form': form, 'formset':formset, 'user': request.user, 'club': club})

@login_required(login_url='/login/')
def review_detail(request, pk):
    review = get_object_or_404(Review, pk=pk)
    return render(request, 'page/review_detail.html', {'review': review})

@login_required(login_url='/login/')
def interest_page(request, pk):
    club = get_object_or_404(Club, pk=pk)
    email = club.email.split('@')
    if not request.user.student.netid == email[0]:
        leaders = club.leader_set.all()
        accept = False
        for leader in leaders:
            emailL = leader.email.split('@')
            if request.user.student.netid == emailL[0]:
                accept = True
        if accept == False:
            messages.info(request, 'You cannot access the information of a club that is not your own!')
            return HttpResponseRedirect(reverse('post_detail', args=[pk]))
    students = Student.objects.filter(clubs_interested__id=pk)
    return render(request, 'page/interest.html', {'students': students, 'club':club})       


@login_required(login_url='/login/')
def search(request):
    if 'q' in request.GET:
        q = request.GET['q']
        type = request.GET['type']

        if len(q) > 50:
            messages.info(request, "Your search query is too long!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


        elif q == "" and type == "%":
            return post_list_full(request, 0)

        elif type == "%":
            if not q:
                clubs = Club.objects.all()
            else:
                q2 = q.split(' ')
                clubs = Club.objects.filter(name__icontains=q2[0]) | Club.objects.filter(desc__icontains=q2[0])
                for i in range(1, len(q2)):
                    clubs = clubs.filter(name__icontains=q2[i]) | clubs.filter(desc__icontains=q2[i])
        else:
            clubs = Club.objects.filter(category__id=type)
            q2 = q.split(' ')
            clubs = clubs.filter(name__icontains=q2[0]) | clubs.filter(desc__icontains=q2[0])
            for i in range(1, len(q2)):
                clubs = clubs.filter(name__icontains=q2[i]) | clubs.filter(desc__icontains=q2[i])



    return render(request, 'page/search_results.html', {'clubs': clubs, 'query': q})

def logintemp(request):
    C = CASClient.CASClient(request)
    auth_attempt = C.Authenticate()
    if "netid" in auth_attempt:
        netid = auth_attempt["netid"]
        request.session["netid"] = netid
        username = netid
        password = netid
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            # User has already logged in before
            auth.login(request, user)
            return redirect(request.GET['next']) 
        else:
            # first time loggin in - create a user
            user = User.objects.create_user(username=username, password=password)
            email = netid + "@princeton.edu"
            student = Student(user=user, netid=netid)
            student.save()
            auth.login(request, user)
            return redirect(request.GET['next'])
    elif "location" in auth_attempt:
        return redirect(auth_attempt["location"])
    else:
        abort(500)

def about_us(request):
    return render(request, 'page/about_us.html')

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            netid = form.cleaned_data['username']
            username = netid
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                # User has already logged in before
                auth.login(request, user)
                return redirect(request.GET['next'])
            else:
                # first time loggin in - create a user
                user = User.objects.create_user(username=username, password=password)
                email = netid + "@princeton.edu"
                student = Student(user=user, netid=netid)
                student.save()
                auth.login(request, user)
                return redirect(request.GET['next'])
    else:
        form = LoginForm()
    return render(request, 'page/logintemp.html', {'form': form}) 


def logout(request):
    auth.logout(request)
    return redirect('/')
    # return redirect('https://fed.princeton.edu/cas/logout?url=http://clubtalk.herokuapp.com/')

def handler404(request, exception):
    return render(request, 'page/404.html', status=404)

def handler500(request, excpetion):
    return render(request, 'page/500.html', status=500)