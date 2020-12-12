from django.shortcuts import render, get_object_or_404
from .models import Post
from .forms import EmailPostForm, CreatePostForm
from django.shortcuts import render, redirect

def post_list(request):
    posts = Post.published.get_queryset(request.user)
    return render(request,
                  'postlist.html',
                  {'posts': posts})
#Handling forms in views
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

def post_detail(request, year, month, day, user, post):
    post = get_object_or_404(Post,  author_name=user,
                                    slug=post,
                                    status='published',
                                    publish__year=year,
                                    publish__month=month,
                                    publish__day=day)
    return render(request,
                  'postdetail.html',
                  {'post': post})
    

