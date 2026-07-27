from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Product, Category, Review, Wishlist, HeroBanner
from django.db.models import Q


def home(request):
    featured_products = Product.objects.filter(
        available=True,
        featured=True
    )[:8]

    categories = Category.objects.all()

    return render(request, "products/home.html", {
        "featured_products": featured_products,
        "categories": categories,
    })


def product_list(request):
    products = Product.objects.filter(available=True)
    categories = Category.objects.all()
    query = request.GET.get('q')
    category_slug = request.GET.get('category')

    if query:
        products = products.filter(name__icontains=query)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories,
        'query': query,
        'category_slug': category_slug,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    reviews = product.reviews.all()
    user_review = None
    if request.user.is_authenticated:
        user_review = Review.objects.filter(product=product, user=request.user).first()

    in_wishlist = False

    if request.user.is_authenticated:
        in_wishlist = Wishlist.objects.filter(
            user=request.user,
            product=product
        ).exists()

    related_products = Product.objects.filter(
        category=product.category, available=True
    ).exclude(id=product.id)[:4]

    images = product.images.all()

    return render(request, "products/product_detail.html", {
        "product": product,
        "reviews": reviews,
        "user_review": user_review,
        "related_products": related_products,
        "images": images,
        "in_wishlist": in_wishlist,
    })


@login_required
def add_review(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        Review.objects.update_or_create(
            product=product,
            user=request.user,
            defaults={'rating': rating, 'comment': comment}
        )
        messages.success(request, 'Your review has been submitted!')
    return redirect('product_detail', slug=slug)

@login_required
def toggle_wishlist(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    wishlist_item = Wishlist.objects.filter(
        user=request.user,
        product=product
    )

    if wishlist_item.exists():
        wishlist_item.delete()
        liked = False
    else:
        Wishlist.objects.create(
            user=request.user,
            product=product
        )
        liked = True

    count = Wishlist.objects.filter(user=request.user).count()

    return JsonResponse({
        "liked": liked,
        "count": count
    })

@login_required
def wishlist(request):

    items = Wishlist.objects.filter(
        user=request.user
    ).select_related("product")

    return render(
        request,
        "products/wishlist.html",
        {
            "items": items
        }
    )

def search_products(request):

    query = request.GET.get("q", "")

    products = Product.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query),
        available=True
    )[:8]

    data = []

    for product in products:

        data.append({
            "name": product.name,
            "price": str(product.price),
            "url": product.get_absolute_url(),
            "image": product.image.url if product.image else "",
        })

    return JsonResponse(data, safe=False)

def about(request):
    return render(request, "about.html")

def home(request):
    banner = HeroBanner.objects.filter(active=True).first()

    context = {
        "banner": banner,
    }

    return render(request, "products/home.html", context)