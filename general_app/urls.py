from django.urls import path, include
from . import views
from users_app.views import login_user
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404

# from django.views.i18n import JavaScriptCatalog

urlpatterns = [
    path('', login_user, name='login'),
    path('users/', include('users_app.urls')),
    path('home/', views.home, name='home'),
    path('home/<int:pk>', views.delete_record, name='delete_record'),
    path('home/<str:hospital_id>/<path:path>/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('configuration/', views.configuration, name='configuration'),
    path('Manage_users/', views.manage_user, name='manage_user'),
    path('edit_user/', views.edit_user, name='edit_user'),
    path('Manage_users/<str:name>/', views.delete_user, name='delete_user'),
    # path('pdf/', views.create_pdf, name='pdf'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('test/', views.test, name='test'),
    path('upload_certificate/', views.upload_certificate, name='upload_certificate'),
    path('Change_Password/', views.change_password, name='change_password'),
    path('changepassword/done/', views.changepassword_done, name='changepassword_done'),
    # path('upload_certificate/<int:cert_id>/',views.upload_certificate_id,name='upload_certificate'),

]

# handler404 = "general_app.views.handle_not_found"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
