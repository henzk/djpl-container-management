

def refine_get_urls(original):

    def get_urls():
        from django.conf.urls import url, patterns, include
        urlpatterns = patterns('',
            # place your feature's urls here
            # see: https://docs.djangoproject.com/en/dev/topics/http/urls/
            # examples:
            # url(r'^articles/([0-9]{4})/([0-9]{2})/([0-9]+)/$', 'news.views.article_detail'),
            # url(r'^(?P<username>\w+)/blog/', include('foo.urls.blog')),

        )
        return urlpatterns + original()
    return get_urls
