# 引入 Django 的 models 模块和 User 模型
from django.db import models
from django.contrib.auth.models import User

# Topic 模型
class Topic(models.Model):
    """用户学习的主题"""

    # 主题名称，最大长度为200
    text = models.CharField(max_length=200)

    # 创建时间，自动添加
    date_added = models.DateTimeField(auto_now_add=True)

    # 外键，对应 User 模型
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """返回模型的字符串表示"""
        # 返回主题名称的前50个字符
        return f"{self.text[:50]}"

# Entry 模型
class Entry(models.Model):
    """学到的有关某个主题的具体知识"""

    # 外键，对应 Topic 模型
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    # 具体知识的文本内容
    text = models.TextField()

    # 创建时间，自动添加
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries' # 模型的复数名称

    def __str__(self):
        """返回模型的字符串表示"""
        # 返回具体知识的前50个字符，加上省略号
        return f"{self.text[:50]}..."
