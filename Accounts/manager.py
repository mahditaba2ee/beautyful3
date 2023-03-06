from django.contrib.auth.models import BaseUserManager


class MyUserManager(BaseUserManager):
    def create_user(self,email,username,phone,password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not phone:
            raise ValueError('Users must have a phone number')
        if not username:
            raise ValueError('Users must have a username')
        user = self.model(email=self.normalize_email(email),
                          phone = phone,
                          username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


        
    def create_superuser(self,email,username,phone,password=None):
        user = self.create_user(email=email,username=username,phone=phone,password=password)
        user.is_admin = True
        user.is_superuser=True
        user.save(using=self._db)
        return user
