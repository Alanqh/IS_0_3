from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('customer', '客户'),
        ('staff', '员工'),
    )
    role = models.CharField('角色', max_length=10, choices=ROLE_CHOICES)
    department = models.CharField('部门', max_length=50)
    name = models.CharField('姓名', max_length=50)
    gender = models.CharField('性别', max_length=10)
    birth_date = models.DateField('生日')
    phone_number = models.CharField('手机号', max_length=20)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="custom_user_set",  # 指定不同的related_name
        related_query_name="custom_user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="custom_user_set",  # 指定不同的related_name
        related_query_name="custom_user",
    )

    def __str__(self):
        return self.username

    def get_unread_messages(self):
        return self.received_messages.filter(read=False)

    def get_sent_messages(self):
        return self.sent_messages.all()

    def send_message(self, recipient, content):
        message = Message(sender=self, recipient=recipient, content=content)
        message.save()

    def mark_message_as_read(self, message_id):
        message = self.received_messages.get(id=message_id)
        message.mark_as_read()

    liked_posts = models.ManyToManyField(
        'blog.Post',
        related_name='likes',
        blank=True,
        verbose_name='Liked posts'
    )

    def like_post(self, post):
        self.liked_posts.add(post)

    def unlike_post(self, post):
        self.liked_posts.remove(post)

    def has_liked_post(self, post):
        return self.liked_posts.filter(id=post.id).exists()

    def get_following(self):
        return self.following.all()

    def get_followers(self):
        return self.followers.all()


class Car(models.Model):
    car_id = models.CharField(max_length=20, primary_key=True)
    car_name = models.CharField('车名', max_length=50)

    def __str__(self):
        return self.car_name


class Message(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        verbose_name='发件人',
    )
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_messages',
        verbose_name='收件人',
    )
    content = models.TextField('内容')
    timestamp = models.DateTimeField('时间戳', auto_now_add=True)
    is_read = models.BooleanField('已读', default=False)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.recipient.username}"

    def mark_as_read(self):
        self.is_read = True
        self.save()
