
from django.urls import path
from . import views


urlpatterns = [

    path("",views.home, name="home"),
    path("about/",views.about, name="about"),
    path("contact/",views.contact, name="contact"),
    path("view_table/",views.view_table, name="Table view"),
    path("createbook/",views.createbook, name='form'),
    path("update/<int:id>",views.update_book, name='upt'),
    path('delete/<int:id>',views.delete_book, name='delete'),
    path('regform',views.user_creation, name='user'),
    path('log',views.loginform,name='log'),
    path('logout/',views.logout_view, name='out'),
    path('view/',views.view_cart,name='v'),
    path('add/<int:bookid>',views.Addcart,name='add'),
]