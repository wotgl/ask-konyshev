from core.models import Question, Profile, Tag, Answer, QLike, ALike
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
import operator
from django.core.cache import cache


def count():
	N = 10
	count = Answer.objects.count()

	count_map = {}
	for i in range(1, count + 1):
		try:
			a = Answer.objects.get(id=i)
			author = a.author
			try:
				res = count_map[author.username]
				count_map[author.username] = res + 1
			except Exception, e:
				count_map[author.username] = 1

		except Answer.DoesNotExist, e:
			pass
					

	sorted_x = sorted(count_map.items(), key=operator.itemgetter(1), reverse=True)

	return sorted_x[:5]


class Command(BaseCommand):
    def handle(self, *args, **options):
        user_list = count()
        cache.set('users', user_list)

        


		