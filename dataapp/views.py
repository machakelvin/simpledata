from django.shortcuts import render, redirect, get_object_or_404
from .models import Entry
from .forms import EntryForm, UserRegisterForm
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from django.conf import settings
LOW_QUANTITY = settings.LOW_QUANTITY
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required

# Home view
def home(request):
    return render(request, 'index.html')



@login_required
def filter_data(request):
    category = request.GET.get('category', '')
    date = request.GET.get('date', '')
    entries = Entry.objects.all()

    # Apply filters if provided
    if category:
        entries = entries.filter(category__icontains=category)
    if date:
        entries = entries.filter(date=date)

    return render(request, 'filter.html', {'entries': entries})

# Entry Detail view
def entry_detail(request, id):
    entry = get_object_or_404(Entry, id=id)
    return render(request, 'detail.html', {'entry': entry})

from django.shortcuts import render, redirect
from .models import Entry
from django.contrib.auth.decorators import login_required
from django.utils import timezone

@login_required  
def add_entry(request):
    if request.method == 'POST':
        # Retrieve data from the form
        name = request.POST.get('name')
        category = request.POST.get('category')
        date = request.POST.get('date')
        quantity = request.POST.get('number')
        details = request.POST.get('details')

        # Create and save the new Entry object
        entry = Entry(name=name, category=category, date=date, quantity=quantity, details=details)
        entry.save()

        # Redirect to a success page or another view
        return redirect('dashboard')  # Change 'entry_list' to your target view name

    return render(request, 'add.html')

    
class SignupView(View):
    def get(self, request,):
        form = UserRegisterForm()
        return render(request, 'register.html', {'form': form})
    
    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            return redirect('index')
        return render(request, 'dataapp/register.html', {'form': form})
    
    



class Dashboard(LoginRequiredMixin,View):
    def get(self, request):
        items = Entry.objects.filter(user=self.request.user.id).order_by('id')
        
        low_inventory = Entry.objects.filter(
            user=self.request.user.id, 
            quantity__lte= LOW_QUANTITY
             )
        if low_inventory.count() > 0:
            if low_inventory.count() > 1:
                messages.error(request, f'{low_inventory.count()} items are running low on inventory')
            else:
                messages.error(request, f'{low_inventory.count()} item is running low on inventory')    
        
        low_inventory_ids = Entry.objects.filter(
            user=self.request.user.id, 
            quantity__lte= LOW_QUANTITY
             ).values_list('id', flat=True)
        
        return render(request, 'dashboard.html', {'items': items, 'low_inventory_ids': low_inventory_ids})
     
     



class CustomLoginView(LoginView):
    template_name = 'inventory/login.html'  # Replace with your actual login template path

    def form_valid(self, form):
        # Call the parent class's form_valid method
        super().form_valid(form)
        
        # Redirect based on the user's role
        if self.request.user.is_superuser:
            return redirect('/admin/')  # Redirect to Django admin page
        else:
            return redirect('dashboard') # Redirect to the dashboard for normal users
        
        
        
        

@login_required
def edit_entry(request, entry_id):
    # Retrieve the existing entry or raise a 404 error if it doesn't exist
    entry = get_object_or_404(Entry, id=entry_id)

    if request.method == 'POST':
        # Update entry with new data from the form
        entry.name = request.POST.get('name')
        entry.category = request.POST.get('category')
        entry.date = request.POST.get('date')
        entry.quantity = request.POST.get('number')
        entry.details = request.POST.get('details')
        entry.save()

        # Redirect to the dashboard or another view after updating
        return redirect('dashboard')  # Change 'dashboard' to your target view name

    # Render the edit form with the current entry data
    return render(request, 'entry_form.html', {'entry': entry})
    
    
    
class DeleteItem(LoginRequiredMixin, DeleteView):
    model = Entry
    template_name = 'delete.html'
    success_url = reverse_lazy('dashboard')
    context_object_name = 'item'
    