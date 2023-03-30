"""
Module/Script Name:<views>
Author: <Devin>
Date: <2023/3/14 15:43>
Description: <Description of Module/Script>
"""

# 引入需要的模块和类
from django.http import Http404   # 引入用于处理 404 异常的类
from django.shortcuts import render   # 引入用于渲染页面的函数
from django.shortcuts import redirect   # 引入用于重定向到其他页面的函数
from django.contrib.auth.decorators import login_required   # 引入用于限制页面访问权限的装饰器

from .models import Topic, Entry   # 引入自定义的模型类
from .forms import TopicForm, EntryForm   # 引入用于处理表单的自定义表单类


# 定义视图函数
# 首页视图函数
# @login_required 注释表示该视图需要登录才能访问，如果未登录则跳转到登录页面。
def index(request):
    """学习笔记的主页"""
    return render(request, 'learning_logs/index.html')


# 主题列表视图函数
@login_required
def topics(request):
    """显示所有的主题。"""
    # 获取当前用户的所有主题，并按创建时间排序。
    topics1 = Topic.objects.filter(owner=request.user).order_by('date_added')
    # 将topics以字典形式传递给模板渲染。
    context = {'topics': topics1}
    return render(request, 'learning_logs/topics.html', context)


# 单个主题视图函数
@login_required
def topic(request, topic_id):
    """显示一个主题及其所有条目。"""
    # 根据传递的主题id获取对应的主题实例。
    topic1 = Topic.objects.get(id=topic_id)
    # 确认请求的主题属于当前用户，如果不属于则抛出404异常。
    if topic1.owner != request.user:
        raise Http404
    # 获取该主题下的所有条目，并按创建时间倒序排序。
    entries = topic1.entry_set.order_by('-date_added')
    # 将topic和entries以字典形式传递给模板渲染。
    context = {'topic': topic1, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


# 新建主题视图函数
@login_required
def new_topic(request):
    """添加新主题。"""
    if request.method != 'POST':
        # 未提交数据：创建一个新表单。
        form = TopicForm()
    else:
        # POST提交的数据：对数据进行处理。
        form = TopicForm(data=request.POST)
        if form.is_valid():
            # 将表单数据与当前用户关联，并保存主题实例。
            new_topic1 = form.save(commit=False)
            new_topic1.owner = request.user
            new_topic1.save()

            return redirect('learning_logs:topics')

    # 显示空表单或指出表单数据无效。
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


# 新建条目视图函数
@login_required
def new_entry(request, topic_id):

    """在特定主题中添加新条目。"""
    # 根据传递的主题id获取对应的主题实例。
    topic1 = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        # 未提交数据：创建一个空表单。
        form = EntryForm()
    else:
        # POST提交的数据：对数据进行处理。
        form = EntryForm(data=request.POST)
        if form.is_valid():
            # 将表单数据与当前主题关联，并保存条目实例。
            new_entry1 = form.save(commit=False)
            new_entry1.topic = topic1
            new_entry1.save()

            return redirect('learning_logs:topic', topic_id=topic_id)
    # 显示空表单或指出表单数据无效。
    context = {'topic': topic1, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


# 编辑条目视图函数
@login_required
def edit_entry(request, entry_id):
    """编辑既有条目。"""
    # 根据传递的条目id获取对应的条目实例。
    entry1 = Entry.objects.get(id=entry_id)
    # 获取该条目对应的主题实例。
    topic1 = entry1.topic
    # 确认请求的主题属于当前用户。
    if topic1.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # 初次请求：使用当前条目填充表单。
        form = EntryForm(instance=entry1)
    else:
        # POST提交的数据：对数据进行处理。
        form = EntryForm(instance=entry1, data=request.POST)
        if form.is_valid():
            # 将修改后的条目数据保存到数据库，并重定向到该条目所属的主题页面。
            form.save()
            return redirect('learning_logs:topic', topic_id=topic1.id)

    # 将当前条目、所属主题以及表单实例以字典形式传递给模板渲染。
    context = {'entry': entry1, 'topic': topic1, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)
