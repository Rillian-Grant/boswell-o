from django.shortcuts import render

import re

from .models import Entry
from .forms import SearchForm

def main(request):
    def get_content_with_tag_links(entry):
        entry.content = entry.get_content_with_tag_links()

        return entry 

    #### TODO: Change so that you don't waste power getting all entries
    entries = Entry.objects.all()

    form = SearchForm(request.GET)
    if form.is_valid():
        tags = re.findall("#\w+", form.cleaned_data["search"])

        for i in range(0, len(tags)):
            if tags[i][0] == '#':
                tags[i] = tags[i][1:]
                
        for tag in tags:
            entries = entries.filter(tag__tag_text=tag)

    if "search" in request.GET:
        compleated_search = request.GET["search"]
    else:
        compleated_search = ""

    # TODO: Change to use lambda function
    return render(request, "boswellCore/index.html", {
        "entries": map(get_content_with_tag_links, entries),
        "search": SearchForm(initial={"search": compleated_search})
    })