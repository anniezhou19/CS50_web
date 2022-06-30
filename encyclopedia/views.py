from pickle import TRUE
import secrets
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.contrib import messages
from . import util
from markdown2 import Markdown

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Entry title")
    content = forms.CharField(widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    markdowner = Markdown()
    entryPage = util.get_entry(entry)
    if entryPage is None:
        return render(request, "encyclopedia/nonExistingEntry.html", {
            "entryTitle": entry
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry":markdowner.convert(entryPage),
            "entryTitle": entry
        })

def search(request):
    search_title = request.GET['q'].upper()
    entries = util.list_entries()
    search_result = []

    for entry in entries:
        if search_title == entry.upper():
            return HttpResponseRedirect(reverse("entry", args=[search_title]))
        else:
            if search_title in entry.upper():
                search_result.append(entry)
                return render(request, "encyclopedia/search.html", {
                    "search_result": search_result
                })
    return render(request, "encyclopedia/nonExistingEntry.html", {
        "entryTitle": search_title
    })

def newpage(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if(util.get_entry(title) is None):
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("entry", args=[title]))  
            else:
                messages.error(request, f"A page {title} already exists. Try another title below.")
                return HttpResponseRedirect(reverse("newpage"))
        else:
            return render(request, "encyclopedia/newpage.html", {
                "form": form
            })
    else:
        return render(request, "encyclopedia/newpage.html", {
            "form": NewEntryForm()
        })

def edit(request, entry):
    content = util.get_entry(entry)
    initial = {"title": entry, "content": content}
    form =NewEntryForm(initial=initial)

    if request.method == "POST":
        form = NewEntryForm(request.POST, initial=initial)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("entry", args=[title]))
        else:
            messages.error(request, "All fields are required!")
            return HttpResponseRedirect(reverse("edit", kwargs={'title':title}))
    else:
        return render(request, "encyclopedia/edit.html", {
            "form": form,
            "title": entry
        })

def random(request):
    entries = util.list_entries()
    RandomEntry = secrets.choice(entries)
    return HttpResponseRedirect(reverse("entry", args=[RandomEntry]))
    