from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from django.utils import timezone

# Create your views here.
def showmain(request):
    posts = Post.objects.all()
    return render(request, "main/mainpage.html", {"posts": posts})


def post(request):
    posts = Post.objects.all()
    return render(request, "main/post.html", {"posts": posts})


def showhw(request):
    return render(request, "main/show.html")


def introduce(request):
    return render(request, "main/introduce.html")


def detail(request, id):
    post = get_object_or_404(Post, pk=id)
    all_comments = post.comments.all().order_by("-created_at")
    return render(request, "main/detail.html", {"post": post, "comments": all_comments})


def new(request):
    return render(request, "main/new.html")


def create(request):
    new_post = Post()
    new_post.title = request.POST["title"]
    new_post.writer = request.user
    new_post.pub_date = timezone.now()
    new_post.summary = request.POST["summary"]
    new_post.body = request.POST["body"]
    new_post.image = request.FILES.get("image")
    new_post.save()
    return redirect("main:detail", new_post.id)


def edit(request, id):
    edit_post = Post.objects.get(id=id)
    return render(request, "main/edit.html", {"post": edit_post})


def update(request, id):
    update_post = Post.objects.get(id=id)
    update_post.title = request.POST["title"]
    update_post.writer = request.user
    update_post.pub_date = timezone.now()
    update_post.body = request.POST["body"]
    update_post.image = request.FILES.get("image")
    update_post.save()
    return redirect("main:detail", update_post.id)


def delete(request, id):
    delete_post = Post.objects.get(id=id)
    delete_post.delete()
    return redirect("main:post")


def create_comment(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=post_id)
        current_user = request.user
        comment_content = request.POST.get("content")
        Comment.objects.create(content=comment_content, writer=current_user, post=post)
    return redirect("main:detail", post_id)


def edit_comment(request, id):
    comment = Comment.objects.get(id=id)
    if request.user == comment.writer:
        return render(request, "main/edit_comment.html", {"comment": comment})
    else:
        return redirect("main:detail", comment.post.id)


def update_comment(request, id):
    comment = Comment.objects.get(id=id)
    comment.content = request.POST.get("content")
    comment.save()
    return redirect("main:detail", comment.post.id)


def delete_comment(request, id):
    comment = Comment.objects.get(id=id)
    if request.user == comment.writer:
        comment.delete()
    return redirect("main:detail", comment.post.id)
