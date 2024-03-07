import uuid
from django.db import models
from django.utils import timezone


STARTED = "STARTED"
IN_PROGRESS = "IN PROGRESS"
COMPLETED = "COMPLETED"
ABORTED = "ABORTED"

STATUS_CHOICES = [
    (STARTED, "Started"),
    (IN_PROGRESS, "In Progress"),
    (COMPLETED, "Completed"),
    (ABORTED, "Aborted"),
]


class MedicalCondition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)
    abbreviation = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Hospital(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Person(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)


class Contact(models.Model):
    REJECTED = "REJECTED"
    ACCEPTED = "ACCEPTED"
    IN_PROGRESS = "IN PROGRESS"

    TYPE_CHOICES = [
        (REJECTED, "Rejected"),
        (ACCEPTED, "Accepted"),
        (IN_PROGRESS, "In Progress"),
    ]

    person = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="contact_person"
    )
    medical_condition = models.ForeignKey(MedicalCondition, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=TYPE_CHOICES, default=IN_PROGRESS)


class Professional(models.Model):
    PHYSICIAN = "Physician"
    PHARMACIST = "Pharmacist"
    PN = "PN"

    TYPE_CHOICES = [
        (PHYSICIAN, "Physician"),
        (PHARMACIST, "Pharmacist"),
        (PN, "PN"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    person = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="professional_person"
    )
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    job_title = models.CharField(max_length=100)
    medical_license_number = models.CharField(max_length=100, unique=True)
    specialization = models.CharField(max_length=100, blank=True, null=True)


class Patient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    person = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="patient_person"
    )
    contact = models.OneToOneField(
        Contact, on_delete=models.CASCADE, null=True, blank=True
    )
    physician = models.ForeignKey(Professional, null=True, on_delete=models.SET_NULL)
    medical_condition = models.ForeignKey(MedicalCondition, on_delete=models.CASCADE)
    initial_consult_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.medical_condition} "


class PatientCall(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    patient_navigator = models.ForeignKey(Professional, on_delete=models.CASCADE)
    booking_date = models.DateTimeField()
    reminder_date = models.DateTimeField()
    no_show = models.BooleanField()
    notes = models.TextField()


class PatientLog(models.Model):
    LANDING_PAGE_SUBMISSION = "Landing Page Submission"
    CALL = "Call"
    EMAIL = "Email"

    TYPE_CHOICES = [
        (LANDING_PAGE_SUBMISSION, "Landing Page Submission"),
        (CALL, "Call"),
        (EMAIL, "Email"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateTimeField()
    type = models.CharField(max_length=100, choices=TYPE_CHOICES)

    def __str__(self):
        return f"Log {self.id} for patient {self.patient}"


class CT(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    trial_name = models.CharField(max_length=255)
    trial_description = models.TextField()

    def __str__(self):
        return self.trial_name


class CTJourney(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    ct = models.ForeignKey(CT, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    eligible = models.BooleanField(default=True)
    ineligible_reason = models.TextField(null=True, blank=True)
    outcome = models.TextField()

    def __str__(self):
        return f"{self.patient}'s journey in clinical trial {self.ct}"


class EAPDossier(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    number = models.CharField(max_length=255)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    product = models.CharField(
        max_length=255
    )  # Assuming this is a name or identifier for a drug or treatment
    enrollment_date = models.DateTimeField()

    def __str__(self):
        return f"Dossier {self.number} for patient {self.patient}"


class EAPJourney(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey("Patient", on_delete=models.CASCADE)
    eap = models.ForeignKey("EAPDossier", on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.patient}'s journey in EAP {self.eap_id}"
