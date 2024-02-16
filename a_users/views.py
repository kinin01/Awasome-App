from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import *

def profile_view(request, username=None):
    
    
    #if username:
       # profile = get_object_or_404(User, username=username).profile
    #else:
        #try:
    profile = request.user.profile
       # except:
           # raise Http404()
        
    #posts = profile.user.posts.all()
    
    #if request.htmx:
     #   if 'top-posts' in request.GET:
      #      posts = profile.user.posts.annotate(num_likes=Count('likes')).filter(num_likes__gt=0).order_by('-num_likes')
       # elif 'top-comments' in request.GET:
        #    comments = profile.user.comments.annotate(num_likes=Count('likes')).filter(num_likes__gt=0).order_by('-num_likes')
         #   replyform = ReplyCreateForm()
          #  return render(request, 'snippets/loop_profile_comments.html', { 'comments': comments, 'replyform': replyform })
        #elif 'liked-posts' in request.GET:
         #   posts = profile.user.likedposts.order_by('-likedpost__created') 
        #return render(request, 'snippets/loop_profile_posts.html', { 'posts': posts })
    
    #new_message_form = InboxNewMessageForm()
    
    context = {
       'profile' : profile,
      #  'posts': posts,
       # 'new_message_form' : new_message_form
    }
    
    return render(request, 'a_users/profile.html' , context )

def profile_edit_view(request):
    form = ProfileForm(instance=request.user.profile)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            
           # if request.user.emailaddress_set.get(primary=True).verified:
            return redirect('profile')
            #else:
                #return redirect('profile-verify-email') 
        
    #if request.path == reverse('profile-onboarding'):
        #template = 'a_users/profile_onboarding.html'
    #else:
       # template = 'a_users/profile_edit.html'
    return render(request, 'a_users/profile_edit.html', {'form':form})     
        #return render(request, template, {'form':form})


