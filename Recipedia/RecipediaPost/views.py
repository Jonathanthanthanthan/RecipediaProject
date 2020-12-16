from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from .forms import EmailPostForm, CreatePostForm, CommentForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponse, JsonResponse

@login_required
def post_list(request):
    posts = Post.published.get_queryset(request.user)
    return render(request,
                  'postlist.html',
                  {'posts': posts})

@login_required
def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST) 
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            # ... send email
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form})

@login_required
def create_post(request):
    if request.method== 'POST':
        form=CreatePostForm(request.POST,files=request.FILES)
        if form.is_valid():
             # Create a new post object but avoid saving it yet
            new_post = form.save(commit=False)
            new_post.author=request.user
            new_post.author_name=request.user.username
            new_post.save()
            return redirect(new_post.get_absolute_url())
    else:
        form=CreatePostForm()
    return render(request,'create_post.html', {'form': form})

@login_required
def post_detail(request, year, month, day, user, post):
    post = get_object_or_404(Post,  author_name=user,
                                    slug=post,
                                    status='published',
                                    publish__year=year,
                                    publish__month=month,
                                    publish__day=day)
    #List of active comments on the post
    comments = post.comments.filter(active=True)

    #new comment that will be created from forms
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.email = request.user.email
            new_comment.user = request.user
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request,'postdetail.html', {'post': post, 'comments':comments, 'comment_form':comment_form})
   
@login_required
def post_feed(request):
    user=request.user
    following=[following_user for following_user in user.following.all()]
    posts = Post.objects.filter(author__in = following).order_by('-pk')

    return render (request,'feed.html',{'posts':posts})

@login_required
@require_POST
def post_like(request):
    post_id = request.POST.get('id')
    action = request.POST.get('action')
    if post_id and action:
        try:
            post = Post.objects.get(id=post_id)
            if action == 'like':
                post.users_like.add(request.user)
            else:
                post.users_like.remove(request.user)
            return JsonResponse({'status':'ok'})
        except:
            pass
        return JsonResponse({'status':'error'})