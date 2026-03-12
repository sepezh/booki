""" Import Libs and models """
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Prefetch, Count, Avg, Q, F, FloatField, ExpressionWrapper
from django.db import transaction
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils import timezone
from .utils import helper
from .models import Book, Category, Author, UserProfile, LibraryBook, Library, Reserve, Review
from .forms import HomeSearchField, LoginForm, RegisterForm, UserProfileForm, ReviewForm
from .decorators import redirect_login_user, ajax_required, librarian_required

User = get_user_model()


def home(request):
    """Home view"""
    latest = Book.objects.order_by('-created_at')[:6]
    return render(request, 'pages/home.html', {
        'page': 'home',
        'latest': latest
    })


def search(request) -> any:
    """ Search view """
    if 'query' in request.GET:
        form = HomeSearchField(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            book_list = Book.objects.filter(
                Q(title__icontains=query) |
                Q(authors__first_name__icontains=query) |
                Q(authors__last_name__icontains=query) |
                Q(isbn__icontains=query) |
                Q(tags__title__icontains=query) |
                Q(category__title__icontains=query)
            ).distinct()
            author_list = Author.objects.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            ).distinct()
            return render(request, 'pages/search.html', {
                'page': 'search',
                'books': book_list,
                'authors': author_list
            })
    return redirect('home')


@redirect_login_user()
def login_register(request) -> any:
    """Login and register view"""
    login_form = LoginForm(request.POST)
    reg_form = RegisterForm(request.POST)

    if request.method == 'POST':
        if 'register' in request.POST:
            if reg_form.is_valid():
                # create new user
                user = reg_form.save()

                # Log in the user
                login(request, user)

                # add success message
                messages.success(
                    request,
                    'Registration successful! You are now logged in.'
                )

                return redirect('home')
        else:
            if login_form.is_valid():
                username_email = login_form.cleaned_data['username_email']
                password = login_form.cleaned_data['password']

                user = User.objects.filter(
                    Q(username=username_email) | Q(email=username_email)).first()

                if user is not None and user.is_active is True:
                    user = authenticate(
                        request, username=user.username, password=password)

                if user is not None:
                    login(request, user)
                    if login_form.cleaned_data.get('remember_me'):
                        # 2 weeks in seconds
                        request.session.set_expiry(1209600)
                    else:
                        # Session will expire when the user closes the browser
                        request.session.set_expiry(0)
                    # Check user is librarian if True redirect to dashboard
                    if user.groups.filter(name='librarian').exists():
                        return redirect('dashboard')
                    # Redirect to a home page
                    return redirect('home')
                else:
                    messages.error(
                        request,
                        'Invalid credentials. Please try again.'
                    )

    return render(request, 'pages/login_register.html', {
        'page': 'login_register',
        'login_form': login_form,
        'reg_form': reg_form
    })


@login_required
def logout_user(request):
    """ Logout user """
    logout(request)
    return redirect('home')


@login_required
@csrf_exempt
def user_profile_edit(request):
    """ User profile edit """
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if user_profile_form.is_valid():
            if user_profile_form.check_valid_address():
                user_profile_form.save()
                messages.success(
                    request,
                    'Update successful! You are now able to reserve a book.'
                )
            else:
                user_profile_form = UserProfileForm(instance=user_profile)
                messages.error(
                    request,
                    'Address is not valid please provide a correct address.'
                )
    else:
        user_profile_form = UserProfileForm(instance=user_profile)

    return render(request, 'pages/user_profile_edit.html', {
        'page': 'account',
        'user_profile': user_profile,
        'user_profile_form': user_profile_form
    })


def categories(request):
    """Categories view"""
    book_queryset = Book.objects.order_by('-created_at')[:6]
    category_list = Category.objects.annotate(
        book_count=Count('book')
    ).filter(
        book_count__gt=0
    ).prefetch_related(
        Prefetch('book_set', queryset=book_queryset, to_attr='latest_books')
    ).all()

    return render(request, 'pages/categories.html', {
        'page': 'categories',
        'categories': category_list
    })


def category_detail(request, slug):
    """Category detail view"""
    category = get_object_or_404(Category, slug=slug)
    book_list = category.book_set.all()

    paginator = Paginator(book_list, 24)
    page_number = request.GET.get('page')
    books = paginator.get_page(page_number)

    return render(request, 'pages/category_detail.html', {
        'page': 'categories',
        'category': category,
        'books': books
    })


def authors(request):
    """ Authors view """
    author_list = Author.objects.all()

    paginator = Paginator(author_list, 24)
    page_number = request.GET.get('page')
    author_list = paginator.get_page(page_number)

    return render(request, 'pages/authors.html', {
        'page': 'authors',
        'authors': author_list
    })


def author_detail(request, slug):
    """ Author detail view """
    author_id = slug.split('-')[0]

    author = get_object_or_404(Author, id=author_id)
    book_list = author.book_set.all()

    return render(request, 'pages/author_detail.html', {
        'page': 'authors',
        'author': author,
        'books': book_list
    })


def book_detail(request, slug):
    """Book detail view"""
    book = get_object_or_404(Book, slug=slug)
    user_review = None
    user_profile = None
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            user_review = Review.objects.get(user=request.user, book=book)
        except UserProfile.DoesNotExist:
            user_profile = None
            user_review = None
        except Review.DoesNotExist:
            user_review = None

    reviews = book.review_set.all()
    average_rating = reviews.aggregate(Avg('rate'))['rate__avg'] or 0
    total_reviews = reviews.count()
    total_comment = reviews.select_related('user__userprofile').exclude(comment__isnull=True).exclude(comment='').count()
    filtered_reviews = reviews.select_related('user__userprofile').exclude(comment__isnull=True).exclude(comment='').order_by('-created_at')[0:10]

    return render(request, 'pages/book_detail.html', {
        'page': 'book_detail',
        'book': book,
        'user_review': user_review,
        'average_rating': average_rating,
        'total_reviews': total_reviews,
        'total_comment': total_comment,
        'reviews': filtered_reviews,
        'user_profile': user_profile
    })


@login_required
@csrf_exempt
def reserve(request):
    """ Reserve a book """
    if request.method == 'POST':
        try:
            book_slug = request.POST.get('book')
            library_book_id = request.POST.get('library-book')
            if not book_slug or not library_book_id:
                raise ValueError('Invalid Request.')
            library_book = LibraryBook.objects.get(id=library_book_id, book__slug=book_slug)
            if not library_book:
                raise ValueError('Invalid Request.')
            user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
            if not user_profile.address or not user_profile.zip_code or not user_profile.city or not user_profile.country:
                raise ValueError('Please update your profile.')
            longitude, latitude = user_profile.get_location()
            library_radius = pow(library_book.library.latitude - latitude, 2) + pow(library_book.library.longitude - longitude, 2)
            if library_radius > pow(10 / 9, 2):
                raise ValueError('Library is not in your range please select another one.')
            if library_book.quantity - 1 < 0:
                raise ValueError('Unfortunately, Library doesn\'t have anymore this book please check another one.')
            with transaction.atomic():
                seven_days = timezone.now() + timezone.timedelta(days=7)
                reservation = Reserve(user=request.user, book=library_book.book, library=library_book.library,
                                      status=Reserve.Status.PENDING, reject_at=seven_days)
                reservation.save()
                library_book.quantity -= 1
                library_book.save()
            messages.success(
                request,
                'Your book is waiting for you to pick up. (7 days)'
            )
            return redirect(f'user/reservation/{reservation.code}')

        except ValueError as e:
            messages.error(
                request,
                str(e)
            )
        except Exception as e:  # pylint: disable=broad-exception-caught
            messages.error(
                request,
                'An unexpected error occurred: ' + str(e)
            )

        return redirect('home')
    return redirect('home')


@login_required
def user_reservation(request, code):
    """ User reservation """
    reservation = get_object_or_404(Reserve, code=code, user=request.user)
    if Reserve.Status(reservation.status) is reservation.Status.PENDING and reservation.reject_at < timezone.now():
        reservation.status = Reserve.Status.REJECTED
        reservation.save()
    return render(request, 'pages/user_reservation.html', {
        'page': 'account',
        'reservation': reservation
    })


@login_required
def user_reservation_list(request):
    """ User reservation list """
    helper.update_pending_reservations(user=request.user)
    reservation_list = Reserve.objects.order_by('-created_at').filter(user=request.user)

    paginator = Paginator(reservation_list, 10)
    page_number = request.GET.get('page')
    reservations = paginator.get_page(page_number)

    return render(request, 'pages/user_reservation_list.html', {
        'page': 'account',
        'reservations': reservations
    })


@login_required
@csrf_exempt
def user_reservation_action(request, code):
    """ Action on reservation """
    if request.method == 'POST' and 'submit' in request.POST:
        reservation = get_object_or_404(Reserve, code=code, user=request.user)
        if request.POST.get('submit') == 'cancel' and Reserve.Status(reservation.status) is reservation.Status.PENDING:
            reservation.status = Reserve.Status.CANCELED
            reservation.save()

    return redirect('user_reservation', code=code)


@login_required
@ajax_required
def ajax_near_libraries(request):
    """ List of nearest 10km libraries """
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if user_profile.address and user_profile.zip_code and user_profile.city and user_profile.country:
        longitude, latitude = user_profile.get_location()
        message = 'success'
        radius_km = 10
        library_book_list = LibraryBook.objects.annotate(
            radius_sqr=ExpressionWrapper(
                pow(F('library__latitude') - latitude, 2) + pow(F('library__longitude') - longitude, 2),
                output_field=FloatField())
        ).order_by('radius_sqr').filter(
            Q(library__is_active=1)
            &
            Q(radius_sqr__lte=pow(radius_km / 9, 2))
            &
            Q(book__slug=request.GET.get('book'))
            &
            Q(quantity__gte=0)
        )
        view = render_to_string('ajax/library_book.html', {'library_book_list': library_book_list, 'book_slug': request.GET.get('book')}, request)
    else:
        message = 'update_profile'
        view = render_to_string('ajax/update_profile.html', {}, request)
    return JsonResponse({'message': message, 'view': view})


@ajax_required
def ajax_load_more_reviews(request, book_slug):
    """ Show more reviews """
    book = get_object_or_404(Book, slug=book_slug)
    per_page = 10
    page = int(request.GET.get('page', 2)) - 1
    current_count = (page - 1) * per_page
    reviews = book.review_set.exclude(comment__isnull=True).exclude(comment='').order_by('-created_at')[current_count:current_count + per_page]
    if reviews:
        message = 'success'
        view = render_to_string('components/review.html', {'reviews': reviews}, request)
    else:
        message = 'empty'
        view = ''
    return JsonResponse({'message': message, 'view': view})


@login_required
@csrf_exempt
def submit_review(request, book_slug):
    """ Submit review """
    # pylint: disable=unused-variable
    if request.method == 'POST':
        book = get_object_or_404(Book, slug=book_slug)
        form = ReviewForm(request.POST)
        if form.is_valid():
            review, created = Review.objects.update_or_create(
                book=book,
                user=request.user,
                defaults={
                    'rate': form.cleaned_data['rate'] if form.cleaned_data['rate'] <= 5 else 5,
                    'comment': form.cleaned_data['comment'] or None,  # Use None if comment is empty
                }
            )

            messages.success(
                request,
                'Review has been submitted successfully.'
            )

    return redirect('book_detail', slug=book_slug)


# Dashboard
@login_required
@librarian_required
def dashboard(request):
    """ Dashboard """

    library = Library.objects.get(staff=request.user)

    helper.update_pending_reservations(library=library)

    total_reservation = library.reserve_set.count()

    library_reserve = library.reserve_set
    if request.method == 'GET' and 'code' in request.GET:
        library_reserve = library_reserve.filter(code=request.GET.get('code'))

    paginator = Paginator(library_reserve.order_by('-created_at'), 10)
    page_number = request.GET.get('page')
    reservations = paginator.get_page(page_number)

    return render(request, 'pages/dashboard.html', {
        'page': 'dashboard',
        'library': library,
        'total_reservation': total_reservation,
        'reservations': reservations
    })


@login_required
@librarian_required
def dashboard_reservation_detail(request, code):
    """ Reservation detail dashboard  """
    library = Library.objects.get(staff=request.user)
    helper.update_pending_reservations(library=library)
    reservation = get_object_or_404(Reserve, code=code, library=library)

    return render(request, 'pages/dashboard_reservation_detail.html', {
        'page': 'dashboard',
        'library': library,
        'reservation': reservation
    })


@login_required
@csrf_exempt
@librarian_required
def dashboard_reservation_action(request, code):
    """ Action on reservation """
    if request.method == 'POST' and 'submit' in request.POST:
        library = Library.objects.get(staff=request.user)
        reservation = get_object_or_404(Reserve, code=code, library=library)
        if request.POST.get('submit') == 'pick-up':
            days = int(request.POST.get('days', '3'))
            pick_until = timezone.now() + timezone.timedelta(days=days)
            reservation.until_at = pick_until
            reservation.status = Reserve.Status.PICKED
            reservation.save()
        elif request.POST.get('submit') == 'cancel':
            reservation.status = Reserve.Status.CANCELED
            reservation.save()
        elif request.POST.get('submit') == 'return':
            reservation.status = Reserve.Status.BACKED
            reservation.save()

    return redirect('dashboard_reservation_detail', code=code)
