from django.urls import path
from taxi.views import (
    index,
    ManufacturerListView,
    ManufacturerDetailView,
    ManufacturerCreateView,
    ManufacturerUpdateView,
    ManufacturerDeleteView,
)


urlpatterns = [
    path("", index, name="index"),
    path("manufacturers/",
         ManufacturerListView.as_view(),
         name="manufacturer-list"),
    path(
        "manufacturers/<int:pk>/",
        ManufacturerDetailView.as_view(),
        name="manufacturer-detail",
    ),
    path(
        "manufacturers/create/",
        ManufacturerCreateView.as_view(),
        name="manufacturer-create",
    ),
    path(
        "manufacturers/<int:pk>/update/",
        ManufacturerUpdateView.as_view(),
        name="manufacturer-update",
    ),
    path(
        "manufacturers/<int:pk>/delete/",
        ManufacturerDeleteView.as_view(),
        name="manufacturer-delete",
    ),
]
