from django.urls import path

from secops.controllers.Kubernetes import Pods


urlpatterns = [
    path("pods/", Pods.PodsController.as_view(), name="kubernetes-pods"),
]
