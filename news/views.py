from django.shortcuts import render
from django.views.generic.base import View
from .models import Post, Category
from django.views.generic import DetailView, ListView


class HomeView(View):
    def get(self, request, *args, **kwargs):
        post = Post.objects.order_by("-created_at")[0:5]
        category = Category.objects.all()
        return render(request, 'home.html', {'post': post, 'category': category,})


class PostList(ListView):
    model = Post
    template_name = 'news/post_list.html'
    context_object_name = 'post'


class PostDetailView(DetailView):
    model = Post
    template_name = 'news/post_detail.html'
    context_object_name = 'post'


class PostByCategory(ListView):
    model = Post
    context_object_name = 'post'
    template_name = 'news/postbycategory.html'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(slug=self.kwargs['slug']).select_related('category')