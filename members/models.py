from django.db import models
from datetime import date, time


class Member(models.Model):
    firstname=models.CharField(max_length=255)
    lastname=models.CharField(max_length=255)
    phone=models.IntegerField(null=True)
    joined_date=models.DateField(null=True)
    specialization = models.CharField(max_length=255, blank=True, null=True)
    schedule = models.TextField(max_length=255, blank=True, null=True)
    remark = models.TextField(max_length=255, blank=True, null=True)
    physician_answer=models.TextField(blank=True, null=True)
    def __str__(self):
    #    return self.firstname
        return f"{self.firstname} {self.lastname}"
class Patient(models.Model):
    firstname=models.CharField(max_length=255)
    lastname=models.CharField(max_length=255)
    dob=models.DateField(null=True)
    add=models.CharField(max_length=500)
    phone=models.IntegerField(null=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], null=True, blank=True)  # New field
    def __str__(self):
        return f"{self.firstname} {self.lastname}"

class Appointment(models.Model):
    date_of_appointment = models.DateTimeField()
    time_of_appointment= models.TimeField()
    patient = models.ForeignKey('members.Patient', on_delete=models.CASCADE)
    physician = models.ForeignKey('members.Member', on_delete=models.CASCADE)
    remark = models.TextField(blank=True, null=True)
    appointment_answer=models.TextField(blank=True, null=True)
    encounter_status = models.BooleanField(default=False)  # This should be present
    def __str__(self):
        return f"Appointment {self.id} on {self.date_of_appointment} time {self.time_of_appointment} for Patient {self.patient_id} with Physician {self.physician_id}"
# my class for chatbot
class ChatResponse(models.Model):
    question = models.CharField(max_length=255, unique=True)
    answer = models.TextField()

    def __str__(self):
        return self.question
#end my class for chatbot

class Encounter(models.Model):
    id = models.AutoField(primary_key=True)
    enc_date = models.DateField(default=date.today)
    enc_patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    enc_physician = models.ForeignKey('Member', on_delete=models.CASCADE)
    enc_appointment = models.ForeignKey('Appointment', on_delete=models.CASCADE)
    
    enc_patient_query = models.TextField(max_length=550, null=True, blank=True)
    enc_physician_finding = models.TextField(max_length=1000, null=True, blank=True)
    enc_prescription = models.TextField(max_length=1000, null=True, blank=True)
    enc_lab_test = models.TextField(max_length=1000, null=True, blank=True)
    enc_diet = models.TextField(max_length=550, null=True, blank=True)
    enc_allergy = models.TextField(max_length=500, null=True, blank=True)
    enc_remark = models.TextField(max_length=550)

    enc_time_start = models.TimeField()
    enc_time_end = models.TimeField()
    enc_answer=models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Encounter {self.id} - {self.enc_patient} with {self.enc_physician} on {self.enc_date}"
    
