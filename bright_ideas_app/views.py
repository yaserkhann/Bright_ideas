from django.shortcuts import render, HttpResponse, redirect
from . models import*
from django.contrib import messages
from django.db.models import Count


def index(request):
    return render(request, 'main.html')


def ideas(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    posts = Idea.objects.annotate(like_count=Count(
        'user_likes')).order_by('-like_count')
    context = {
        'ideas': posts,
        'user': user
    }
    return render(request, 'idea.html', context)

# registering a user


def register(request):
    if request.method == 'GET':
        return redirect('/')
    errors = User.objects.validate(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect('/')
    else:
        new_user = User.objects.register(request.POST)
        request.session['user_id'] = new_user.id
        messages.success(request, "You have successfully registered!")
        return redirect('/bright_ideas')

# log in existing user


def login(request):
    if request.method == "GET":
        return redirect('/')
    if not User.objects.authenticate(request.POST['email'], request.POST['password']):
        messages.error(request, 'Invalid Email/Password')
        return redirect('/')
    user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = user.id
    # messages.success(request, "You have successfully logged in!")
    return redirect('/bright_ideas')


def logout(request):
    request.session.flush()
    messages.success(request, 'you are successfully logout')
    return redirect('/')


def post_idea(request):
    if request.method == "GET":
        return redirect('/')
    poster = User.objects.get(id=request.session['user_id'])
    post = request.POST['idea']
    new_idea = Idea.objects.create(post=post, poster=poster)
    print(new_idea.post)
    return redirect('/bright_ideas')


def add_like(request, idea_id):
    user = User.objects.get(id=request.session['user_id'])
    idea = Idea.objects.get(id=idea_id)
    idea.user_likes.add(user)
    return redirect('/bright_ideas')


def detail(request, idea_id):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'idea': Idea.objects.get(id=idea_id)
    }
    return render(request, 'post.html', context)


def user_detail(request, user_id):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id=user_id)
    }
    return render(request, 'user.html', context)


def delete(request, idea_id):
    idea_to_delete = Idea.objects.get(id=idea_id)
    idea_to_delete.delete()
    return redirect('/bright_ideas')


def edit(request, idea_id):
    if 'user_id' not in request.session:
        return redirect('/')
    idea = Idea.objects.get(id=idea_id)
    user = idea.poster
    context = {
        'idea': Idea.objects.get(id=idea_id),
        'user': idea.poster
    }
    return render(request, 'edit.html', context)


def update_idea(request, idea_id):
    idea_to_update = Idea.objects.get(id=idea_id)
    print(idea_to_update.post)
    idea_to_update.post = request.POST['idea']
    idea_to_update.save()
    return redirect('/bright_ideas')


def update_user(request, user_id):
    user_to_update = User.objects.get(id=user_id)
    if request.method == 'GET':
        return redirect('/')
    errors = User.objects.validate_update(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect(f'/edit/{user_id}')
    user_to_update.name = request.POST['name']
    user_to_update.alias = request.POST['alias']
    user_to_update.save()
    return redirect('/bright_ideas')
