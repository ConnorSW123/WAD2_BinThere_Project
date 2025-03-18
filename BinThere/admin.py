from django.contrib import admin
from BinThere.models import Location
from BinThere.models import BinType
from BinThere.models import Bin
from BinThere.models import Vote

# Add in this class to customise the Admin Interface
class CategoryAdmin(admin.ModelAdmin):
    # Update the registration to include this customised interface
    prepopulated_fields = {'slug':('name',)}

# Administrative Site Registration for Each Model
admin.site.register(Location)
admin.site.register(BinType)
admin.site.register(Bin)
admin.site.register(Vote)