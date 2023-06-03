from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField
from register.models import User


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField('标题',max_length=100)
    content = RichTextUploadingField('内容',blank=False)
    image = models.ImageField('图片',upload_to='blog/images/', null=True, blank=True)
    video = models.FileField('视频',upload_to='blog/videos/', null=True, blank=True)
    created_at = models.DateTimeField('创建时间',auto_now_add=True)
    updated_at = models.DateTimeField('更新时间',auto_now=True)
    shares = models.PositiveIntegerField('分享',default=0)
    tags = TaggableManager('标签',blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} commented on {self.post.title}'


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f'{self.follower.username} follows {self.following.username}'


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f'{self.user.username} likes {self.post.title}'
