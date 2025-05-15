from django.urls import path

from secops.controllers.usercases import BPER, Conjur


urlpatterns = [
    path("bper/<str:action>/", BPER.UseCaseBPERController.as_view(), name="BPER-use-case"),
    path("conjur/<str:action>/", Conjur.UseCaseConjurController.as_view(), name="conjur-use-case"),
]
