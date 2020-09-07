from django.urls import path
from . import views
urlpatterns=[
    path("register",views.register,name="index"),
    path("login",views.login,name="index"),
    path("index1",views.index1,name="index1"),
    path("leader",views.leader,name="leader"),
    path("contact",views.contact,name="contact"),
    path("logout",views.logout,name="logout"),   
    path('c',views.c,name='c'),
    path('HelloWorldinpy',views.HelloWorldinpy,name="HelloWorldinpy"),
    path('HelloWorldinjava',views.HelloWorldinjava,name="HelloWorldinjava"),
     path('HelloWorldinc',views.HelloWorldinc,name="HelloWorldinc"),
    path('python',views.python,name='python'),
    path('java',views.java,name='java'),
    path("RUN",views.RUN,name="RUN"),
    path("RUNJAVA",views.RUNJAVA,name="RUNJAVA"),
    path("RUNC",views.RUNC,name="RUNC"),
    path("EVALUATE",views.EVALUATE,name="EVALUATE"),
    
]