from django.shortcuts import render, redirect
from django import forms

from . import util
import random
from markdown2 import Markdown

markdowner = Markdown()

class NewSearchForm(forms.Form):
    search = forms.CharField(label='', widget=forms.TextInput(attrs={
        "placeholder":"Search Encyclopedia"}))

class NewEntryForm(forms.Form):
    title = forms.CharField(label='')
    entry = forms.CharField(label='', widget=forms.Textarea(attrs={
        "class": "entry_form", "placeholder":"Enter your Markdown text here."}))


def index(request):
    if request.method == "POST":
        form = NewSearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data["search"]
            exact_entry = util.get_entry(search)
            if not exact_entry:
                custom_list = []
                for name in util.list_entries():
                    if search in name:
                        custom_list.append(name)
                return render(request, "encyclopedia/search_results.html", {
                    "keyword":search,
                    "entries":custom_list
                })
            return entry(request, search)
        else:
            return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries(),
                "form": form
            })
        
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewSearchForm()
    })

def entry(request, name):
    entry = util.get_entry(name)
    conv_entry = markdowner.convert(entry)
    return render(request, "wiki/entry.html", {
        "entry": conv_entry,
        "name": name
    })

def random_page(request):
    rp = random.choice(util.list_entries())
    return redirect("entry", name=rp)

def create_page(request):
    if request.method == "POST":
        entry_form = NewEntryForm(request.POST)
        if entry_form.is_valid():
            title = entry_form.cleaned_data["title"]
            content = entry_form.cleaned_data["entry"]
            check = util.get_entry(title)
            if check:
                message = "Page with this title already exists."
                return render(request, "encyclopedia/create.html", {
                "entryform":entry_form,
                "message":message
            })
            else:
                util.save_entry(title, content)
                return entry(request, title)
        else:
            return render(request, "encyclopedia/create.html", {
                "entryform":entry_form,
                "messages": None
            })
    return render(request, "encyclopedia/create.html", {
        "entryform":NewEntryForm(),
        "messages": None
    })

def edit_page(request, name):
    content = util.get_entry(name)
    form = NewEntryForm(initial={'title':name, 'entry':content})
    if request.method == "POST":
        entry_form = NewEntryForm(request.POST)
        if entry_form.is_valid():
            title = entry_form.cleaned_data["title"]
            content = entry_form.cleaned_data["entry"]
            util.save_entry(title, content)
            return entry(request, title)
        else:
            return render(request, "wiki/edit.html", {
                "entryform":entry_form,
                "name":name
            })
    return render(request, "wiki/edit.html", {
        "entryform":form,
        "name":name
    })
    