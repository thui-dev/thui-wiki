from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.http import HttpResponse
from django import forms
from random import *

import markdown2
from . import util


class CreateEntry(forms.Form):
    title = forms.CharField(label="title")
    content = forms.CharField(label="content")


class Search(forms.Form):
    q = forms.CharField(label="q")


def index(request):
    if request.method == "GET":
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })

def search(request):
    if request.method == 'POST':
        i = []
        form = Search(request.POST)
        q = form.data['q']

        if util.get_entry(q):
            return redirect('wiki/'+q)

        for _ in util.list_entries():
            if q in _.lower():
                i.append(_)

        return render(request, "encyclopedia/search.html", {
        "entries": i
        })

def wiki(request, title):
    if util.get_entry(title):
        return render(request, "encyclopedia/entry.html", {
            "page": mark_safe(markdown2.markdown(util.get_entry(title))),
            "title": title
            })
    else:
        return render(request, "encyclopedia/error.html",{
            "message": "requested page was not found."
        })

def create(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create.html")
    else:
        form = CreateEntry(request.POST)

        if util.get_entry(form.data['title']):
            return render(request, "encyclopedia/error.html",{
                "message": "this entry already exists!"
            })

        util.save_entry(form.data['title'], form.data['content'])
        return render(request, "encyclopedia/thanks.html")

def edit(request, title):
    if request.method == "GET":
        return render(request, "encyclopedia/edit.html",{
            'title':title,
            'content': util.get_entry(title)
        })
    else:
        form = CreateEntry(request.POST)
        util.save_entry(form.data['title'], form.data['content'])
        return render(request, "encyclopedia/thanks.html")

def random(request):
    return redirect("wiki", choice(util.list_entries()))
