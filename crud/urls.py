from django.conf.urls import url
from . import views


urlpatterns = [
    url(
        r'^api/v1/books/(?P<pk>[0-9]+)$',
        views.get_delete_update_book,
        name='get_delete_update_book'
    ),

    url(
        r'^api/v1/books/$',
        views.get_post_books,
        name='get_post_books'
    ),
	url(
		r'^api/v1/check/$',
		views.urlCheck,
		name='urlCheck'
	)
]
