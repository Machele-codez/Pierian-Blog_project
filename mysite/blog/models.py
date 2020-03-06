from django.db import models
from django.utils import timezone
from django.urls import reverse


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete = models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now())
    published_date = models.DateTimeField(blank=True, null=True)

    # todo: funtion to publish a comment and save its date of publication 
    def publish(self):
        self.published_date = timezone.now()
        self.save()
    
    def approved_comments(self):
        return self.comments.filter(approved=True)

    # todo: define url to go back to after creation
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

class Comment(models.Model):
    author = models.CharField(max_length=100) #? the author of the comment could be anyone at all
    post = models.ForeignKey('blog.Post', on_delete = models.CASCADE, related_name='comments')
    text = models.TextField()
    create_date = models.DateTimeField(default = timezone.now)
    approved = models.BooleanField(default=False)

    def approve(self):
        self.approved = True
        self.save()

    # todo: define url to go back to after creation
    def get_absolute_url(self):
        return reverse("post_list")
    

    def __str__(self):
        return self.text
        