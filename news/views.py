from django.shortcuts import render, redirect
from django.views.generic.base import View
from .models import Post, Category, Comment
from django.views.generic import DetailView, ListView, FormView
from .forms import CommentForm
from django.urls import reverse, reverse_lazy


class HomeView(View):
    def get(self, request, *args, **kwargs):
        post = Post.objects.order_by("-created_at")[0:5]
        category = Category.objects.all()
        return render(request, 'home.html', {'post': post, 'category': category,})


class PostList(ListView):
    model = Post
    template_name = 'news/post_list.html'
    context_object_name = 'post'


class PostDetailView(FormView, DetailView):
    model = Post
    template_name = 'news/post_detail.html'
    context_object_name = 'post'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('post_detail', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['comments'] = Comment.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class PostByCategory(ListView):
    model = Post
    context_object_name = 'post'
    template_name = 'news/postbycategory.html'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.select_related('category')