from django.db import models


# Create your models here.

class userIpdetails(models.Model):
    email = models.CharField(max_length=30, null=True)
    ip_address = models.CharField(max_length=100)
    with_mask_count = models.IntegerField(null=True)
    without_mask_count = models.IntegerField(null=True)
    time = models.DateTimeField(null=True)
    social_dis = models.IntegerField(null=True)

    class Meta:
        db_table = 'user_ipdetails'