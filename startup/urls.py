from django.conf.urls import patterns, include, url
from startup import views

urlpatterns = patterns('',
    url('^$', views.index, name='index'),
    url('plan_page', views.plan_page, name='plan_page'),
    url('^plan/(?P<key>\w+)/$', views.plan, name='plan'),
    url('^flight_query', views.flight_query, name='flight_query'),
    url('^populate_cities', views.populate_cities, name='populate_cities'),
    url('^get_members', views.get_members, name='get_members'),
    url('^can_add_city', views.can_add_city, name='can_add_city'),
    url('^create_plan', views.create_plan, name='create_plan'),
    url('^get_recommendations', views.get_recommendations, name='get_recommendations'),
    url('^compute_plan', views.compute_plan, name='compute_plan'),
    url('^get_intersection', views.get_intersection, name='get_intersection'),
    
)


urlpatterns += patterns('',
  url(r'^login/$', views.login_view, name='login_view'),
  url(r'^logout/$', views.logout_view, name='logout_view'),
  url(r'^signup/$', views.signup, name='signup'),
  url(r'^login_page/$', views.login_page, name='login_page'),
  url(r'^signup_page/$', views.signup_page, name='signup_page'),
) 