from core.models import Question, Tag
from django.core.management.base import BaseCommand, CommandError
import operator
import memcache


def count():
	N = 10
	count = Question.objects.count()

	count_map = {}
	for i in range(0, count):
		try:
			q = Question.objects.get(id=i)
			tags = q.tags.all()
			for tag in tags:
				try:
					res = count_map[tag.name]
					count_map[tag.name] = res + 1
				except Exception, e:
					count_map[tag.name] = 1

		except Question.DoesNotExist, e:
			pass
					

	sorted_x = sorted(count_map.items(), key=operator.itemgetter(1), reverse=True)

	return sorted_x[:10]


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    # def add_arguments(self, parser):
    #     parser.add_argument('count', nargs='+', type=str)

    def handle(self, *args, **options):
        tag_list = count()
        for i in tag_list:
        	print str(i[0]) + "   " + str(i[1])
        cache = memcache.Client(['127.0.0.1:11211'], debug=0) 
        cache.set('tags', tag_list)
        


		