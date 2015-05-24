from core.models import Question, Profile, Tag, Answer, QLike, ALike
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
import operator
import memcache


def count():
	N = 10
	count = Answer.objects.count()

	count_map = {}
	for i in range(0, count):
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
    help = 'Closes the specified poll for voting'

    # def add_arguments(self, parser):
    #     parser.add_argument('count', nargs='+', type=str)

    def handle(self, *args, **options):
        user_list = count()
        cache = memcache.Client(['127.0.0.1:11211'], debug=0) 
        cache.set('users', user_list)
        


		