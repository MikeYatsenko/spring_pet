from django.conf import settings
from django.db import models
from users.models import User
from autoslug import AutoSlugField
import random
import string

ALPHANUMERIC_CHARS = string.ascii_lowercase + string.digits
STRING_LENGTH = 3

def generate_random_string(chars = ALPHANUMERIC_CHARS, length = STRING_LENGTH):
     return "".join(random.choice(chars)for _ in range(length))

def my_slug_func(title):
    string = generate_random_string()
    title_x = str((title.replace(' ','_')))
    title_z = title_x.lower()
    return '{}_{}'.format(string,title_z)


class Post(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField()
    title = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from=lambda instance: instance.title,
                         unique_with=['author', 'creation_date'],
                         slugify=my_slug_func)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='blog')
    voters = models.ManyToManyField(to=User, related_name='voters')

    def __str__(self):
        return self.title





class Comment(models.Model):
     creation_date = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)
     content = models.TextField()
     post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
     author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
     comment_voters = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='comment_voters')

     def __str__(self):
         return self.author.username
