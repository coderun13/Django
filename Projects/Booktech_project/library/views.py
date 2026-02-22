from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from .forms import AuthorForm, BookForm,BookFormwithoutauthor, BookFormwithoutauthorandpublisher, PublisherForm
from library.models import Author, Book
from django.views.generic import DetailView, ListView

# Create your views here.
def index(request):
    return HttpResponse("Welcome to the Library app!")

#two types of views: FBV9(function based views) and CBV(class based views)
#function based view
def book_list(request):
    books= Book.objects.all() 

    context= {
        'books': books
    }
    return render(request, 'library/book_list.html', context)


# class based view
from django.views import View
class BookListView(ListView):
    model = Book
    template_name = 'library/cbv_book_list.html'
    context_object_name = 'books'


# book detail view
# function based view
def book_detail(request, book_id):
    book= get_object_or_404(Book, id=book_id)
    context= {
        'book': book
    }
    return render(request, 'library/book_detail.html', context)


# class based view
class BookDetailView(DetailView):
    model= Book
    context_object_name= 'book'
    template_name= 'library/book_detail.html'

# books by author view
def books_by_author(request, author_id):
    author=get_object_or_404(Author, id=author_id)
    books= Book.objects.filter(author=author)
    context= {
        'books': books,
        'author': author
    }
    return render(request, 'library/books_by_author.html', context)


# author list view
def author_list(request):
    authors= Author.objects.all()
    context= {
        'authors': authors
    }
    return render(request, 'library/author_list.html', context)

# add book view
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list_fbv')
    else:
        form = BookForm()
    
    context = {
        'form': form
    }
    return render(request, 'library/add_book.html', context)

# add book and author
def add_book_and_author(request):
    if request.method == 'POST':
        book_form = BookFormwithoutauthor(request.POST)
        author_form = AuthorForm(request.POST)
        if book_form.is_valid() and author_form.is_valid():
            author = author_form.save()
            book = book_form.save(commit=False)
            book.author = author
            book.save()
            return redirect('book_list_fbv')
    else:
        book_form = BookFormwithoutauthor()
        author_form = AuthorForm()
    
    context = {
        'book_form': book_form,
        'author_form': author_form
    }
    return render(request, 'library/add_book_and_author.html', context)


# add book publisher view(in this I want to add book along with author and publisher(no drop down for publisher))
def add_book_with_author_publisher(request):
    if request.method == 'POST':
        book_form = BookFormwithoutauthorandpublisher(request.POST)
        author_form = AuthorForm(request.POST)
        publisher_form = PublisherForm(request.POST)

        if book_form.is_valid() and author_form.is_valid() and publisher_form.is_valid():
            author = author_form.save()
            publisher = publisher_form.save()

            book = book_form.save(commit=False)
            book.author = author
            book.publisher = publisher
            book.save()

            return redirect('book_list_fbv')
    else:
        book_form = BookFormwithoutauthorandpublisher()
        author_form = AuthorForm()
        publisher_form = PublisherForm()

    return render(request, 'library/add_book_with_author_publisher.html', {
        'book_form': book_form,
        'author_form': author_form,
        'publisher_form': publisher_form
    })