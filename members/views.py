from django.utils.timezone import now
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.models import User
from datetime import datetime, timedelta, time,date
# my addition
import csv
from django.http import JsonResponse
from .models import ChatResponse
import pyttsx3
# End my addition
from .models import Member
from .models import Patient
from .models import Appointment
from django.utils.timezone import now
from django.core.paginator import Paginator
from datetime import datetime 
import spacy
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Encounter
from .forms import EncounterForm
from .forms import EncounterFilterForm
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape,letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph, Spacer, SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from datetime import datetime
from .nlp_service import process_text
import os
import io
from reportlab.lib.utils import simpleSplit










def members(request): # this will list all the physicians
    mymembers=Member.objects.all().values()
#   template=loader.get_template('all_members.html')
#   contex={ 'mymembers':mymembers,}
#   return HttpResponse(template.render(contex,request))
    paginator = Paginator(mymembers, 5)  # Show 5 appointments per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'mymembers': page_obj,
    }
    return render(request, 'all_members.html', context)

def patients(request):       # this will list all patient
    mypatients=Patient.objects.all().order_by('firstname', 'lastname').values()
    #template=loader.get_template('all_patients.html')
    #contex={'mypatients':mypatients}
    #return HttpResponse(template.render(contex,request))
    paginator=Paginator(mypatients,5) #show 5 patients per page
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    context={
                'mypatients':page_obj, 
            }
    return render(request,'all_patients.html', context)


def details(request, id):
    mymember=Member.objects.get(id=id)
    template=loader.get_template('details.html')
    context={'mymember':mymember,}
    return HttpResponse(template.render(context, request))
def main(request):
    template=loader.get_template('main.html')
    return HttpResponse(template.render())

def testing(request):
    template=loader.get_template('template.html')
    context={'fruits':['Apple','Banana','Cherry'],}
    return HttpResponse(template.render(context,request))

def add(request): # to add physician's  record to form
    template=loader.get_template('add_physician.html')
    return HttpResponse(template.render({}, request))

def addrecord(request):  # submitting physician's record to database
    x = request.POST['first']
    y = request.POST['last']
    jdate1=request.POST['jdate']
    ph=request.POST['phone']
    date_object = datetime.strptime(jdate1, "%Y-%m-%d")
    expert=request.POST['expt']
    phy_schedule=request.POST['schedule']
    phy_remark=request.POST['remark']
    p_ans=f"{x} {y} is {expert} and has joined clinic from {jdate1}. His contact number is {ph}. He visits clinic {phy_schedule}. {phy_remark}."
    member = Member(firstname=x, lastname=y, phone=ph, joined_date=date_object,specialization=expert, schedule=phy_schedule, remark=phy_remark, physician_answer=p_ans)
    
    member.save()
    return HttpResponseRedirect(reverse('members'))

def add_patient(request):
    template=loader.get_template('addpatient.html')
    return HttpResponse(template.render({},request))
                                         
def addpatientrecord (request):
    fn1=request.POST['firstname1']
    ln1=request.POST['lastname1']
    dobirth1=request.POST["dob1"]
    dobirth1 = datetime.strptime(dobirth1, "%Y-%m-%d").date()
    gen1=request.POST['gender1']
    addr1=request.POST["add1"]
    phoneno1=request.POST["phone1"]
    patient1=Patient(firstname=fn1, lastname=ln1, dob=dobirth1, add=addr1, phone=phoneno1,gender=gen1)
    patient1.save()
    #return HttpResponseRedirect(reverse('members'))
    return HttpResponseRedirect(reverse('patients'))
    
    

def setchatbot(request):
    template=loader.get_template('setchatbot.html')
    return HttpResponse(template.render({}, request))
    
def setchatbotrecord(request):
    qst=request.POST['question']
    ans=request.POST['answer']
    qst_ans=ChatResponse(question=qst, answer=ans)
    qst_ans.save()
    return HttpResponseRedirect(reverse('members'))
def viewchatbotsettings(request):
    record1=ChatResponse.objects.all().values()
    template=loader.get_template('viewchatbotsettings.html')
    contex={ 'record1':record1,}
    return HttpResponse(template.render(contex,request))
    
#define my function for chatbot
def chatbot_response1(request):
    if request.method == "GET":
        question = request.GET.get("question", "").strip()
        print(question)
        if question:
            response = ChatResponse.objects.filter(question__icontains=question).first()
            
            if response:
                answer = response.answer
                
            else:
                answer = "Sorry, I don't have an answer to that question."
            
            # Convert text to speech
            #engine = pyttsx3.init()
            #engine.say(answer)
            #engine.runAndWait()
            
            return JsonResponse({"answer": answer})
    return JsonResponse({"answer": "Invalid request"})
#End defination of my function for chatbot
def chatbot_response(request):
    if request.method == "GET":
        question = request.GET.get("question", "").strip()
        print(question)
        if question:
            response = process_text(question)
            
            if response and "response" in response:
                answer = response["response"] or "Sorry, I don't have an answer to your question"
                
            else:
                answer = "Sorry, I don't have an answer to that question."
            
            # Convert text to speech
            #engine = pyttsx3.init()
            #engine.say(answer)
            #engine.runAndWait()
            
            return JsonResponse({"answer": answer})
    
    return JsonResponse({"answer": "Invalid request"})
#End defination of my function for chatbot










def format_date(date_str):
    """Convert a date from 'YYYY-MM-DD' format to 'DDth Month, YYYY' format."""
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    day = int(date_obj.strftime("%d"))
    
    # Determine ordinal suffix
    suffix = "th" if 11 <= day <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
    
    # Format date with suffix
    formatted_date = f"{day}{suffix} {date_obj.strftime('%B')}, {date_obj.strftime('%Y')}"
    return formatted_date
def convert_date_to_string(date_obj):
    """Convert a date object to 'DDth Month, YYYY' format."""
    day = date_obj.day

    # Determine ordinal suffix
    suffix = "th" if 11 <= day <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")

    # Format the date
    formatted_date = f"{day}{suffix} {date_obj.strftime('%B')}, {date_obj.year}"
    
    return formatted_date

def convert_to_am_pm(time_str):
    """Convert 'HH:MM' 24-hour format to 'HH:MM a.m./p.m.' 12-hour format."""
    # Split hours and minutes
    hours, minutes = map(int, time_str.split(":"))
    
    # Determine a.m. or p.m.
    period = "a.m." if hours < 12 else "p.m."
    
    # Convert hours to 12-hour format
    hours = hours % 12 or 12  # Convert 0 to 12 for midnight
    
    return f"{hours}:{minutes:02d} {period}"
def time_spent(start, end):
    """Calculate the time difference between start and end time in HH:MM format."""
    today = datetime.today().date()
    start_dt = datetime.combine(today, start)
    end_dt = datetime.combine(today, end)

    # Handle case where end time is past midnight
    if end_dt < start_dt:
        end_dt += timedelta(days=1)

    # Calculate time difference
    time_diff = end_dt - start_dt
    hours, minutes = divmod(time_diff.seconds // 60, 60)

    return f"{hours} hours {minutes} minutes"
def create_appointment(request):
    if request.method == 'POST':
        doa = request.POST.get('date_of_appointment')
        toa = request.POST.get('time_of_appointment')
        patient_id = request.POST.get('patient_id')
        physician_id = request.POST.get('physician_id')
        remark = request.POST.get('remark')
        # Convert date string to date object (not datetime)
                
        
        fdoa=format_date(doa)
        ftoa=convert_to_am_pm(toa)
        # Validate and save the appointment
        try:
            patient = Patient.objects.get(id=patient_id)
            physician = Member.objects.get(id=physician_id)
            appointment = Appointment(
                date_of_appointment=doa,
                time_of_appointment=toa,
                patient=patient,
                physician=physician,
                remark=remark,
                appointment_answer=f"The appointment for patient {patient} with {physician} is on {fdoa} at {ftoa}."
            )
            appointment.save()
            # Use messages framework
            #messages.success(request, "Appointment created successfully!")
            # Redirect to appointment list page
            return redirect('/appointments')
            
           # return HttpResponse("Appointment created successfully!")
        except Patient.DoesNotExist:
            return HttpResponse("Patient not found.")
        except Member.DoesNotExist:
            return HttpResponse("Physician not found.")
        except Exception as e:
            return HttpResponse(f"Error: {e}")
    else:
        patients = Patient.objects.all().values()
        # print(patients)
        physicians = Member.objects.all().values()
        # print(physicians)
        return render(request, 'create_appointment.html', {'patients': patients, 'physicians': physicians})

def split_full_name(full_name):
    name_parts = full_name.strip().split()
    
    if len(name_parts) > 1:
        first_name = " ".join(name_parts[:-1])  # All except last word
        last_name = name_parts[-1]  # Last word as last name
    else:
        first_name = full_name
        last_name = ""

    return first_name, last_name

def appointment_list(request):
    appointments = Appointment.objects.select_related('patient', 'physician').order_by('date_of_appointment')
    #newly added code
    print(appointments.count())
    # Get filter values from request
    physician_name = request.GET.get('physician', '').strip()
    patient_name = request.GET.get('patient', '').strip()
    appointment_date = request.GET.get('date', '').strip()
    print(physician_name)
    print(patient_name)
    print(appointment_date)
    # Apply filters if provided
    
    if physician_name:
        first_name, last_name = split_full_name(physician_name)
        appointments = appointments.filter(
            Q(physician__firstname__icontains=first_name, physician__lastname__icontains=last_name) |
            Q(physician__firstname__icontains=last_name, physician__lastname__icontains=first_name)
        )   
    if patient_name:
        name_parts = patient_name.split()
        if len(name_parts) == 2:
            first_name, last_name = name_parts
            appointments = appointments.filter(
                Q(patient__firstname__icontains=first_name, patient__lastname__icontains=last_name) |
                Q(patient__firstname__icontains=last_name, patient__lastname__icontains=first_name)
            )

    if appointment_date:
        appointments = appointments.filter(date_of_appointment=appointment_date)

     # Debugging: Check count after filtering
    print("Filtered Count:", appointments.count())
    
    physicians = Member.objects.all()
    patients = Patient.objects.all()
    
    # Pagination
    paginator = Paginator(appointments, 5)  # Show 10 appointments per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'appointments': page_obj,
        'physician_name': physician_name,
        'patient_name': patient_name,
        'appointment_date': appointment_date,
        'physicians': physicians,  # Pass physicians list to template
        'patients': patients,  # Pass patients list to templat
        #'encounter':encounter, # pass encounter status 0 or null not, 1 yes
    }
    return render(request, 'appointment_list.html', context)
    
    
    #End newly added code
    
    paginator = Paginator(appointments, 5)  # Show 5 appointments per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # following is old code 
    #context = {
    #    'appointments': page_obj,
    #}
    #return render(request, 'appointment_list.html', context)

def delete_appointment(request, appointment_id):
    # Fetch the appointment object
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Delete the appointment
    appointment.delete()
    
    # After deletion, redirect back to the list page 
    return redirect('appointment_list')  # URL name for the appointments list page  
    
    
def delete_physician(request, member_id):
    physician=get_object_or_404(Member, id=member_id)
    physician.delete()
    return redirect('members')
    
# Load the SpaCy model
nlp = spacy.load("en_core_web_sm")

def analyze_text(request):
    text = request.GET.get("text", "")
    if text:
        result = process_text(text)
        return JsonResponse(result)
    return JsonResponse({"error": "No text provided"})

def search_products(request):
    results = []
    c_answer=[]
    canswer="Here is your answer:. "
    query = None
    engine = pyttsx3.init()
    if request.method == "POST":
        # Get the search text from the user
        query = request.POST.get("query")
        search_method=request.POST.get("search_method")
        print(search_method)
        print(query)
        if query:
            # Process the input text using NLP
            doc = nlp(query)
            print(doc)
            # Extract relevant keywords (e.g., nouns or named entities)
            keywords = [token.text.lower() for token in doc if token.pos_ in ["NOUN", "PROPN"]]
            #names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
            price = None
            print(keywords)
            #print(names)

            # Check if the text contains a price entity
            #for ent in doc.ents:
             #   if ent.label_ == "MONEY":
              #      try:
               #         price = float(ent.text.replace("$", ""))
                #    except ValueError:
                 #       pass
            
            # Query the database using keywords and optional price
            products = ChatResponse.objects.all()
            
            query=Q() #new
            if keywords:
                # Match keywords in name or description (case insensitive)
               
                for keyword in keywords:
                    if search_method=="Strick":
                        query &=Q(answer__icontains=keyword) # new
                    else:
                        query |=Q(answer__icontains=keyword) # new for loose searching
                        
                    #products = products.filter(name__icontains=keyword) | products.filter(description__icontains=keyword)
                    #products = products.filter(answer__icontains=keyword)  
                products=products.filter(query) # new
            #if price:
                # Filter products by price if a price is mentioned
             #   products = products.filter(price__lte=price)
            
            results = products.distinct()
            for ans in results:
                c_answer.append(ans.answer) 
            print(c_answer)
            # Initialize the text-to-speech engine
            

            # Speak each answer one by one
            for answer in c_answer:
                engine.say(answer)

            # Run the speech engine
                engine.runAndWait()
            #print(query)
            

    return render(request, "search.html", {"results": results, "query": query})
# Render the template for both GET and POST
def select_physician(request):
    """Displays a dropdown of all physicians"""
    physicians = Member.objects.all()
    print(physicians)
    return render(request, 'select_physician.html', {'physicians': physicians})

def select_appointment(request, physician_id):
    """Lists all appointments for the selected physician"""
    physician = get_object_or_404(Member, id=physician_id)
    print(physician.firstname)
    appointments = Appointment.objects.filter(physician=physician)
    
    return render(request, 'select_appointment.html', {'physician': physician, 'appointments': appointments})

def create_encounter(request, appointment_id):
    """Handles encounter form submission"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    patient = appointment.patient
    print(patient.firstname)
    physician = appointment.physician
    print(physician.firstname)

    if request.method == "POST":
        form = EncounterForm(request.POST)
        if form.is_valid():
            encounter = form.save(commit=False)
            encounter.enc_patient = patient
            encounter.enc_physician = physician
            encounter.enc_appointment = appointment
            encounter.enc_date = datetime.today().date()
            appointment.encounter_status=1
            edate_str=convert_date_to_string(encounter.enc_date)
            #edate_str=format_date(encounter.enc_date)
            e_time_spent=time_spent(encounter.enc_time_end, encounter.enc_time_start)
            encounter.enc_answer=f"Patient {patient.firstname} {patient.lastname} has completed encounter with physician {physician.firstname} {physician.lastname} on {edate_str}. The encounter started at {encounter.enc_time_start}. Total encounter time was {e_time_spent}. The patient's complaint was {encounter.enc_patient_query},whereas the physician diagnose {encounter.enc_physician_finding}. The physician prescribe {encounter.enc_prescription} with diet control {encounter.enc_diet} and Lab Test  {encounter.enc_lab_test}. The patient's allergy report is {encounter.enc_allergy}. The physician completed his encounter with {encounter.enc_remark}."
            encounter.save()
            appointment.encounter_status=1
            appointment.appointment_answer=appointment.appointment_answer + "Whereas, the patient has already encountered with physician. Please, Check encounter details with encounter list."
            
            appointment.save()
            return JsonResponse({'success': True, 'message': "Encounter saved successfully!"})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

    else:
        form = EncounterForm()
    
    return render(request, 'create_encounter.html', {'form': form, 'appointment': appointment, 'physician':physician, 'patient':patient}) 

def encounter_report(request):
    form = EncounterFilterForm(request.GET or None)
    encounters = Encounter.objects.all()
    
    if form.is_valid():
        if form.cleaned_data['date']:
            encounters = encounters.filter(enc_date=form.cleaned_data['date'])
        if form.cleaned_data['physician']:
            encounters = encounters.filter(enc_physician=form.cleaned_data['physician'])
        if form.cleaned_data['patient']:
            encounters = encounters.filter(enc_patient=form.cleaned_data['patient'])
    
    return render(request, 'encounter_report.html', {'form': form, 'encounters': encounters})
def generate_encounter_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="encounter_report.pdf"'

    # Set up Landscape PDF
    doc = SimpleDocTemplate(response, pagesize=landscape(letter))
    elements = []
    styles = getSampleStyleSheet()

    # Clinic Info
    clinic_name = "ABC Healthcare Solution"
    clinic_address = "123 Health Street, Nagpur City, 440008, M.S. (India)"
    clinic_contact = "Phone: +91-234-567-890 | Email: contact@abcclinic.com"

    # Add Clinic Name
    clinic_title = Paragraph(f"<b>{clinic_name}</b>", styles["Title"])
    elements.append(clinic_title)

    # Add Address & Contact
    clinic_info = Paragraph(f"{clinic_address}<br/>{clinic_contact}", styles["Normal"])
    elements.append(clinic_info)
    
    elements.append(Spacer(1, 0.3 * inch))  # Spacing

    # Report Title & Date
    report_title = Paragraph("<b>Encounter Report</b>", styles["Heading2"])
    report_date = Paragraph(f"<b>Report Date:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles["Normal"])
    elements.append(report_title)
    elements.append(report_date)
    
    elements.append(Spacer(1, 0.2 * inch))  # Spacing

    # Fetch Encounters
    encounters = Encounter.objects.all()

    # Table Headers
    data = [["ID", "Date", "Patient", "Physician", "Findings", "Prescription", "Lab Test", "Diet"]]

    # Populate Table Data
    for encounter in encounters:
        data.append([
            str(encounter.id),
            str(encounter.enc_date),
            str(encounter.enc_patient),
            str(encounter.enc_physician),
            Paragraph(encounter.enc_physician_finding or "N/A", styles["BodyText"]),
            Paragraph(encounter.enc_prescription or "N/A", styles["BodyText"]),
            Paragraph(encounter.enc_lab_test or "N/A", styles["BodyText"]),
            Paragraph(encounter.enc_diet or "N/A", styles["BodyText"])
        ])

    # Create Table with Better Formatting
    table = Table(data, colWidths=[30, 70, 100, 100, 130, 130, 100, 100])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("ROWBACKGROUNDS", (1, -1), (-1, -1), [colors.lightgrey, colors.white])
    ]))

    elements.append(table)
    elements.append(Spacer(1, 0.3 * inch))  # Spacing

    # Footer with Page Number & Confidential Note
    def footer(canvas, doc):
        canvas.setFont("Helvetica", 9)
        canvas.drawString(inch, 0.75 * inch, "Confidential - ABC Healthcare Solution")
        canvas.drawString(10 * inch, 0.75 * inch, f"Page {doc.page}")

    # Build PDF with Footer
    doc.build(elements, onFirstPage=footer, onLaterPages=footer)

    return response


def appointment_report(request):
    appointments = Appointment.objects.select_related('patient', 'physician').all()

    # Get filter values
    date_filter = request.GET.get('date', '')
    physician_filter = request.GET.get('physician', '')
    patient_filter = request.GET.get('patient', '')

    # Apply filters
    if date_filter:
        appointments = appointments.filter(date_of_appointment__date=date_filter)
    if physician_filter:
        appointments = appointments.filter(physician_id=physician_filter)
    if patient_filter:
        appointments = appointments.filter(patient_id=patient_filter)

    # Pagination
    paginator = Paginator(appointments, 10)  # Show 10 appointments per page
    page_number = request.GET.get('page')  # Get current page number from query parameter
    page_obj = paginator.get_page(page_number)  # Get the corresponding page of appointments

    physicians = Member.objects.all()
    patients = Patient.objects.all()

    return render(request, 'appointments_report.html', {
        'appointments': page_obj,  # Pass the paginated page object
        'physicians': physicians,
        'patients': patients,
        'date_filter': date_filter,
        'physician_filter': physician_filter,
        'patient_filter': patient_filter
    })


def export_appointments_csv(request):
    """ Export filtered appointments as CSV """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="appointments.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Appointment ID', 'Patient Name', 'Physician Name', 'Date', 'Time', 'Remark', 'Status'])

    appointments = Appointment.objects.select_related('patient', 'physician').all()

    # Apply filters
    date_filter = request.GET.get('date', '')
    physician_filter = request.GET.get('physician', '')
    patient_filter = request.GET.get('patient', '')

    if date_filter:
        appointments = appointments.filter(date_of_appointment__date=date_filter)
    if physician_filter:
        appointments = appointments.filter(physician_id=physician_filter)
    if patient_filter:
        appointments = appointments.filter(patient_id=patient_filter)

    for appointment in appointments:
        writer.writerow([
            appointment.id,
            f"{appointment.patient.firstname} {appointment.patient.lastname}",
            f"{appointment.physician.firstname} {appointment.physician.lastname}",
            appointment.date_of_appointment.date(),
            appointment.time_of_appointment,
            appointment.remark if appointment.remark else "No remarks",
            "Completed" if appointment.encounter_status else "Pending"
        ])

    return response


def export_appointments_pdf(request):
    """ Export filtered appointments as a well-styled PDF """
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="appointments.pdf"'

    buffer = []
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Title
    title = Paragraph("<b>Patient Appointment Report</b>", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))

    # Report Date
    report_date = now().strftime("%Y-%m-%d %H:%M:%S")
    date_paragraph = Paragraph(f"Report Date: <b>{report_date}</b>", styles['Normal'])
    elements.append(date_paragraph)
    elements.append(Spacer(1, 12))

    # Fetch filtered appointments
    appointments = Appointment.objects.select_related('patient', 'physician').all()
    date_filter = request.GET.get('date', '')
    physician_filter = request.GET.get('physician', '')
    patient_filter = request.GET.get('patient', '')

    if date_filter:
        appointments = appointments.filter(date_of_appointment__date=date_filter)
    if physician_filter:
        appointments = appointments.filter(physician_id=physician_filter)
    if patient_filter:
        appointments = appointments.filter(patient_id=patient_filter)

    # Table Data
    data = [["ID", "Patient Name", "Physician Name", "Date", "Time", "Status"]]
    
    for appointment in appointments:
        data.append([
            appointment.id,
            f"{appointment.patient.firstname} {appointment.patient.lastname}",
            f"{appointment.physician.firstname} {appointment.physician.lastname}",
            appointment.date_of_appointment.date(),
            appointment.time_of_appointment.strftime("%H:%M"),
            "Completed" if appointment.encounter_status else "Pending"
        ])

    # Table Styling
    table = Table(data, colWidths=[50, 130, 130, 80, 70, 80])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(table)
    elements.append(Spacer(1, 50))

    # Signature Line
    signature_paragraph = Paragraph("<br/><br/>Authorized Signature: ____________________", styles['Normal'])
    elements.append(signature_paragraph)

    # Build PDF
    doc.build(elements)
    return response
def calculate_birth_year(age):
    """Calculate the birth year for filtering based on age."""
    today = date.today()
    return today.year - age

def patient_report(request):
    patients = Patient.objects.all().order_by('id')  # ✅ Start with all patients
    print(patients)
    # Get filter values from request
    gender_filter = request.GET.get('gender', 'All')
    age_min = request.GET.get('age_min', '')
    age_max = request.GET.get('age_max', '')

    # Apply gender filter if selected
    if gender_filter and gender_filter != "All":
        patients = patients.filter(gender=gender_filter)

    # Debugging: Print gender filter
    print("Gender Filter:", gender_filter, "Patients Found:", patients.count())

    # Apply age range filter only if both values are provided
    if age_min.isdigit() and age_max.isdigit():
        age_min = int(age_min)
        age_max = int(age_max)

        if age_min > 0 and age_max > 0 and age_min <= age_max:
            min_birth_year = calculate_birth_year(age_max)  # Older patients
            max_birth_year = calculate_birth_year(age_min)  # Younger patients
            patients = patients.filter(dob__year__range=(min_birth_year, max_birth_year))

    # Debugging: Print age filter
    print("Age Filter:", age_min, "-", age_max, "Patients Found:", patients.count())

    # Pagination (10 patients per page)
    paginator = Paginator(patients, 10)
    page_number = request.GET.get('page')
    patients_page = paginator.get_page(page_number)

    today=date.today()
    return render(request, 'patient_report.html', {
        'page_obj': patients_page,
        'gender_filter': gender_filter,
        'age_min': age_min,
        'age_max': age_max,
        'today':today,
    })
def download_csv(request):
    patients = Patient.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="patient_list_{datetime.today().date()}.csv"'
    writer = csv.writer(response)
    writer.writerow(['Id','First Name', 'Last Name', 'DOB', 'Address', 'Phone', 'Gender'])
    for patient in patients:
        writer.writerow([patient.firstname, patient.lastname, patient.dob, patient.add, patient.phone, patient.gender])
    return response

def download_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="patient_list_{datetime.today().date()}.pdf"'

    # Set up PDF with landscape orientation
    pdf = canvas.Canvas(response, pagesize=landscape(letter))
    width, height = landscape(letter)

    # Title
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(250, height - 50, "Patient List")  # Title
    pdf.setFont("Helvetica", 12)
    pdf.drawString(width - 150, height - 50, str(datetime.today().date()))  # Date on the right

    # **Increase spacing between title & table**
    y_start = height - 150  # More space below title

    # Get sample styles for wrapped text
    styles = getSampleStyleSheet()
    styleN = styles["Normal"]

    # Table Data (Wrap Address)
    data = [['ID', 'First Name', 'Last Name', 'DOB', 'Address', 'Phone', 'Gender']]  # Header row
    for patient in Patient.objects.all():
        wrapped_address = Paragraph(patient.add, styleN)  # Wrap long addresses
        data.append([
            patient.id, patient.firstname, patient.lastname, 
            patient.dob, wrapped_address, patient.phone, patient.gender
        ])

    # Create Table with Proper Column Sizing
    col_widths = [50, 100, 100, 80, 200, 100, 80]  # Wider column for Address
    table = Table(data, colWidths=col_widths)

    # Apply Styling: Light Yellow Background
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightyellow),  # Light Yellow Header
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    # **Ensure enough space between title and table**
    table.wrapOn(pdf, width, height)
    table.drawOn(pdf, 50, y_start - len(data) * 15)  # Move the table further down

    # Signature Line (at the bottom)
    pdf.setFont("Helvetica", 12)
    pdf.drawString(250, 80, "Authorized Signature")

    pdf.showPage()
    pdf.save()
    return response
def physician_report(request):
    specialization_filter = request.GET.get('specialization', '')
    physicians = Member.objects.all()
    
    if specialization_filter:
        physicians = physicians.filter(specialization=specialization_filter)
    
    specializations = Member.objects.values_list('specialization', flat=True).distinct()
    
    return render(request, 'physician_report.html', {
        'physicians': physicians,
        'specializations': specializations,
        'selected_specialization': specialization_filter,
    })
def download_csv_physician(request):
    specialization_filter = request.GET.get('specialization', '')
    physicians = Member.objects.all()
    
    if specialization_filter:
        physicians = physicians.filter(specialization=specialization_filter)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="physician_report.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['ID', 'First Name', 'Last Name', 'Joining Date', 'Specialization', 'Schedule', 'Remark'])
    
    for physician in physicians:
        writer.writerow([physician.id, physician.firstname, physician.lastname, physician.joined_date, physician.specialization, physician.schedule, physician.remark])
    
    return response
def download_pdf_physician(request):
    specialization_filter = request.GET.get('specialization', '')
    physicians = Member.objects.all()
    
    if specialization_filter:
        physicians = physicians.filter(specialization=specialization_filter)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="physician_report.pdf"'
    
    p = canvas.Canvas(response, pagesize=landscape(letter))
    width, height = landscape(letter)
    margin = 36  # 0.5 inch margin
    
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width / 2, height - margin, "Physician Report")
    
    p.setFont("Helvetica", 10)
    y = height - (margin + 30)
    col_widths = [(width - 2 * margin) / 7] * 7  # 7 columns equally spaced
    col_x_positions = [margin + sum(col_widths[:i]) for i in range(7)]
    headers = ["ID", "First Name", "Last Name", "Joining Date", "Specialization", "Schedule", "Remark"]
    
    # Draw table headers
    p.setStrokeColor(colors.black)
    p.setLineWidth(1)
    for i, header in enumerate(headers):
        p.drawString(col_x_positions[i], y, header)
    
    y -= 15
    
    # Draw table rows with borders
    for physician in physicians:
        row_data = [
            str(physician.id),
            physician.firstname,
            physician.lastname,
            str(physician.joined_date),
            physician.specialization or "",
            physician.schedule or "",
            physician.remark or ""
        ]
        
        row_top = y + 10
        row_bottom = y - 5
        p.line(margin, row_bottom, width - margin, row_bottom)  # Draw row bottom border
        
        for i, cell in enumerate(row_data):
            wrapped_text = simpleSplit(cell, "Helvetica", 10, col_widths[i])
            if wrapped_text:
                p.drawString(col_x_positions[i], y, wrapped_text[0])
            else:
                p.drawString(col_x_positions[i], y, "")  # Print empty string if no text
        
        y -= 15
        if y < margin:
            p.showPage()
            p.setFont("Helvetica", 10)
            y = height - (margin + 30)
    
    p.showPage()
    p.save()
    return response