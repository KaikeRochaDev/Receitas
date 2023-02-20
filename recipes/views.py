from django.shortcuts import render, get_list_or_404, get_object_or_404
from .models import Recipe
from django.http import Http404
from django.core.paginator import Paginator
from django.db.models import Q

def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    
    current_page = request.GET.get('page', 1)
    paginator = Paginator(recipes, 9)
    page_obj = paginator.get_page(current_page)
    
    return render(request, 'recipes/pages/home.html', {'recipes': page_obj})

def category(request, category_id):
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id, 
            is_published=True, 
        ).order_by('-id')
    )
    
    return render(request, 'recipes/pages/category.html', {
        'recipes': recipes, 
        'title': f'{recipes[0].category.name} - Categoria | '})

def recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id, is_published=True,)

    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': recipe,
        'is_detail_page': True,
    })
    
def search(request):
    search_term = request.GET.get('q', '').strip()
    
    if not search_term:
        raise Http404()
    
    recipes = Recipe.objects.filter(
        Q(
            Q(title__contains=search_term) | 
            Q(description__contains=search_term),
        ),
        is_published=True
    ).order_by('-id')
    
    return render(request, 'recipes/pages/search.html', {'page_title': f'Pesquisa por "{search_term}" |', 'search_term': search_term, 'recipes': recipes})