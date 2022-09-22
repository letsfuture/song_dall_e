from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Post, Category

import os
import time

from soynlp.normalizer import *
import re

class PostCreate(CreateView):
    model = Post
    fields = ['content']
    
class PostList(ListView):
    model = Post
    ordering = '-pk'
    # template_name = 'blog/index.html'
    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context

class PostDetail(DetailView):
    model = Post
    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context

    # def get_result(self, **kwargs):
    #     k_count = 0
    #     e_count = 0
    #     result = super(PostDetail, self).get_context_data()
    #     for c in str(result):
    #         if ord('가') <= ord(c) <= ord('힣'):  # ord ---> 하나의 문자를 인자로 받고 해당 문자에 해당하는 유니코드 정수를 반환
    #             k_count += 1
    #         elif ord('a') <= ord(c.lower()) <= ord('z'):
    #             e_count += 1
    #     if k_count > 1:
    #         result = "한국어"
    #     else:
    #         result = "영어"
    #     return result



# def index(request):
#     posts = Post.objects.order_by('-pk')
#
#     return render(
#         request,
#         'blog/index.html',
#         {
#             'posts': posts,
#         }
#     )

# def single_post_page(request, pk):
#     post = Post.objects.get(pk=pk)
#
#     return render(
#         request,
#         'blog/single_post_page.html',
#         {
#             'post':post,
#         }
#     )

def category_page(request, slug):
    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

    return render(
        request,
        'blog/post_list.html',
        {
            'post_list': post_list,
            'categories': Category.objects.all(),
            'no_category_post_count': Post.objects.filter(category=None).count(),
            'category': category,
        }
    )