import uuid # This is required for assigning unique book instance
from django.urls import reverse	# Used to generate URLs by reversing the URL patterns
from django.db import models
from django.contrib.auth.models import (
 	BaseUserManager, AbstractBaseUser
)

# Create the user model instance View forms.py
class MyUserManager(BaseUserManager):
	def create_user(self, first_name, last_name, email, date_of_birth, password=None):
		"""
		Creates and saves a User with the given first_name, last_name, email, date_of_birth, and password
		"""
		if not email:
			raise ValueError('Users must have an email address')

		user = self.model(
			first_name = first_name,
			last_name = last_name,
			email = self.normalize_email(email),
			date_of_birth=date_of_birth,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, first_name, last_name, email, date_of_birth, password):
		"""
		Creates and saves a superuser with the given first_name, last_name, email, date_of_birth and password.
		"""
		user = self.create_user(
			first_name=first_name,
			last_name=last_name,
			email=email,
			password = password,
			date_of_birth=date_of_birth,
		)
		user.is_worker = True
		user.is_admin = True
		user.save(using=self._db)
		return user

class MyUser(AbstractBaseUser):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	email = models.EmailField(
		verbose_name='Email Address',
		max_length=255,
		unique=True,
	)
	date_of_birth=models.DateField()
	is_active=models.BooleanField(default=True)
	is_worker = models.BooleanField(default=False)
	is_admin = models.BooleanField(default=False)

	objects = MyUserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['first_name', 'last_name', 'date_of_birth']

	def get_full_name(self):
		# The user is identified by the first and last names
		return f'{self.last_name} {self.first_name}'

	def get_short_name(self):
		# The user is identifid by their last_name
		return self.email

	def __str__(self):
		return self.email

	def has_perm(self, perm, obj=None):
		"Does the user have specific permissions?"
		# Simplest possible answer: Yes, always
		return True

	def has_module_perms(self, app_label):
		"Does the user have permissions to view the app 'app_label'?"
		# Simplest possible answer: Yes, always
		return True

	def get_absolute_url(self):
		"""Return the url to access a particular user."""
		return reverse('user', args=[str(self.id)])

	@property
	def is_staff(self):
		"Is the user a member of the staff"
		# Simplest possible answer: All admins are staff
		return self.is_admin

class Genre(models.Model):
	"""Model representing a book genre."""
	name = models.CharField(max_length = 200, help_text = 'Enter a book genre (e.g. Science Fiction)')

	def __str__(self):
		"""String for representing the Model object."""
		return self.name

class Language(models.Model):
	"""Mode representing a language of the book."""
	name = models.CharField(max_length = 200, help_text = 'Enter the book language (e.g. English)')

	def __str__(self):
		"""String for representing the Model object."""
		return self.name

class Book(models.Model):
	"""Model representing a book (but not a specific copy of a book). The general view of every book."""
	title = models.CharField(max_length = 200)

	# Foreign Key used because book can only have one author, but authors can have multiple books
	# Author as a string rather than object because it hasn't been declared yet in the file
	author = models.ForeignKey('Author', on_delete=models.SET_NULL, null = True)

	language = models.ManyToManyField(Language, help_text='Select a language for this book.' )

	summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book.')
	isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

	# ManytoManyField used because genre can contain many books and Different books can cover many genres.
	# Genre class has already been defined so we can specify the object above.
	genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')

	class Meta:
		ordering = ['title']

	def display_language(self):
		"""Create a string for the Language. This is required to display the language in Admin."""
		return ', '.join(language.name for language in self.language.all() [:3])

	display_language.short_description = 'Language'

	def display_genre(self):
		"""Create a string for the Genre. This is required to display the genre in Admin because it's ManyToManyField."""
		return ', '.join(genre.name for genre in self.genre.all() [:3])

	display_genre.short_description = 'Genre'

	def __str__(self):
		"""String for representing the Book object"""
		return self.title

	def get_absolute_url(self):
		"""Returns the url to access a detail record for this book."""
		return reverse('book-detail', args=[str(self.id)])

class BookInstance(models.Model):
	"""Model representing a specific copy of the book (i.e. that can be borrowed from the library)."""
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text = 'Unique ID from this particular book across while library')
	book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
	imprint = models.CharField(max_length = 200)
	due_back = models.DateField(null=True, blank=True)

	LOAN_STATUS = [
		('m', 'Maintenance'),
		('o', 'On loan'),
		('a', 'Available'),
		('r', 'Reserved'),
	]

	status = models.CharField(
	    max_length = 1,
	    choices = LOAN_STATUS,
	    blank=True,
	    default='m',
	    help_text = 'Book availability',
	)

	class Meta:
		ordering = ['status', 'due_back', 'book']

	def __str__(self):
		"""String for representing the Model object."""
		return f'{self.id} ({self.book.title})'


class Author(models.Model):
	"""Model representing an author."""
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	date_of_birth = models.DateField(null = True, blank = True)

	class Meta:
		ordering = ['last_name', 'first_name']

	def get_absolute_url(self):
		"""Return the url to access a particular author instance."""
		return reverse('author-detail', args=[str(self.id)])

	def __str__(self):
		"""String for representing the Model object."""
		return f'{self.last_name} {self.first_name}'



