import datetime
from django.shortcuts import render
from django.views import generic
from django.shortcuts import get_object_or_404
from django.http import request
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Author
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Author, Book, BookInstance
from catalog.form import RenewBookForm

# Create your views here.


@login_required
def index(request):
    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(
        status__exact='a').count()
    # The 'all()' is implied by default.
    num_authors = Author.objects.count()
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits
    }

    return render(request, 'index.html', context=context)


class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    paginate_by = 2
    # your own name for the list as a template variable
    context_object_name = 'book_list'
    queryset = Book.objects.all()[:5]  # Get 5 books containing the title war
    template_name = 'book_list.html'  # Specify your own template name/location


# def book_detail_view(request, pk):
#     book = get_object_or_404(Book, pk=pk)
#     return render(request, 'book_detail.html', context={'book': book})

class book_detail_view(generic.DetailView):
    model = Book
    template_name = 'book_detail.html'


class AuthorsListView(LoginRequiredMixin, generic.ListView):
    model = Author
    paginate_by = 5
    context_object_name = 'authors_list'
    queryset = Author.objects.all()
    template_name = 'authors_list.html'


class author_detail_view(generic.DetailView):
    model = Author
    context_object_name = 'author'
    template_name = 'author_detail.html'


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class LoanedBookListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    template_name = 'bookinstance_list_borrowed_staff.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if(request.method == 'POST'):
        form = RenewBookForm(request.POST)

        if (form.is_valid()):
            book_instance.due_back = form.cleaned_data['renewl_date']

            book_instance.save()

            return HttpResponseRedirect(reverse('borrowed') )

    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewl_date': proposed_renewal_date})

    context = {
            'form': form,
            'book_instance' : book_instance,
            }

    return render(request,'book_renew_librarian.html', context)


class AuthorCreate(PermissionRequiredMixin,CreateView):
    permission_required = 'catalog.can_mark_returned'
    model = Author
    fields =['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/06/2020'}



class AuthorUpdate(PermissionRequiredMixin,UpdateView):
    permission_required = 'catalog.can_mark_returned'
    model = Author
    fields = '__all__'


class AuthorDelete(PermissionRequiredMixin ,DeleteView):
    permission_required = 'catalog.can_mark_returned'
    model = Author
    success_url = reverse_lazy('authors')


class BookCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'catalog.can_mark_returned'
    model = Book
    fields = '__all__'


class BookUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.can_mark_returned'
    model = Book
    fields = '__all__'


class BookDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'catalog.can_mark_returned'
    model = Book
    success_url = reverse_lazy('books')
