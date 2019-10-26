from django.conf.urls import url
from . import views
from django.contrib.auth import views as  authViews
from django.views.generic import RedirectView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
urlpatterns = [
    url(r'^signup/$', views.signup, name="signup"),
    url(r'^login/$', views.login, name="login.html"),
    url(r'^logout/$', views.logout_view, name="logout.html"),
    url(r'^entry/$',views.Package_entry, name="entry.html"),
    url(r'^delivery/$',views.retrieve,name="delivery.html"),
    url(r'^verified/$',  TemplateView.as_view(template_name='Mailroom/verified.html')),
    url(r'^Adminlogout/$',  TemplateView.as_view(template_name='Mailroom/Adminlogout.html')),
    url(r'^UserSave/$',  TemplateView.as_view(template_name='Mailroom/UserSave.html')),
    url(r'^Packageentry/$',  TemplateView.as_view(template_name='Mailroom/Packageentry.html')),
    url(r'^Home/$',views.Home,name="Home.html"),
    url(r'^(?P<pk>[0-9]+)/$', views.package, name="package.html"),
]
