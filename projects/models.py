
import uuid
from django.db import models

from users.models import Profile


class Project(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, 
    primary_key=True, editable=False)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE,null=True,blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(null=False,blank=False, default="default.jpg")
    demo_link = models.CharField(max_length=2000,null=True,blank=True)
    source_link = models.CharField(max_length=2000,null=True,blank=True)
    tags = models.ManyToManyField("Tag",blank=True )
    vote_total = models.IntegerField(default=0, null=True,blank=True)
    vote_ratio = models.IntegerField(default=0, null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    

    class Meta:
        ordering = ["-vote_ratio","-vote_total", "title"]
    
    def __str__(self):
        return self.title


    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list("owner_id", flat=True)
        return queryset

    @property
    def get_vote_count(self):
        reviews = self.review_set.all()
        up_votes = reviews.filter(value = "up").count()
        total_votes = reviews.count()

        ratio = (up_votes / total_votes) * 100
        self.vote_total = total_votes
        self.vote_ratio = ratio
        self.save()

class Review(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, 
    primary_key=True, editable=False)
    VOTE_TYPE = (
        ("up", "Up vote"),
        ("down", "Down vote"),
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [["owner","project"]]


    def __str__(self):
        return self.value


class Tag (models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, 
    primary_key=True, editable=False)
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    


    def __str__(self):
        return self.name