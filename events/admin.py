from django.contrib import admin
from events.models import Country, City, Event, Topics, Location, EventFilters


class CountryAdmin(admin.ModelAdmin):
    list_display = ("name",)


admin.site.register(Country, CountryAdmin)


class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "country")


admin.site.register(City, CityAdmin)


class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "pub_datetime", "start_datetime", "end_datetime",
                    "location", "slug", "is_cancelled", "is_published")
    list_filter = ["pub_datetime", "start_datetime"]
    search_fields = ["title", "description"]
    raw_id_fields = ("location", )


admin.site.register(Event, EventAdmin)


class TopicsAdmin(admin.ModelAdmin):
    list_display = ("name", "description")


admin.site.register(Topics, TopicsAdmin)


class LocationAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Location details",    {"fields": ["venue", "address1", "address2", "city", "country"]}),
        (None,                  {"fields": ["slug"]}),
    ]
    list_display = ("venue", "address1", "address2", "city", "country")
    search_fields = ["venue", "address1", "address2", "city", "country"]


admin.site.register(Location, LocationAdmin)


class EventFiltersAdmin(admin.ModelAdmin):
    list_display = ("user", "city", "topics", "start_range", "end_range")


admin.site.register(EventFilters, EventFiltersAdmin)



