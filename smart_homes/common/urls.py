from django.urls import path
from django.views.generic import TemplateView
from smart_homes.common.views import ContactView


urlpatterns = [
    path("", TemplateView.as_view(template_name="common/index.html"), name="home"),
    path("about/", TemplateView.as_view(template_name="common/about.html"), name="about"),
    path("for-business/", TemplateView.as_view(template_name="common/for-business.html"), name="for_business"),
    path("for-home/", TemplateView.as_view(template_name="common/for-home.html"), name="for_home"),
    path("solutions/", TemplateView.as_view(template_name="common/solutions.html"), name="solutions"),

    path("contact/", ContactView.as_view(), name="contact")
]

