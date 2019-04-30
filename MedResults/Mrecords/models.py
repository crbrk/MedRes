from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_delete
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Clinic(models.Model):
    name = models.CharField(max_length=50)
    street = models.CharField(max_length=50, blank=True)
    street_number = models.CharField(max_length=10, blank=True)
    city = models.CharField(max_length=50, blank=True)
    postal = models.CharField(max_length=6, blank=True)
    owner = models.ForeignKey(get_user_model(),
                              on_delete=models.CASCADE,
                              related_name='c_owner')

    def __str__(self):
        return f"{self.name} {self.street} {self.street_number} {self.city} {self.postal}"

    def identify(self):
        return "clinic"


class Specialist(models.Model):
    name = models.CharField(max_length=50, blank=True)
    surname = models.CharField(max_length=50, blank=True)
    specialisation = models.CharField(max_length=50)
    owner = models.ForeignKey(get_user_model(),
                              on_delete=models.CASCADE,
                              related_name='s_owner')

    def __str__(self):
        return f"{self.specialisation} {self.surname} {self.name}"

    def identify(self):
        return 'specialist'


class Examination(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    signer = models.ForeignKey(Specialist, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    owner = models.ForeignKey(get_user_model(),
                              on_delete=models.CASCADE,
                              related_name='e_owner')

    def __str__(self):
        return f"{self.date}: {self.name} - {self.signer}"

    def identify(self):
        return 'examination'


def user_directory_path(instance, filename):
    return '{0}/{1}'.format(instance.owner.username, filename)




class File(models.Model):
    file = models.FileField(upload_to=user_directory_path)
    examination = models.ForeignKey(Examination, on_delete=models.CASCADE)
    owner = models.ForeignKey(get_user_model(),
                              on_delete=models.CASCADE,
                              related_name='f_owner',
                              )

    def identify(self):
        return 'file'


@receiver(post_delete, sender=File)
def submission_delete(sender, instance, **kwargs):
    instance.file.delete(False)

#below works, but i wouldnt all-in on it;
#for now it works but its still #TODO better

@receiver(pre_save, sender=File)
def submission_after_edit_delete(sender, instance, **kwargs):
    try:
        old_file = sender.objects.get(pk=instance.pk).file
    except sender.DoesNotExist:
        return False

    new_file = instance.file
    if not old_file == new_file:
        old_file.delete(False)
