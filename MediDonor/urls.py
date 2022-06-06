from . import views
from django.urls import path

from MediDonor.views import DonateList, DonateView, DonateUpdateView, DonateDeleteView, PostView, PostListView, \
    PostUpdateView, PostDeleteView, NomineeView, NomineeListView, NomineeUpdateView, NomineeDeleteView


urlpatterns = [
    path('donate/', DonateView.as_view(), name='donate'),
    path('donate_list/', DonateList.as_view(), name='donate-list'),
    path('donate_update/<int:id>', DonateUpdateView.as_view(), name='donate-update'),
    path('donate_delete/<int:id>', DonateDeleteView.as_view(), name='donate-delete'),
    path('post/', PostView.as_view(), name='post'),
    path('post_list/', PostListView.as_view(), name='post-list'),
    path('post_update/<int:id>', PostUpdateView.as_view(), name='post-update'),
    path('post_delete/<int:id>', PostDeleteView.as_view(), name='post-delete'),
    path('nominee/', NomineeView.as_view(), name='nominee'),
    path('nominee_list/', NomineeListView.as_view(), name='nominee-list'),
    path('nominee_update/<int:id>', NomineeUpdateView.as_view(), name='nominee-update'),
    path('nominee_delete/<int:id>', NomineeDeleteView.as_view(), name='nominee-delete'),
    path('pdfcreate/',views.pdfcreate),
    path('pdfview/',views.pdfview)
]
