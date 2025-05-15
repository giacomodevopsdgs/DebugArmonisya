from django.urls import path, include

from .controllers import Root


urlpatterns = [
    path('api/', Root.RootController.as_view()),
    path('api/v1/', Root.RootController.as_view()),

    path('api/v1/secops/', include('secops.commonUrls')),
    path('api/v1/secops/cyberark/', include('secops.cyberarkUrls')),
    path('api/v1/secops/conjur/', include('secops.conjurUrls')),
    path('api/v1/secops/kubernetes/', include('secops.kubernetesUrls')),
    path('api/v1/secops/usecases/', include('secops.usecasesUrls')),
]
