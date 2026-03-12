from django.contrib import admin

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
# Register your models here.
from .models import UserProfile, Author, Category, Tag, Book, Reserve, Review, Library, LibraryBook


class LibraryAdmin(admin.ModelAdmin):
    """ Custom Library Admin """

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "staff":
            try:
                group = Group.objects.get(name='librarian')
                unassigned_librarians = get_user_model().objects.filter(groups=group, library__isnull=True)
                if request.resolver_match.kwargs.get('object_id'):
                    library = self.get_object(request, request.resolver_match.kwargs['object_id'])
                    assigned_staff = library.staff.all()
                else:
                    assigned_staff = get_user_model().objects.none()
                kwargs["queryset"] = assigned_staff | unassigned_librarians
            except Group.DoesNotExist:
                kwargs["queryset"] = get_user_model().objects.none()
        return super().formfield_for_manytomany(db_field, request, **kwargs)


admin.site.register(UserProfile)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Book)
admin.site.register(Reserve)
admin.site.register(Review)
admin.site.register(Library, LibraryAdmin)
admin.site.register(LibraryBook)
