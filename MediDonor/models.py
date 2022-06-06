from django.db import models

# Create your models here.
from django.db import models

from MediUser.models import MediUser


class common(models.Model):
    date = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        abstract = True


class Organ(common):

    class Meta:
        db_table = 'organ'

    class BloodGroup(models.TextChoices):
        A_positive = 'A+'
        A_negative = 'A-'
        B_positive = 'B+'
        B_negative = 'B-'
        AB_positive = 'AB+'
        AB_negative = 'AB-'
        O_positive = 'O+'
        O_negative = 'O-'

    class Organ_Type(models.TextChoices):
        eye = 'eye'
        kidney = 'kidney'
        heart = 'heart'
        liver = 'liver'
        pancreas = 'pancreas'
        lungus = 'lungus'

    blood_group = models.CharField(max_length=100, choices=BloodGroup.choices, default=BloodGroup.A_positive)
    user_id = models.ForeignKey(MediUser, on_delete=models.CASCADE, related_name='organ', null=True)
    organ_age = models.IntegerField(null=True)
    organ_type = models.CharField(max_length=200, choices=Organ_Type.choices, default=Organ_Type.eye)

    def __str__(self):
        return self.user_id


class Nominee(common):

    class Meta:
        db_table = 'nominee'

    class Relation(models.TextChoices):
        Father = 'father'
        Mother = 'mother'
        Spouse = 'spouse'
        Brother = 'brother'
        Sister = 'sister'
        Friend = 'friend'

    user = models.OneToOneField(MediUser, on_delete=models.CASCADE, related_name='Nominee', null=True)
    nominee_name = models.CharField(max_length=20)
    nominee_mobile = models.CharField(max_length=10, null=True)
    nominee_email = models.EmailField()
    relation = models.CharField(max_length=10, choices=Relation.choices, default=Relation.Spouse)
    username = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.nominee_name


class Post(common):

    class Meta:
        db_table = 'post'

    user_id = models.ForeignKey(MediUser, on_delete=models.CASCADE, related_name='post', null=True)
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=100, default=" ")
    description = models.CharField(max_length=500, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    duration = models.IntegerField(default=0)
    username = models.CharField(max_length=100, default=" ")

    def __str__(self):
        return self.title


class Post_like_count(models.Model):

    class Meta:
        db_table = 'post_like_count'

    user_id = models.OneToOneField(MediUser, on_delete=models.CASCADE, related_name='post_like_count', null=True)
    post_id = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='post_like_count', null=True)
    count_like = models.IntegerField(default=0, editable=False)
    count_dislike = models.IntegerField(default=0, editable=False)

    def __str__(self):
        return self.post_id
