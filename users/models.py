from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()

def getFollowers(self, *args, **kwargs):
	return Follow.objects.filter(to=self)

def getFollowing(self, *args, **kwargs):
	return Follow.objects.filter(by=self)


UserModel.add_to_class('getFollowers', getFollowers)
UserModel.add_to_class('getFollowing', getFollowing)

def user_profile_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'media/user_{0}/profile/{1}'.format(instance.user.id, filename)

GENDER = [
    (1, 'male'),
    (2, 'female'),
]

class Profile(models.Model):
	user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
	# slug = models.SlugField(unique=True, populate_from=('name',))
	dob = models.DateField(null=True, blank=True)
	img = models.ImageField(upload_to=user_profile_path, null=True, blank=True)
	gender = models.SmallIntegerField(choices=GENDER, blank=True, null=True)


class Follow(models.Model):
	by = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="follow_by")
	to = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="follow_to")
	dt = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return 'by {} to {}'.format(self.by.username, self.to.username)

	class Meta:
		unique_together = ('by', 'to',)


