import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.views import generic
from django.http import HttpResponseRedirect
from django.contrib.auth import (
    login,
    authenticate,
    logout,
)
from django.urls import reverse
from catalog.forms import (
    SignUpForm,
    LoginForm,
    PasswordSetForm,
    EditProfileForm,
    ContactForm,
    RenewBookForm,
)
from catalog.models import Book, Author, Language, BookInstance, MyUser

class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)

# Create your views here.


# @login_required
def index(request):
  return render(request, 'index.html', {})

@login_required(login_url='login')
def locallibrary(request):

    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()
    num_languages = Language.objects.count()

    # Number of visits to this view, as counted in the session variable
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_languages': num_languages,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render (request, 'locallibrary.html', context = context)


class BookListView(generic.ListView):
    # login_url = 'login'
    model = Book
    paginate_by = 10
    # context_object_name = 'my_book_list'    # This is changed name for the list as a template variable. By default the generic views look for templates in /application_name(catalog)/the_model_name_list.html(book_list.html).
    # queryset = Book.objects.filter(title_icontains='programming')[:5]   # Get the first 5 books containing the keyword 'programming'
    # template_name = 'books/my_arbitrary_template_name_list.html'    # Specifying your own template name/location


class BookDetailView(generic.DetailView):
    model = Book

# Create the list view of authors
class AuthorListView(generic.ListView):
    model = Author

class AuthorDetailView(generic.DetailView):
    model = Author

class UserView(generic.DetailView):
    model = MyUser
    template_name = 'catalog/user.html'

def login_view(request):
    if request.method == 'POST':
        next = request.GET.get('next')
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            login(request, user)
            if next:
                return redirect(next)
            return redirect('locallibrary')

    else:
        form = LoginForm()

    context = {
        'form': form
    }
    return render(request, 'login.html', context)


# SignUp view
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # form.clean_password2()
            user = form.save(commit=False)
            # email = form.cleaned_data.get('email')
            password = form.clean_password2()
            user.set_password(password)
            user.save()
            new_user = authenticate(email=user.email, password=password)
            login(request, new_user)
            return redirect('locallibrary')

    else:
        form = SignUpForm()

    context = {
        'form': form,
    }
    return render(request, 'signup.html', context=context)

# Logout view
def logout_view(request):
    logout(request)
    return redirect('index')


def reset_view(request):
    if request.method == 'POST':
        form = PasswordSetForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.clean_password2()
            user.set_password(password)
            user.save()
            return redirect('reset/done/')
    else:
        form = PasswordSetForm()
    context = {
        'form':form,
    }

    return render(request, 'password_reset_form.html', context=context)


# Edit Profile View
@login_required(login_url='login')
def edit_profile_view(request, pk):
    user = get_object_or_404(MyUser, pk = pk)

    # If this is the POST request then process the Form data
    if request.method == 'POST':
        # Create a new form instance and populate it with data from the request (binding):
        form = EditProfileForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # Process the data in form.cleaned_data as required (here and just write it to the corresponding MyUser model)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.date_of_birth = form.cleaned_data['date_of_birth']
            user.save()

            # Redirect to the profile URL
            return HttpResponseRedirect(reverse('user', args=[pk]))

    # If this is the GET (or any other method) create the default form
    else:
        first_name = user.first_name;
        last_name = user.last_name;
        email = user.email;
        date_of_birth = user.date_of_birth;
        form = EditProfileForm(initial = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'date_of_birth': date_of_birth,
        })

    context = {
        'form': form,
        'user': user,
    }

    return render(request, 'catalog/my_account.html', context = context)


# Contact view
@login_required(login_url='login')
def contact(request):

    # If this is the POST request method then process the data
    if request.method == 'POST':
        form = ContactForm(request.POST)

        # Check if the form is valid
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            return HttpResponseRedirect(reverse('contact-success'))

        # If this is a GET ( or any other method ) create the default form
    else:
        form = ContactForm()

    context = {
        'form': form,
    }

    return render(request, 'contact.html', context=context)

def about(request):
    # The "About Page" for knowing more about the library

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()
    num_languages = Language.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_languages': num_languages,
    }

    # Render the HTML template index.html with the data in the context variable
    return render (request, 'about.html', context = context)


@permission_required('catalog.is_admin')
def renew_book_librarian(request, id):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    form = RenewBookForm(request.POST)

    # Check if the form is valid:
    if form.is_valid():
        # Process the data in form.cleaned_data as required(we write the data to the model's due_back field)
        book_instance.due_back = form.cleaned_data['renewal_date']
        book_instance.save()

        # Redirect the new URL:
        return HttpResponseRedirect(reverse('all-borrowed'))

    # If this is a GET or any other method. Create the default form
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form.RenewBookForm(inital={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)
