from django.views import View
from recipes.models import Recipe
from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from recipes.models import Recipe
from django.urls import reverse
from authors.forms.recipe_form import AuthorRecipeForm

class DashboardRecipe(View):
    def get_recipe(self, id=None):
        recipe = None
        
        if id is not None:
            self.request
            recipe = Recipe.objects.filter(is_published=False, author=self.request.user, id=id).first()
        
            if not recipe:
                raise Http404()
            
        return recipe
    
    def render_recipe(self, form):
        return render(self.request, 'authors/pages/dashboard_recipe.html', {'form': form})
    
    
    def get(self, request, id=None):
        recipe = self.get_recipe(id)
        form = AuthorRecipeForm(instance=recipe)
        return self.render_recipe(form)
    
    def post(self, request, id=None):
        recipe = self.get_recipe(id)
        
        form = AuthorRecipeForm(
            request.POST or None,
            files=request.FILES or None,
            instance=recipe,
        )
        
        if form.is_valid():
            recipe = form.save(commit=False)

            recipe.author = request.user
            recipe.preparation_steps_is_html = False
            recipe.is_published = False

            recipe.save()

            messages.success(request, 'Sua receita foi salva com sucesso!')
            return redirect(reverse('authors:dashboard_recipe_edit', args=(recipe.id,)))
        
        return self.render_recipe(form)