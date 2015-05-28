from core.models import Question, Tag
from django.core.management.base import BaseCommand, CommandError
import operator
from django.core.cache import cache


def count():
	N = 10
	count = Question.objects.count()

	count_map = {}
	for i in range(1, count + 1):
		try:
			q = Question.objects.get(id=i)
			print q.title
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
    def handle(self, *args, **options):
        tag_list = count()
        cache.set('tags', tag_list)

        


		