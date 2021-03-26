# -*- coding: utf-8 -*-
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models, connection, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def list_databases():
    cursor = connection.cursor()
    cursor.execute(""" SELECT datname from pg_database WHERE datname LIKE 'user_%'""")
    rows = cursor.fetchall()
    return [(row[0], row[0]) for row in rows]


def create_database(name):
    cursor = connection.cursor()
    cursor.execute(f""" CREATE DATABASE {name} """)
    cursor.execute(f""" CREATE ROLE {name} """)
    cursor.execute(f""" GRANT ALL ON DATABASE {name} TO {name}""")


class UserManager(BaseUserManager):
    # Mostly copied from django.contrib.auth.models.UserManager

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), max_length=254, unique=True)
    name = models.CharField(max_length=255)

    is_staff = models.BooleanField(_("staff status"), default=False)
    is_active = models.BooleanField(_("active"), default=True)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    database = models.CharField(max_length=255)
    number_of_secondary_roles = models.PositiveIntegerField(default=10)

    USERNAME_FIELD = "email"

    objects = UserManager()

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name


@receiver(post_save, sender=User)
def create_db_for_user(sender, instance: User, *args, **kwargs):
    if not instance.database:
        instance.database = f'user_{instance.id}'
        create_database(instance.database)
        with transaction.atomic():
            instance.save(update_fields=['database'])
