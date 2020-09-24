from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views
from . import forms
from django.contrib.auth import views as auth_views

urlpatterns = [
	path('', views.index, name='index'),
	path('login/', views.login_view, name='login'),
	path('signup/', views.signup_view, name='signup'),
	path('logout/', views.logout_view, name='logout'),
	path('locallibrary/', views.locallibrary, name='locallibrary'),
	path('books/', login_required(views.BookListView.as_view()), name='books'),
	path('book/<int:pk>/', login_required(views.BookDetailView.as_view()), name='book-detail'),
	path('authors/', login_required(views.AuthorListView.as_view()), name='authors'),
	path('author/<int:pk>/', login_required(views.AuthorDetailView.as_view()), name='author-detail'),
	path('user/<int:pk>', login_required(views.UserView.as_view()), name='user'),
	path('user/<int:pk>/edit_profile/', views.edit_profile_view, name='edit-profile'),
	path('contact/', views.contact, name="contact"),
	path('about/', views.about, name="about"),
	path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html', email_template_name='password_reset_email.html', subject_template_name='password_reset_subject.txt', form_class=forms.ResetPasswordForm), name='password_reset'),
	path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
	path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html', form_class=forms.PasswordSetForm), name='password_reset_confirm'),
	path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),

]

urlpatterns += [
	path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
]