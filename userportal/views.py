from django.contrib.auth import logout
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Team, Post, Comment
from django.db.models import Q
from django.http import JsonResponse
from .ai_utils import summarize_text, get_combined_text
from django.db import models


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    teams = Team.objects.all()   
    return render(request, 'userportal/home.html', {'teams': teams})

@login_required
def create_team(request):
    if request.method == "POST":
        team_name = request.POST.get('team_name')

        if not team_name:
            messages.error(request, "Team name cannot be empty!")
            return redirect('home')

        if Team.objects.filter(team_name__iexact=team_name).exists():
            messages.error(request, "Team already exists!")
            return redirect('home')

        team = Team.objects.create(
            team_name=team_name,
            creator=request.user
        )

        team.members.add(request.user)

        messages.success(request, "Team created successfully!")
        return redirect('home')

    return redirect('home')

@login_required
def team_detail(request, team_id):
    team = Team.objects.get(team_id=team_id)

    query = request.GET.get('search')

    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        pdf = request.FILES.get("pdf")

        post = Post.objects.create(
            team=team,
            user=request.user,
            title=title,
            content=content,
            pdf=pdf
        )

        combined_text = get_combined_text(
            content,
            post.pdf.path if post.pdf else None
        )

        combined_text = combined_text[:5000]

        if combined_text.strip():
            post.summary = summarize_text(combined_text)
            post.save()

        return redirect('team_detail', team_id=team_id)

    matched_posts = []

    if query:
        matched_posts = Post.objects.filter(
            team=team
        ).filter(
            Q(title__icontains=query) |
            Q(user__username__icontains=query)
        )

    # posts = Post.objects.filter(team=team).order_by('-created_at')

    sort = request.GET.get('sort')

    if sort == "likes":
        posts = Post.objects.filter(team=team).annotate(
            like_count=models.Count('likes')
        ).order_by('-like_count', '-created_at')
    else:
        posts = Post.objects.filter(team=team).order_by('-created_at')

    is_member = request.user in team.members.all()
    members = team.members.all()

    return render(request, "userportal/team_detail.html", {
        "team": team,
        "posts": posts,
        "matched_posts": matched_posts,
        "query": query,
        "is_member": is_member,
        "members": members
    })

@login_required
def join_team(request, team_id):
    team = Team.objects.get(team_id=team_id)
    team.members.add(request.user)
    return redirect('team_detail', team_id=team_id)

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, post_id=post_id)

    if post.user != request.user:
        return redirect('home')

    team_id = post.team.team_id
    post.delete()

    return redirect('team_detail', team_id=team_id)


@login_required
def toggle_like(request, post_id):
    post = Post.objects.get(post_id=post_id)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return JsonResponse({
        "likes": post.likes.count()
    })

@login_required
def add_comment(request, post_id):
    if request.method == "POST":
        post = Post.objects.get(post_id=post_id)
        text = request.POST.get('text')

        Comment.objects.create(
            post=post,
            user=request.user,
            text=text
        )

    return redirect('team_detail', team_id=post.team.team_id)

@login_required
def edit_post(request, post_id):
    post = Post.objects.get(post_id=post_id)

    if post.user != request.user:
        return redirect('home')

    if request.method == "POST":
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')

        if request.FILES.get('pdf'):
            post.pdf = request.FILES.get('pdf')

        post.save()
        return redirect('team_detail', team_id=post.team.team_id)

    return render(request, 'userportal/edit_post.html', {'post': post})

def search_team(request):
    query = request.GET.get('q')

    if query:
        try:
            team = Team.objects.get(team_name__iexact=query)
            return redirect('team_detail', team_id=team.team_id)
        except Team.DoesNotExist:
            return redirect('home') 

    return redirect('home')

@login_required
def profile(request):
    user = request.user

    teams = user.teams.all()   
    posts = Post.objects.filter(user=user).order_by('-created_at')

    return render(request, "userportal/profile.html", {
        "teams": teams,
        "posts": posts
    })

@login_required
def generate_summary(request, post_id):
    post = Post.objects.get(post_id=post_id)

    combined_text = get_combined_text(
        post.content,
        post.pdf.path if post.pdf else None
    )

    combined_text = combined_text[:2000]

    if combined_text.strip():
        post.summary = summarize_text(combined_text)
        post.save()

    return redirect('team_detail', team_id=post.team.team_id)

@login_required
def leave_team(request, team_id):
    team = Team.objects.get(team_id=team_id)

    if request.user in team.members.all():
        team.members.remove(request.user)

    return redirect('home')  