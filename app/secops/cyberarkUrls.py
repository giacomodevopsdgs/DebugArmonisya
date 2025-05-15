from django.urls import path

from secops.controllers.CyberArk import Safe, Safes, Account, Accounts, SafeMembers, SafeAccounts


urlpatterns = [
    path("safe/<str:id>/", Safe.SafeController.as_view(), name="cyberark-safe"),
    path("safes/", Safes.SafesController.as_view(), name="cyberark-safes"),

    path("account/<str:id>/", Account.AccountController.as_view(), name="cyberark-account"),
    path("accounts/", Accounts.AccountsController.as_view(), name="cyberark-accounts"),

    path("safe/<str:id>/accounts/", SafeAccounts.SafeAccountsController.as_view(), name="cyberark-safe-accounts"),
    path("safe/<str:id>/members/", SafeMembers.SafeMembersController.as_view(), name="cyberark-safe-members"),
]
