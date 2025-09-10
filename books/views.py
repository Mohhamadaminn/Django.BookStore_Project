from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import Book
from .forms import CommentForm


class BooksListView(generic.ListView):
    model = Book
    paginate_by = 6
    template_name = 'books/book_list.html'
    context_object_name = 'books'

    
@login_required
def book_detail_view(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book_comments = book.comments.all()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.book = book
            new_comment.user = request.user
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, 'books/book_detail.html', {
        'book': book,
        'comments': book_comments,
        'comment_form': comment_form,
    })



class BooksCreateView(LoginRequiredMixin, generic.CreateView):
    model = Book
    fields = ['title', 'author', 'description', 'price', 'cover',]
    template_name = 'books/book_create.html'


    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class BookUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Book
    fields = ['title', 'author', 'description', 'price', 'cover', ]
    template_name = 'books/book_update.html'

    # set the condition that just let the owner of book edit it.
    def dispatch(self, request, *args, **kwargs):

        obj = self.get_object()
        if obj.user != request.user:
            return render(request, 'not_owner.html')    

        return super().dispatch(request, *args, **kwargs)


class BookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Book
    template_name = 'books/book_delete.html'
    success_url = reverse_lazy('book_list')

    # set the condition that just let the owner of book delete it.
    def dispatch(self, request, *args, **kwargs):

        obj = self.get_object()
        if obj.user != request.user:
            return render(request, 'not_owner.html')    

        return super().dispatch(request, *args, **kwargs)
    

    