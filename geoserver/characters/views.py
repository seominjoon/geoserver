import json

from django.core.urlresolvers import reverse
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from django.views.generic.list import ListView

from characters.forms import CharacterForm
from characters.models import Character


# Create your views here.
class CharacterListView(ListView):
    '''
    Display all characters
    '''
    model = Character
    context_object_name = 'character_list'
    
class CharacterUploadView(View):
    def post(self, request):
        form = CharacterForm(request.POST, request.FILES)
        if form.is_valid():
            # Actions
            form.save()
            
            # Views
            if 'html' in request.POST and request.POST['html'] == 'false':
                return HttpResponse('success')
            else:
                data = {'title': 'Success',
                        'message': 'Character uploaded successfully.',
                        'link': reverse('characters-list'),
                        'linkdes': 'Go to character list page.'}
                return render(request, 'result.html', data)
        else:
            # Do nothing
            
            # Views
            if 'html' in request.POST and request.POST['html'] == 'false':
                return HttpResponse('failure')
            else:
                data = {'title': 'Failed',
                        'message': 'Character upload failed',
                        'link': reverse('characters-upload'),
                        'linkdes': 'Upload character again.'}
                return render(request, 'result.html', data)
            
    def get(self, request):
        form = CharacterForm()
        data = {'form': form, 'title':'Upload a character'}
        return render(request, 'upload_form.html', data)
   
def get_characters(query):
    if query == 'all':
        return Character.objects.all()
    else:
        try:
            int(query)
        except:
            raise Exception('query must be an integer')
        return [Character.objects.get(pk=int(query))]
     
    
class CharacterUpdateView(View):
    def get(self, request, query):
        forms = [CharacterForm(prefix=character.pk, instance=character)
                 for character in get_characters(query)]
        data = {'title':'Update characters', 'forms':forms}
        return render(request, 'characters/character_update_form.html', data)
    
    def post(self, request, query):
        forms = [CharacterForm(request.POST, prefix=character.pk, instance=character)
                 for character in get_characters(query)]
        if all([form.is_valid() for form in forms]):
            [form.save() for form in forms]
            data = {'title': 'Success',
                    'message': 'Characters updated successfully.',
                    'link': reverse('characters-list'),
                    'linkdes': 'Go to character list page.'}
            return render(request, 'result.html', data)
        data = {'title': 'Failure',
                'message': 'Character update failed.',
                'link': reverse('characters-update', query),
                'linkdes': 'Go back to update page.',}
        return render(request, 'result.html', data)
    
class CharacterDeleteView(DeleteView):
    model = Character
    slug_field = 'pk'
    
    def delete(self, request, *args, **kwargs):
        # Actions
        self.object = self.get_object()
        self.object.delete()
        
        # Views
        if 'html' in request.POST and request.POST['html'] == 'false':
            return HttpResponse('success')
        else:
            data = {'title': 'Success',
                    'message': 'Character deleted successfully.',
                    'link': reverse('characters-list'),
                    'linkdes': 'Go to character list page.',
                    }
            return render(request, 'result.html', data)
        
class CharacterDownloadView(View):
    '''
    CharacterDownloadView is similar to CharacterListView,
    except that download returns JSON while list returns HTML.
    '''
    def get(self, request, query):
        
        if query == 'all':
            objects = Character.objects.all()
        else:
            try:
                int(query)
            except:
                raise Exception('query must be an integer.')
            objects = [Character.objects.get(pk=int(query))]

        data = [{'pk':character.pk, 
                 'image_url': request.build_absolute_uri(character.image.url), 
                 'label':character.label} for character in objects]

        text = json.dumps(data)
        return HttpResponse(text)
    

class CharacterDetailView(DetailView):
    model = Character
    context_object_name = 'character'
    slug_field = 'pk'
        
        