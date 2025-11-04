"""my iports"""
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage,\
                                  PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm



def post_list(request):
    """post_list function"""
    posts_list = Post.published.all()
    # Постраничная разбивка с 3 постами на страницу
    paginator = Paginator(posts_list, 3)
    page_number = request.GET.get('page')
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # Если page_number не целое число, то
        # выдать первую страницу
        posts = paginator.page(1)
    except EmptyPage:
        # Если page_number находится вне диапазона, то
        # выдать последнюю страницу результатов
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                  {'posts': posts})


def post_detail(request, year, month, day, post):
    """post_detail function"""
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    # list of active comments for this post
    comments = post.comments.filter(active=True)
    # form for user comments
    form = CommentForm()

    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'form': form})


class PostListView(ListView):
    """
    Альтернативное представление списка постов
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_share(request, post_id):
    """post_share function"""
    #Извлечь пост по идентификатору id
    post = get_object_or_404(Post,
                                   id=post_id,
                                   status=Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        #Форма была передана на обработку
        form = EmailPostForm(request.POST)
        if form.is_valid():
            #Поля формы успешно прошли валидацию
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                           f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                           f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'pustovit.iss@gmail.com',
                      [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})


@require_POST
def post_comment(request, post_id):
    """function for comments view"""
    post = get_object_or_404(Post,
                                   id=post_id,
                                   status=Post.Status.PUBLISHED)
    comment = None
    # comment has been sent
    form = CommentForm(data=request.POST)
    if form.is_valid():
        #Create an object of the Comment class, without storing it in database
        comment = form.save(commit=False)
        # assign a post to a comment
        comment.post = post
        #save comment to database
        comment.save()
    return render(request, 'blog/post/comment.html',
                            {'post': post,
                             'form': form,
                             'comment': comment})