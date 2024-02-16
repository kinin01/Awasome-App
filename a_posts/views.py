from django.shortcuts import render, redirect, get_object_or_404
from .forms import *

from bs4 import BeautifulSoup
import requests
from django.contrib import messages


def home_view(request, tag=None): 
    if tag:
        posts = Post.objects.filter(tags__slug=tag)
        tag = get_object_or_404(Tag, slug=tag)
    else:
        posts = Post.objects.all()
    categories = Tag.objects.all()
        
   
        
    #paginator = Paginator(posts, 3)
    #page = int(request.GET.get('page', 1))
    #try:
        #posts = paginator.page(page)
    #except:
       # return HttpResponse('')

    #try:
       # feature_herobutton = feature_enabled(1, 'Andreas')
   # except:
        #feature_herobutton = False
        

    
    context = {
        'posts' : posts,
        'categories': categories,
        'tag' : tag,
       # 'page' : page,
        #'feature_herobutton' : feature_herobutton
    }
    
    #if request.htmx:
        #return render(request, 'snippets/loop_home_posts.html', context)
        
    return render(request, 'a_posts/home.html', context)

        


def post_create_view (request):
    
    form = PostCreateForm()
    
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            
            website = requests.get(form.data['url'])
            sourcecode = BeautifulSoup(website.text, 'html.parser')
            find_image = sourcecode.select('meta[content^="https://live.staticflickr.com/"]')
            try:   
                image = find_image[0]['content']
            except:
                messages.error(request, 'Requested image is not on Flickr!')
                return redirect('post-create')
            
            post.image = image
            
            find_title = sourcecode.select('h1.photo-title')
            title = find_title[0].text.strip()
            post.title = title
            
            find_artist = sourcecode.select('a.owner-name')
            artist = find_artist[0].text.strip() 
            post.artist = artist
            
            post.author = request.user
            
            post.save()
            form.save_m2m()
            return redirect('home')
    
    return render(request, 'a_posts/post_create.html', {'form' : form })
    
    
def post_delete_view(request, pk):
    post = get_object_or_404(Post, id=pk, author=request.user)
    
    if request.method == "POST":
        post.delete()
        messages.success(request, 'Post deleted')
        return redirect('home')
        
    return render(request, 'a_posts/post_delete.html', {'post' : post})


def post_edit_view(request, pk):
    post = get_object_or_404(Post, id=pk)
    form = PostEditForm(instance=post)
    
    if request.method == "POST":
        form = PostEditForm(request.POST, instance=post)
        if form.is_valid:
            form.save()
            messages.success(request, 'Post updated')
            return redirect('home')
    
    context = {
        'post' : post,
        'form' : form
    }
    return render(request, 'a_posts/post_edit.html', context)

def post_page_view(request, pk):
    post = get_object_or_404(Post, id=pk)
   # commentform = CommentCreateForm()
    #replyform = ReplyCreateForm()
    
    #if request.htmx:
       # if 'top' in request.GET:
            #comments = post.comments.annotate(num_likes=Count('likes')).filter(num_likes__gt=0).order_by('-num_likes')
        #else:
            #comments = post.comments.all()
        #return render(request, 'snippets/loop_postpage_comments.html', {'comments': comments, 'replyform': replyform})
    
    #context = {
        #'post' : post,
        #'commentform' : commentform,
       # 'replyform' : replyform,
   # }
    
    return render(request, 'a_posts/post_page.html', {'post': post})
