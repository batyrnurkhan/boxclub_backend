from django.db import models

from accounts.models import CustomUser


# Create your models here.
class ProbableFight(models.Model):
    fighter1 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='fighter1_fights')
    fighter2 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='fighter2_fights')
    promotion_name = models.CharField(max_length=255)
    weight_category = models.IntegerField()  # Store the weight in kg
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.fighter1.username} vs {self.fighter2.username} - {self.promotion_name}"