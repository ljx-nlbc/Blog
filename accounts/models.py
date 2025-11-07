from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    """用户头像"""
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to='avatars/',
        default='avatars/default.png',
        blank=True
    )
    bio = models.TextField(max_length=500,blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # 调整图片大小
        if self.avatar:
            img = Image.open(self.avatar.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.avatar.path)

    def __str__(self):
        return f"{self.user.username} 的资料"
