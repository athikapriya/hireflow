from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from accounts.models import User
from accounts.serializers import UserSerializer

from jobs.models import Job
from jobs.serializers import JobSerializer

from applications.models import Application
from applications.serializers import ApplicationSerializer


# =============== job lists =============== 
@api_view(['GET'])
def job_list(request):
    jobs = Job.objects.filter(is_active=True)
    serializer = JobSerializer(jobs, many=True)
    return Response(serializer.data)


# =============== job details =============== 
@api_view(['GET'])
def job_detail(request, pk):
    try:
        job = Job.objects.get(pk=pk)
    except Job.DoesNotExist:
        return Response({"error": "Job not found"}, status=404)
    serializer = JobSerializer(job)
    return Response(serializer.data)


# =============== apply job =============== 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def apply_job(request, job_id):
    try:
        job = Job.objects.get(pk=job_id)
    except Job.DoesNotExist:
        return Response({"error": "Job not found"}, status=404)

    if Application.objects.filter(job=job, candidate=request.user).exists():
        return Response({"error": "Already applied"}, status=400)

    application = Application.objects.create(
        job=job,
        candidate=request.user,
        resume=request.FILES.get('resume'),
        cover_letter=request.data.get('cover_letter', '')
    )
    serializer = ApplicationSerializer(application)
    return Response(serializer.data)


# =============== employer application =============== 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def employer_applications(request):
    user = request.user

    if user.role != 'employer':
        return Response({"error": "Only employers can view applications"}, status=403)

    applications = Application.objects.filter(job__employer=user)
    serializer = ApplicationSerializer(applications, many=True)

    return Response(serializer.data)


# =============== user application status =============== 
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_application_status(request, pk):
    user = request.user

    try:
        application = Application.objects.get(pk=pk)
    except Application.DoesNotExist:
        return Response({"error": "Application not found"}, status=404)

    if user.role != 'employer':
        return Response({"error": "Only employers can update status"}, status=403)
    if application.job.employer != user:
        return Response({"error": "Not your job"}, status=403)

    status_value = request.data.get("status")

    if status_value not in ["accepted", "rejected"]:
        return Response({"error": "Invalid status"}, status=400)

    application.status = status_value
    application.save()

    return Response({"message": f"Application {status_value}"})


# =============== user details =============== 
@api_view(['GET'])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    serializer = UserSerializer(user)
    return Response(serializer.data)