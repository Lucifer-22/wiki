from django.shortcuts import render
from django.http import HttpResponse
from markdown import Markdown #Some real tough thing to understand

from . import util

md = Markdown() #To oversome error

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def pages(request, name):
    page_name = util.get_entry(name)
#page_name returns the name of the page is exists in the entry or NONE.
    if page_name is None:
        return render(request, "encyclopedia/invalidPage.html", {
            "title": name.capitalize()
        })   

    return render(request, "encyclopedia/wikiPages.html", {
        "page": md.convert(page_name),
        "title": name
    })