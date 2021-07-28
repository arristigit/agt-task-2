from django.urls import path, include
from homeapp import views

urlpatterns = [
    path('', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('patient', views.patient, name='patient'),
    path('doctor', views.doctor, name='doctor'),
    path('dashboard', views.dashboard, name='dashboard'),
    
    path('allposts', views.allposts, name='allposts'),
    path('newpost', views.newpost, name='newpost'),
    path('myposts', views.myposts, name='myposts'),
    path('showpost/<int:id>', views.showpost, name='showpost'),
    path('updatepost/<int:id>', views.updatepost, name='updatepost'),

    path('listdoctors', views.listdoctors, name='listdoctors'),
    path('bookappointment/<int:id>', views.bookappointment, name='bookappointment'),
    path('appointmentdetails', views.appointmentdetails, name='appointmentdetails'),

]
