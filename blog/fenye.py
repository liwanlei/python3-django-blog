from  django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
def fenye(request,posts):
    paginator = Paginator(posts, 4)
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.paginator(paginator.num_pages)
    return post_list