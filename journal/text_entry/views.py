from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Entry
from .forms import EntryForm

# Create your views here.
def index(request):
	entries = Entry.objects.all().order_by('-pub_date')
	return render(request, 'text_entry\index.html', {
		'entries':entries
	})

def entry_details(request, entry_slug):
	try:
		selected_entry = Entry.objects.get(slug=entry_slug)
		return render(request, 'text_entry\entry_details.html', {
			'entry_found':True,
			'entry_image':selected_entry.image,
			'entry_title':selected_entry.title,
			'entry_date':selected_entry.pub_date,
			'entry_text':selected_entry.entry_text
		})
	except Exception as exc:
		return render(request, 'text_entry\entry_details.html', {
			'entry_found':False
		})

def new_entry(request):
	if request.method == 'POST':
		entry_form = EntryForm(request.POST, request.FILES)
		if entry_form.is_valid():
			entry = entry_form.save()
			return redirect('entry-detail', entry.slug)
		messages.error(request, 'Something went wrong, make sure you put a title and uploaded an image!')
	entry_form = EntryForm()
	return render(request, 'text_entry/new_entry.html', {
		'form':entry_form,
	})