from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404


# Help Functions

def pagination(request, list, number_of_page):
	paginator = Paginator(list, number_of_page) # Show number_of_page contacts per page
	page = request.GET.get('page')

	try:
		list = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		list = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		raise Http404('Not found')

	return list


#	Name parser

def nameParser(name):
	parse = name.split(' ')
	dict = {'first_name': parse[0], 'last_name': parse[1:]}
	last_name = ' '.join(dict['last_name'])		#	list to string
	dict['last_name'] = last_name

	return dict

#	For redirect

def checkURL(url):
	pattern = '127.0.0.1'
	if pattern in url:
		return True
	return False

	