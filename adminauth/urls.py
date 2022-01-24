from django.urls import path
from .views import PatronApiView, PatronRetrieve, StudentApiView, StudentRetrieveView, PatronToStudentView, PatronToStudentRetrieveView
from .statistics.view import DashApiView
from .searchView import searchPatron, searchStudent

filterUrls = [
    path("filter/patron/", searchPatron),
    path("filter/student/", searchStudent)

    # path("filter/<str:condition>/<int:payment>/^(?P<date>\d{2}.\d{2}.\d{4})/$'/", searchPatron)
]

urlpatterns = [
    path("homiylar/", PatronApiView.as_view()),
    path("homiy/<int:id>/", PatronRetrieve.as_view()),
    path("statistics/", DashApiView.as_view()),
    path("student/<int:id>/", StudentRetrieveView.as_view()),
    path("student/", StudentApiView.as_view()),
    path("homiytostudent/", PatronToStudentView.as_view()),
    path("homiytostudent/<int:id>/", PatronToStudentRetrieveView.as_view()),



] + filterUrls