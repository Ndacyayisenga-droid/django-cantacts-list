from django.shortcuts import render, redirect
from django.http import Http404
from .models import Contact

# Create your views here.

def index(request):
    contacts = Contact.objects.all()
    search_input = request.GET.get('search-area')
    if search_input:
        contacts = contacts.filter(full_name__icontains=search_input)
    return render(request, 'index.html', {'contacts': contacts, 'search_input': search_input})

def addContact(request):
    if request.method == 'POST':
        try:
            new_contact = Contact(
                full_name=request.POST['fullname'],
                relationship=request.POST['relationship'],
                email=request.POST['email'],
                phone_number=request.POST['phone-number'],
                address=request.POST['address'],
            )
            new_contact.save()
            return redirect('/')
        except Exception as e:
            # Handle error (e.g., display error message)
            pass
    return render(request, 'new.html')

def editContact(request, pk):
    try:
        contact = Contact.objects.get(id=pk)
    except Contact.DoesNotExist:
        raise Http404("Contact not found")

    if request.method == 'POST':
        contact.full_name = request.POST['fullname']
        contact.relationship = request.POST['relationship']
        contact.email = request.POST['email']
        contact.phone_number = request.POST['phone-number']
        contact.address = request.POST['address']
        contact.save()
        return redirect('/profile/'+str(contact.id))
    return render(request, 'edit.html', {'contact': contact})

def deleteContact(request, pk):
    try:
        contact = Contact.objects.get(id=pk)
    except Contact.DoesNotExist:
        raise Http404("Contact not found")

    if request.method == 'POST':
        contact.delete()
        return redirect('/')
    return render(request, 'delete.html', {'contact': contact})

def contactProfile(request, pk):
    try:
        contact = Contact.objects.get(id=pk)
    except Contact.DoesNotExist:
        raise Http404("Contact not found")
    return render(request, 'contact-profile.html', {'contact':contact})
