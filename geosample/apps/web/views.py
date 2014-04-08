# coding: utf-8
from django.views.generic import TemplateView
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from django.http import Http404
from geosample.apps.data.models import PhenomenonObservation
import models


class BasePageView(TemplateResponseMixin):
    """ All pages should inherit this class to get shared components
    """

    def dispatch(self, request, *args, **kwargs):
        # get shared objets between pages
        self.year = datetime.today().year
        self.pages = models.Page.objects.get(url='/').get_descendants()
        return super(BasePageView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BasePageView, self).get_context_data(**kwargs)
        # Add shared objects
        context['year'] = self.year
        context['pages'] = self.pages
        return context


class HomePageView(TemplateView, BasePageView):

    template_name = "web/home.html"


class GenericPageView(DetailView, BasePageView):

    template_name = "web/page.html"
    model = models.Page
    context_object_name = 'page'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        # Get page by url
        url = self.kwargs.get('url', None)
        queryset = queryset.filter(url='/' + url)
        try:
            obj = queryset.get()
        except ObjectDoesNotExist:
            raise Http404(_(u"Page not found"))
        return obj


class ObservationListView(ListView, BasePageView):

    template_name = "web/observation_list.html"
    model = PhenomenonObservation

    def dispatch(self, request, *args, **kwargs):
        # get page title, content from Page if exits
        self.page = models.Page(title='Observation list')
        try:
            self.page = models.Page.objects.get(url=request.path)
        except ObjectDoesNotExist:
            pass
        # Paginate results
        page = request.GET.get('page', 1)
        self.queryset = self.get_queryset()
        paginator = Paginator(self.queryset, 20)  # 20 per page
        try:
            self.current_page = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            self.current_page = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            self.current_page = paginator.page(paginator.num_pages)
        return super(ObservationListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ObservationListView, self).get_context_data(**kwargs)
        context['page'] = self.page
        context['current_page'] = self.current_page
        return context
