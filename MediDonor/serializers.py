from rest_framework import serializers

import io
from django.http import FileResponse
from reportlab.pdfgen import canvas

from MediDonor.models import Organ, Post, Nominee
from MediUser.models import MediUser, Donation
from .tasks import send_mail_post


class DonateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organ
        fields = ['blood_group', 'organ_age', 'organ_type']

    def create(self, validated_data):
        donor = self.context.get('request').user
        d = MediUser.objects.get(username=donor)
        dd = Organ.objects.create(user_id_id=d.id)
        dd.blood_group = validated_data['blood_group']
        dd.organ_age = validated_data['organ_age']
        dd.organ_type = validated_data['organ_type']
        dd.save()

        ddd = Organ.objects.filter(user_id_id=d.id).all()
        for dddd in ddd:
            ddddd = Donation.objects.create(user_id_id=d.id, organ_id_id=dddd.id)
            ddddd.save()
            buffer = io.BytesIO()
            # Create the PDF object, using the buffer as its "file."
            p = canvas.Canvas(buffer)
            # Draw things on the PDF. Here's where the PDF generation happens.
            # See the ReportLab documentation for the full list of functionality.
            p.drawString(100, 100, "{ddd}")
            # Close the PDF object cleanly, and we're done.
            p.showPage()
            p.save()
            # FileResponse sets the Content-Disposition header so that browsers
            # present the option to save the file.
            buffer.seek(0)
            return FileResponse(buffer, as_attachment=True, filename='donation.pdf')


class DonateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organ
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['username', 'date', 'title', 'location', 'description', 'start_date', 'end_date']

    def create(self, validated_data):
        posting = self.context.get('request').user
        p = MediUser.objects.get(username=posting)
        pp = Post.objects.create(user_id_id=p.id, username=p.username)
        pp.title = validated_data['title']
        pp.description = validated_data['description']
        pp.location = validated_data['location']
        pp.start_date = validated_data['start_date']
        pp.end_date = validated_data['end_date']
        pp.save()
        send_mail_post.delay(pp.id)
        return validated_data


class NomineeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nominee
        fields = ['username', 'date', 'nominee_name', 'nominee_email', 'nominee_mobile', 'relation']

    def create(self, validated_data):
        nominee = self.context.get('request').user
        n = MediUser.objects.get(username=nominee)
        nn = Nominee.objects.create(user_id=n.id, username=n.username)
        nn.nominee_name = validated_data['nominee_name']
        nn.nominee_email = validated_data['nominee_email']
        nn.nominee_mobile = validated_data['nominee_mobile']
        nn.relation = validated_data['relation']
        nn.save()
        return validated_data
