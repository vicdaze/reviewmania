from io import BytesIO
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.db.models import Count
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
from django.db.models.query import QuerySet
from django.db.models import Q
from django.core.files import File
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth import logout

from reviewmania.forms import ScoreFormSet, LoginForm
from reviewmania.models import Category, Criteria, Photo, Product, Review, Score

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return HttpResponse('Disabled account')
        else:
            return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'reviewmania/login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('home')


def index(request):
    categories = Category.objects.annotate(products_count=Count("product")).order_by("-products_count").exclude(products_count=0)
    context = {"categories" : categories}
    return render(request, "index.html", context)

def search(request):
    search_value = request.GET['q']
    search = Product.objects.filter(\
        Q(title__icontains = search_value) | \
        Q(description__icontains = search_value) | \
        Q(review__text__icontains = search_value))\
        .distinct()
    return render(request, "reviewmania/search.html", {'results': search})

class ProductDetailView(DetailView):
    model = Product
    

class ReviewCreateView(TemplateView):
    template_name = 'reviewmania/product_review.html'
    def get(self, *args, **kwargs):
        product = Product.objects.get(pk=kwargs['pk'])
        category = product.category
        criteria_set: QuerySet[Criteria] = category.criteria_set.all()
        score_list = []
        for criteria in criteria_set:
            score_list.append({'criteria': criteria.id, 'criteria_name': criteria.name})
        score_formset = ScoreFormSet(initial=score_list)
        return self.render_to_response({'score_formset': score_formset})
    
    def post(self, request: HttpRequest, *args, **kwargs):
        product = Product.objects.get(pk=kwargs['pk'])

        if not request.user.is_superuser and product.review_set.filter(user = request.user).exists():
            return redirect('product_detail', pk=kwargs['pk'])

        text = request.POST['text']
        review = Review(user=request.user, product=product, text=text)
        review.save()

        score_formset = ScoreFormSet(request.POST)   
        
        if score_formset.is_valid():
            for form in score_formset:
                data = form.cleaned_data
                criteria = Criteria.objects.get(pk=data.get('criteria'))
                value = data.get('value')
                score = Score(criteria=criteria, review = review, value = value)
                score.save()
        
        for file in request.FILES.getlist('photo'):
            if not file.content_type.startswith('image'):
                continue

            photo = Photo()
            photo.review = review
            image_bytes = BytesIO(file.read())
            photo.image.save(file.name, File(image_bytes))
            photo.save()

        return redirect('product_detail', pk=kwargs['pk'])

    
