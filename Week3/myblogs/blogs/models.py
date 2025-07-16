from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

# ครั้งที่ 2

class Blog(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    like = models.IntegerField(default=0)
    created_by = models.ForeignKey("blogs.Author", on_delete=models.PROTECT)
    created_date = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField("blogs.Category")
    # https://docs.djangoproject.com/en/5.0/topics/db/examples/many_to_many/

    def __str__(self):
        return f"{self.title} ({self.like})"

class Comment(models.Model):
    comment = models.CharField(max_length=200)
    blog = models.ForeignKey("blogs.Blog", on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)