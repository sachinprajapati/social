from django.db import models

from django.contrib.auth import get_user_model

UserModel = get_user_model()

class Posts(models.Model):
	user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
	title = models.CharField(max_length=255, null=True, blank=True)
	desc = models.TextField()
	dt = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __str__(self):
		return '{} by {}'.format(self.title, self.user.username)

	def getLikes(self):
		return self.like_set

	def isLiked(self, user):
		l = Like.objects.filter(by=user, post=self).exists()
		print(l)
		return l

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'media/user_{0}/posts/{1}'.format(instance.post.user.id, filename)

class Images(models.Model):
	img = models.ImageField(upload_to=user_directory_path)
	post = models.ForeignKey(Posts, on_delete=models.CASCADE)
	dt = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
	post = models.ForeignKey(Posts, on_delete=models.CASCADE)
	by = models.ForeignKey(UserModel, on_delete=models.CASCADE)
	dt = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return 'post {0} by {1}'.format(self.post, self.by)
