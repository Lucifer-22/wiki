from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, request
from django.urls import reverse
from markdown import Markdown #Some real tough thing to understand
from django import forms
from random import randint

from . import util

md = Markdown() #To overcome error


class createPage(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'cols': 60}))
    description = forms.CharField(label="Description", widget=forms.Textarea(attrs={'cols': 120}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

#
def pages(request, name):
    page_name = util.get_entry(name)
        #page_name returns the name of the page is exists in the entry or NONE.
    if page_name is None:
        return render(request, "encyclopedia/invalidPage.html", {
            "title": name.capitalize()
        })
    body = md.convert(page_name)
    return render(request, "encyclopedia/wikiPages.html", {
        "body": body,
        "title": name
    })

def post_new(request):
    if request.method == "POST":
        form = createPage(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            if title not in util.list_entries():
                util.save_entry(title, description)
                return HttpResponseRedirect(reverse('pages', kwargs={
                'name': title
                }))
            else:
                description = {
                    'form': createPage(),
                    'message': f"Entry with {title} already available."
                }
            return render(request, 'encyclopedia/newpage.html', description)
    else:
        description = {
            'form':createPage()
        }
        return render(request, "encyclopedia/newpage.html", description)

def post_edit(request, name):
    if request.method == "POST":
        form = createPage(request.POST)
        description = request.POST.get('description')
        
        util.save_entry(name, description)
        return HttpResponseRedirect(reverse('pages', kwargs={'name': name }))
    else:
        form = createPage() # this will create empty form if it is a GET request
    description = {
        'title': name,
        'description': util.get_entry(name)
    }
    return render(request, "encyclopedia/edit.html", description)

def random(request):
    pages_list = util.list_entries()
    random_title = pages_list[randint(0, len(pages_list)-1)]
    return HttpResponseRedirect(reverse("pages", kwargs={'name': random_title}))



def search(request):
    searchItem = request.POST["item"]
    entries = util.list_entries()
    if searchItem in entries:
        return HttpResponseRedirect("wiki/"+searchItem)
    else:
        list = []
        for article in entries:
            if searchItem in article:
                list.append(article)
        return render(request, "encyclopedia/index.html", {
            "entries": list
        })