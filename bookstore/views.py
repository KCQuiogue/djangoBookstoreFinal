from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic
from .models import Book, Cart, CartItem, Order, OrderItem


def book_list(request):
    query = request.GET.get('query', '')
    sort = request.GET.get('sort', 'newest')

    books = Book.objects.all()
    if query:
        books = books.filter(title__icontains=query) | books.filter(author__icontains=query)

    if sort == 'newest':
        books = books.order_by('-date_added')  # assuming 'date_added' field exists
    elif sort == 'oldest':
        books = books.order_by('date_added')  # assuming 'date_added' field exists
    elif sort == 'alphabetical':
        books = books.order_by('title')
    elif sort == 'reverse_alphabetical':
        books = books.order_by('-title')
    elif sort == 'price_low_high':
        books = books.order_by('unitPrice')
    elif sort == 'price_high_low':
        books = books.order_by('-unitPrice')
    # Add other sorting logic as needed

    return render(request, 'bookstore/book_list.html', {'books': books})


@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)

    if not created:
        cart_item.quantity += 1
    else:
        messages.success(request, 'Item added to cart successfully!')

    cart_item.save()

    return redirect('book_list')


# region Shopping Cart
@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)
    total_price = sum(item.quantity * item.book.unitPrice for item in cart_items)
    return render(request, 'bookstore/cart.html', {'cart_items': cart_items, 'total_price': total_price})


@login_required
def update_cart(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        action = request.POST.get('action')

        if action == 'increase':
            item.quantity += 1
        elif action == 'decrease':
            if item.quantity > 1:
                item.quantity -= 1
            else:
                item.delete()

        item.save()
    return redirect('view_cart')


@login_required
def remove_from_cart(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        item.delete()
    return redirect('view_cart')
# endregion


# region Inventory
class BookList(generic.ListView):
    model = Book
    context_object_name = 'books'
    template_name = 'bookstore/book_index.html'


class BookDetail(generic.DetailView):
    model = Book
    context_object_name = 'book'


class BookCreate(generic.CreateView):
    model = Book
    fields = ['image', 'title', 'author', 'description', 'unitPrice']
    success_url = reverse_lazy('books')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Book was added successfully.")
        return super(BookCreate, self).form_valid(form)


class BookUpdate(generic.UpdateView):
    model = Book
    fields = ['image', 'title', 'author', 'description', 'unitPrice']
    success_url = reverse_lazy('books')

    def form_valid(self, form):
        messages.success(self.request, "Book was updated successfully.")
        return super(BookUpdate, self).form_valid(form)


class BookDelete(generic.DeleteView):
    model = Book
    context_object_name = 'book'
    template_name = 'bookstore/book_delete.html'
    success_url = reverse_lazy('books')

    def form_valid(self, form):
        messages.success(self.request, "Book was deleted successfully.")
        return super(BookDelete, self).form_valid(form)
# endregion

# Ordering

def create_order(request):
    if request.method == 'POST':
        cart_items = CartItem.objects.filter(cart__user=request.user)

        order = Order.objects.create(user=request.user, total_price=0)
        total_price = 0

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                book=item.book,
                quantity=item.quantity,
                price=item.book.unitPrice
            )
            total_price += item.book.unitPrice * item.quantity

        order.total_price = total_price
        order.save()

        cart_items.delete()

        return redirect('order_confirmation')

    return redirect('cart')


@login_required
def purchase_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'bookstore/purchase_history.html', {'orders': orders})


def order_confirmation(request):
    return render(request, 'bookstore/order_confirmation.html')
