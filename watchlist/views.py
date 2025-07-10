from django.shortcuts import render #render HTML templates (returning an HTTP response with a given template and context data).  

import requests # make HTTP requests to the external TMDB API and receive JSON responses.
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy  # resolves a URL name into a URL string lazily (useful in class-based views, similar to url_for in Flask).
from django.shortcuts import redirect #sending the user to a different URL.
from .models import WatchItem , Status #db
from .forms import WatchItemForm #WatchItem entries.
from django.contrib.messages.views import SuccessMessageMixin



class WatchItemListView(ListView):
 # هذا البحث الداخلي في قاعدة بياناتي (WatchItem)

    model = WatchItem
    template_name = 'watchlist/home.html'
    context_object_name = 'watchlist'
    paginate_by = 8  # هنا عدد العناصر في كل صفحة 


    def get_queryset(self):
        queryset = super().get_queryset()
        type_filter = self.request.GET.get('type')
        status_filter = self.request.GET.get('status')
        # يدعم q أو query
        query = self.request.GET.get('query') or self.request.GET.get('q')

        if type_filter:
            queryset = queryset.filter(type=type_filter)
        if status_filter:
            queryset = queryset.filter(status__name=status_filter)
        if query:
            queryset = queryset.filter(title__icontains=query)
        return queryset
    
    def get_context_data(self, **kwargs):
        #  show_type_filter = True عشان يظهر في الهوم فقط
        context = super().get_context_data(**kwargs)
        context['show_type_filter'] = True
        return context

class WatchItemDetailView(DetailView):
    model = WatchItem
    template_name = 'watchlist/details.html'
    context_object_name = 'item'
    
    def get_context_data(self, **kwargs):
        #  show_type_filter = False يخفي الفلتر لهالصفحة
        context = super().get_context_data(**kwargs)
        context['show_type_filter'] = False
        return context


class WatchItemCreateView(SuccessMessageMixin, CreateView):
    model = WatchItem
    form_class = WatchItemForm
    template_name = 'watchlist/add.html'
    success_url = reverse_lazy('home') # equivalent to "redirect" in function based views
    success_message = "Movie/Series was added successfully!"

    def get_context_data(self, **kwargs):
        #  show_type_filter = False يخفي الفلتر لهالصفحة
        context = super().get_context_data(**kwargs)
        context['show_type_filter'] = False
        return context



class WatchItemUpdateView(SuccessMessageMixin, UpdateView):
    model = WatchItem
    form_class = WatchItemForm
    template_name = 'watchlist/edit.html'
    success_url = reverse_lazy('home') # equivalent to "redirect" in function based views
    success_message = "Movie/Series was updated successfully!"

    def get_context_data(self, **kwargs):
        #  show_type_filter = False يخفي الفلتر لهالصفحة
        context = super().get_context_data(**kwargs)
        context['show_type_filter'] = False
        return context




class WatchItemDeleteView(DeleteView):
    model = WatchItem
    template_name = 'watchlist/delete.html'
    success_url = reverse_lazy('home') # equivalent to "redirect" in function based views

    def get_context_data(self, **kwargs):
        #  show_type_filter = False يخفي الفلتر لهالصفحة
        context = super().get_context_data(**kwargs)
        context['show_type_filter'] = False
        return context


class MovieSearchView(TemplateView):
    template_name = 'watchlist/search.html'
    api_key = '7b471cc80f03ffba08be5289f331c098'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        search_type = self.request.GET.get('type', 'multi')


        local_results = []
        movies = []

        if query:
            #  البحث الداخلي في قاعدة بياناتي (WatchItem)
            local_results = WatchItem.objects.filter(title__icontains=query)

            if not local_results.exists():
                #  البحث الخارجي في TMDB API لو ما لقيت في قائمتي
                url = f"https://api.themoviedb.org/3/search/{search_type}?api_key={self.api_key}&query={query}"
                response = requests.get(url)
                data = response.json()
                if data.get('results'):
                    movies = data['results']

        #To Send All Variables To Template
        context['local_results'] = local_results
        context['movies'] = movies
        context['query'] = query
        context['search_type'] = search_type
        context['show_type_filter'] = False

        return context

class AddFromAPIView(SuccessMessageMixin, CreateView): # to add movies from api
    model = WatchItem
    fields = []  
    success_url = reverse_lazy('home')
    success_message = "Movie/Series was added successfully!"

    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        type= request.POST.get('type') 
        year = request.POST.get('year')
        poster_path = request.POST.get('poster_path')

          #  هنا نحول type جاي من TMDB (tv أو movie) إلى Movie / Series
        if type == "Tv":
            type_value = "Series"
        else:
            type_value = "Movie"

        #Builds the full URL for the poster image.
        full_poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else ""

        #By default, sets the status of the new item to “Want to Watch”.
        status = Status.objects.get(name="Want to Watch")

        #Creates and saves the new WatchItem in the database.
        WatchItem.objects.create(
            title=title,
            type=type,
            year=year or 0,
            genre="",
            rating=0,
            poster_url=full_poster_url,
            status=status
        )

        return redirect(self.success_url)











   

    