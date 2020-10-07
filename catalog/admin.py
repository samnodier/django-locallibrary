from django.contrib import admin

from .models import Author, Genre, Language, Book, BookInstance

# To register the custom User Model created in models.py this is the added code.
from django import forms
# from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import MyUser

class UserCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the
    required fields, plus a repeated password.
    """
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Input password'})
    )
    password2 = forms.CharField(
        label='Password Confirmation',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'})
    )

    class Meta:
        model = MyUser
        fields = ('first_name', 'last_name', 'email', 'date_of_birth',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    """
    A form for updating users. Includes all the fields on the user, but replaces
    the password field with admin's password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = (
            'first_name',
            'last_name',
            'email',
            'date_of_birth',
            'password',
            'is_active',
            'is_admin',
        )

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the field
        # does not have access to the initial value.
        return self.initial['password']


class MyUserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = (
        'last_name',
        'first_name',
        'email',
        'date_of_birth',
        'is_admin',
    )
    list_filter = ('is_admin',)

    fieldsets = (
        (
            None, {
                'fields': (
                    'email',
                    'password',
                )
            }
        ),
        (
            'Personal Info', {
                'fields': (
                    'last_name',
                    'first_name',
                    'date_of_birth',
                )
            }
        ),
        (
            'Permissions', {
                'fields': ('is_admin',)
            }
        ),
    )

    # add_fieldsets is not standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating user.
    add_fieldsets = (
        (
            None, {
                'classes': ('wide',),
                'fields': (
                    'last_name',
                    'first_name',
                    'email',
                    'date_of_birth',
                    'password1',
                    'password2'
                )
            }
        ),
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(MyUser, MyUserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from the admin.
admin.site.unregister(Group)

# admin.site.register(Book)
# admin.site.register(Author)
admin.site.register(Language)
admin.site.register(Genre)
# admin.site.register(BookInstance)

# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth',)
    # This changes the alignment of the fields (horizontally or vertically)
    fields = ['first_name', 'last_name', ('date_of_birth',)]

# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)

# Register teh horizontal/vertical layout of the book information
class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0

# Register the Admin classes for Book using decorator
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_language', 'display_genre')
    inlines = [BooksInstanceInline]

# Register the Admin classes for BookInstance using decorator
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        })
    )

