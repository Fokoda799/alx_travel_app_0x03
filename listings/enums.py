from django.db import models


class Role(models.TextChoices):
    ADMIN = 'admin', 'Administrator'
    GUEST = 'guest', 'Guest'
    HOST = 'host', 'Host'

    
class Status(models.TextChoices):
    PENDING = 'pending', 'Pending'
    CONFIRMED = 'confirmed', 'Confirmed'
    CANCELED = 'canceled', 'Canceled'
