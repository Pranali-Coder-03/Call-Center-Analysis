from django.urls import path
from . import views


urlpatterns = [

    path(
        "",
        views.dashboard,
        name="dashboard"
    ),

    path(
        "analyze/",
        views.analyze_call,
        name="analyze_call"
    ),

    path(
        "analyze/<int:call_id>/",
        views.analyze_call_result,
        name="analyze_call_result"
    ),

    path(
        "recordings/",
        views.view_recordings,
        name="recordings"
    ),

    path(
        "recordings/<int:call_id>/delete/",
        views.delete_recording,
        name="delete_recording"
    ),

    path(
        "report/<int:call_id>/",
        views.download_report,
        name="download_report"
    ),
]