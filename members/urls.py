from django.urls import path
from . import views
from .views import chatbot_response
from .views import select_physician, select_appointment, create_encounter, encounter_report,generate_encounter_pdf,appointment_report,export_appointments_csv, export_appointments_pdf,patient_report, download_csv, download_pdf, physician_report, download_csv_physician, download_pdf_physician
from .views import analyze_text
urlpatterns = [
    path('',views.main, name='main'),
    path('members/', views.members, name='members'),
    path('patients/', views.patients, name='patients'),
    path('members/details/<int:id>',views.details, name='details'),
    path('testing/',views.testing, name='testing'),
    path("chat/", chatbot_response, name="chatbot_response"),
    path('add/', views.add, name='add'),
    path('add/addrecord/', views.addrecord,name='addrecord'),
    path('add_patient/', views.add_patient, name='add_patient'),
    path('add_patient/addpatientrecord/', views.addpatientrecord, name='addpatientrecord'),
    path('setchatbot/', views.setchatbot, name='setchatbot'),
    path('setchatbot/setchatbotrecord/', views.setchatbotrecord, name='setchatbotrecrord'),
    path('viewchatbotsettings', views.viewchatbotsettings, name='viewchatbotsettings'),
    path('create_appointment/', views.create_appointment, name='create_appointment'),
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('delete-appointment/<int:appointment_id>/', views.delete_appointment, name='delete_appointment'),
    path('delete-physician/<int:member_id>/', views.delete_physician, name='delete_physician'),
    path('search/', views.search_products, name="search_products"),
    path('select-physician/', select_physician, name='select_physician'),
    path('select-appointment/<int:physician_id>/', select_appointment, name='select_appointment'),
    path('create-encounter/<int:appointment_id>/', create_encounter, name='create_encounter'),
    path('encounter_report/', encounter_report, name='encounter_report'),
    path('encounter_report/pdf/', generate_encounter_pdf, name='generate_encounter_pdf'),
    path('analyze-text/', analyze_text, name='analyze_text'),
    path('appointment-report/', appointment_report, name='appointment_report'),
    path('export/csv/', export_appointments_csv, name='export_appointments_csv'),
    path('export/pdf/', export_appointments_pdf, name='export_appointments_pdf'),
    path('patient-report/', patient_report, name='patient_report'),
    path('patient-report/download-csv/', download_csv, name='download_csv'),
    path('patient-report/download-pdf/', download_pdf, name='download_pdf'),
     path('physician-report/', physician_report, name='physician_report'),
    path('download-csv_physician/', download_csv_physician, name='download_csv_physician'),
    path('download-pdf_physician/', download_pdf_physician, name='download_pdf_physician'),
    
]