import PyPDF2
import io

from django.db.models import F


from django.http import FileResponse
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from MediDonor.models import Organ, Post, Nominee
from MediDonor.serializers import DonateListSerializer, DonateSerializer, PostSerializer, NomineeSerializer

from reportlab.pdfgen import canvas


def pdfcreate(request):
    d = Organ.objects.filter(user_id__id=request.user.pk).all()
    print(str(d.__str__))
    buffer = io.BytesIO()
    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, (str(d.__str__)))
    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='donation.pdf')


@csrf_exempt
def pdfview(request):
    if request.method == 'POST':
        # creating a pdf file object
        pdfFileObj = open('/Users/prarthanamaheta/Desktop/sample.pdf', 'rb')

        # creating a pdf reader object
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

        # printing number of pages in pdf file

        print(pdfReader.numPages)

        # creating a page object
        pageObj = pdfReader.getPage(0)

        # extracting text from page
        print(pageObj.extractText())

        # closing the pdf file object
        pdfFileObj.close()
        return "message updated successfully"


class DonateView(generics.CreateAPIView):
    """
    Register donation if Mediuser is authenticated
    """

    permission_classes = [IsAuthenticated]
    serializer_class = DonateSerializer
    queryset = Organ.objects.all

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(
            {
                'request': self.request
            }
        )
        return context


# ROWS FETCH NEXT 6 ROWS ONLY
class DonateList(generics.ListAPIView):
    """
     Getting list of  donation
     """

    sql = Organ.objects.raw("SELECT * FROM Organ LIMIT 3 OFFSET 0")
    for i in sql:
        print(i.blood_group)
    queryset = sql

    serializer_class = DonateListSerializer


class DonateUpdateView(generics.UpdateAPIView):
    """
        updating donation if Mediuser is authenticated
    """

    permission_classes = [IsAuthenticated]
    queryset = Organ.objects.all()
    serializer_class = DonateSerializer
    lookup_field = 'id'


class DonateDeleteView(generics.DestroyAPIView):
    """
        deleting donation if Mediuser is authenticated
    """

    permission_classes = [IsAuthenticated]
    queryset = Organ.objects.all()
    serializer_class = DonateSerializer
    lookup_field = 'id'


class PostView(generics.CreateAPIView):
    """
    posting post if Mediuser is authenticated

    """

    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    # def get_serializer_context(self):
    #     context = super().get_serializer_context()
    #     context.update(
    #         {
    #             'request': self.request
    #         }
    #     )
    #     return context

    def get_queryset(self):
        return self.queryset.annonate(duration=F('start_date') - F('end_date'))


class PostListView(generics.ListAPIView):
    """
    listing post if Mediuser is authenticated
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'location']



class PostUpdateView(generics.UpdateAPIView):
    """
     updating post if Mediuser is authenticated
     """

    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": " updated successfully"})
        else:
            return Response({"message": "failed", "details": serializer.errors})


class PostDeleteView(generics.DestroyAPIView):
    """
        deleting post if Mediuser is authenticated
    """

    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = DonateSerializer
    lookup_field = 'id'


class NomineeView(generics.CreateAPIView):
    """
    register nominee if Mediuser is authenticated
    """

    permission_classes = [IsAuthenticated]
    queryset = Nominee.objects.all()
    serializer_class = NomineeSerializer


class NomineeListView(generics.ListAPIView):
    """
    listing nominee if Mediuser is authenticated
    """

    queryset = Nominee.objects.all()
    serializer_class = NomineeSerializer


class NomineeUpdateView(generics.UpdateAPIView):
    """
    updating nominee if Mediuser is authenticated
    """

    permission_classes = [IsAuthenticated]
    queryset = Nominee.objects.all()
    serializer_class = NomineeSerializer
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": " updated successfully"})
        else:
            return Response({"message": "failed", "details": serializer.errors})


class NomineeDeleteView(generics.DestroyAPIView):
    """
        deleting nominee if Mediuser is authenticated
    """

    permission_classes = [IsAuthenticated]
    queryset = Nominee.objects.all()
    serializer_class = NomineeSerializer
    lookup_field = 'id'

