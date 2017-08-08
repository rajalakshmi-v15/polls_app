from django.conf.urls import url

from . import views

app_name = 'sample_app'
urlpatterns = [
    #url(r'^admin/', admin.site.urls),
    url(r'^$', views.HomePageView.as_view(), name = 'home_page'),
	url(r'^(?P<pk>[0-9]+)/$', views.DetailsView.as_view(), name = 'details'),
   	url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name = 'results'),
   	url(r'^(?P<question_id>[0-9]+)/votes/$', views.votes, name = 'votes')
]
# repo name - 