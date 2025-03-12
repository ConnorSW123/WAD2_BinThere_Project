from django.db import models
from django.conf import settings
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.contrib import admin
from django.contrib.auth.models import User
from django import forms


class UserProfile(models.Model):
    # This line is required. Links UserProfile to a user model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    #The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username  # Now displays the username in Django Admin


class Location(models.Model):
    """Represents a unique location where bins are placed."""
    NAME_MAX_LENGTH = 100
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)  # Ensure unique names
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0.0)  # Store latitude as a decimal (up to 6 decimal places)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0.0) # Store longitude as a decimal (up to 6 decimal places)
    slug = models.SlugField(unique=True, blank=True)  # Slug field for URL-friendly names

    def save(self, *args, **kwargs):
        """Generate a slug before saving."""
        self.slug = slugify(self.name)
        super(Location, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'locations'

    def __str__(self):
        return self.name


# Types of waste that bins accept
class BinType(models.Model):
    WASTE_CHOICES = [
        ('PET Bottle', 'PET Bottle'),
        ('Glass', 'Glass'),
        ('Plastic', 'Plastic'),
        ('Paper', 'Paper'),
        ('Metal', 'Metal'),
        ('General', 'General'),
        ('Organic', 'Organic'),
    ]
    name = models.CharField(max_length=50, choices=WASTE_CHOICES, unique=True)

    class Meta:
        verbose_name_plural = 'bin_types'

    def __str__(self):
        return self.name




class Bin(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="bins")
    bin_types = models.ManyToManyField(BinType, related_name="bins")  # Allow multiple bin types
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    

    # Additional fields
    overview = models.TextField(default="No overview provided")
    picture = models.ImageField(upload_to='bin_pictures/', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'bins'

    def __str__(self):
        return f"{', '.join([bin_type.name for bin_type in self.bin_types.all()])} Bin at {self.location.name}"




# Allows users to upvote or downvote a bin
class Vote(models.Model):
    bin = models.ForeignKey(Bin, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vote = models.SmallIntegerField(choices=[(1, 'Upvote'), (-1, 'Downvote')])

    class Meta:
        unique_together = ('bin', 'user')  # Prevents duplicate votes by the same user

    def __str__(self):
        return f"{self.user.username} voted {self.vote} on {self.bin}"


