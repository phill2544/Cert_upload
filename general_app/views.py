import datetime
import json
import pathlib
from django.http import FileResponse
from datetime import date
from textwrap import wrap
from reportlab.lib import colors
from PyPDF3.pdf import BytesIO
from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import User_Detail, CertificateFile, Configuration, Province, Ministry, Verify_Certificatefile
from django.contrib.auth.models import User
from .forms import User_DetailForm, UserProfileForm, UserCreationForm, CertificateForm, Verify_CertificateForm
import os
import django
from django.core.mail import send_mail
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle, Spacer, Paragraph, Image, PageBreak, Frame, PageTemplate
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.contrib.auth import update_session_auth_hash
from Cert_upload import settings
# settings.EMAIL_HOST_USER = '5555@mail.com'
# print(settings.EMAIL_HOST_USER)

from django.contrib.admin.views.decorators import staff_member_required


# from django.http import FileResponse
# import io
# from reportlab.pdfgen import canvas
# from reportlab.lib.units import inch
# from django.views.generic import View
# from django.template.loader import get_template, render_to_string
# from fpdf import FPDF
# from reportlab.lib.pagesizes import A4
# from django.contrib.staticfiles import finders
# from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
# from xhtml2pdf import pisa
# from io import BytesIO
# from django.conf import settings
# from django.core.files.storage import FileSystemStorage
# from django.core import serializers
# from django.template import Template, Context


def month_th(month, short=None):
    if month == 1:
        if short:
            return "ม.ค."
        else:
            return "มกราคม"
    elif month == 2:
        if short:
            return "ก.พ."
        else:
            return "กุมภาพันธ์ "
    elif month == 3:
        if short:
            return "มี.ค."
        else:
            return "มีนาคม"
    elif month == 4:
        if short:
            return "เม.ย."
        else:
            return "เมษายน"
    elif month == 5:
        if short:
            return "พ.ค."
        else:
            return "พฤษภาคม"
    elif month == 6:
        if short:
            return "มิ.ย."
        else:
            return "มิถุนายน"
    elif month == 7:
        if short:
            return "ก.ค."
        else:
            return "กรกฎาคม"
    elif month == 8:
        if short:
            return "ส.ค."
        else:
            return "สิงหาคม"
    elif month == 9:
        if short:
            return "ก.ย."
        else:
            return "กันยายน"
    elif month == 10:
        if short:
            return "ต.ค."
        else:
            return "ตุลาคม"
    elif month == 11:
        if short:
            return "พ.ย."
        else:
            return "พฤศจิกายน"
    else:
        if short:
            return "ธ.ค."
        else:
            return "ธันวาคม"


def date_th(dates):
    cert_date = []
    try:
        for date in dates:
            cert_date.append('{} {} {}'.format(date.create_date.day, month_th(date.create_date.month),
                                               date.create_date.year + 543))
    except:
        cert_date.append('{} {} {}'.format(dates.day, month_th(dates.month),
                                           dates.year + 543))
    return cert_date


def delete_file():
    print('delete_def')
    if Configuration.objects.get(pk=1).delete_date_status:
        try:
            year = int(-Configuration.objects.get(pk=1).delete_date)
        except:
            year = -1
        certificates = CertificateFile.objects.filter(
            create_date__lte=date.today() + relativedelta(years=year))  # __lte = less than or equal
        for certificate in certificates:
            certificate.delete()
    pass
    return True


def send_email():
    if Configuration.objects.get(pk=1).sender_mail_status:
        try:
            month = int(Configuration.objects.get(pk=1).send_mail_date)
        except:
            month = 2
        try:
            users = User_Detail.objects.filter(send_email=False)[0]
            if (users.cal_date + relativedelta(months=-month)) < date.today():
                users.cal_date = (users.cal_date + relativedelta(years=1))
                users.send_email = True
                users.save()
                email = []
                for obj in User.objects.filter(is_superuser=True):
                    email.append(obj.email)
                email.append(users)
                try:
                    send_mail(
                        "แจ้งนัดล่วงหน้าเพื่อทำการตรวจสอบเครื่องมือแพทย์",
                        'เครื่องมือแพทย์ของท่านครบกำหนดทดสอบสอบเทียบ ในเดือน{} \nหากมีความประสงค์ทดสอบ สอบเทียบ สามารถติดต่อประสานงานได้ที่ กลุ่มวิศวกรรมการแพทย์ ศูนย์สนับสนุนบริการสุขภาพที่7 \nTel : 043-243738 \nE-mail : saraban-hss7@hss.mail.go.th'.format(
                            month_th(users.cal_date.month)),
                        '',
                        email,
                        fail_silently=False,
                    )
                except:
                    pass
        except:
            User_Detail.objects.all().update(send_email=False)
        if date.today().month == 10:
            User_Detail.objects.all().update(send_email=False)
    pass
    return True



def create_pdf(datas):
    img = Image('general_app/ตรากระทรวงสาธารณสุขใหม่.png', 50, 50)
    data = []
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="สรุปรายงานการอัปโหลดใบรับรองเครื่องมือแพทย์.pdf"'

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=5,
                            leftMargin=5,
                            topMargin=10,
                            bottomMargin=5, title='report of HSS7 {}'.format(date.today() + relativedelta(years=543)))

    pdfmetrics.registerFont(TTFont('THSarabun', 'general_app/THSarabunNew.ttf'))
    pdfmetrics.registerFont(TTFont('THSarabunB', 'general_app/THSarabunNew Bold.ttf'))
    data += [
        # header,
        [img, 'ศูนย์สนับสนุนบริการสุขภาพที่ 7','',''],
        ['', '', '', ''],
        ['วันที่ : {}'.format(date_th(date.today())[0]), '', ''],
        ['', '', '', ''],
        ['ตารางสรุปผลการอัปโหลดและดาวน์โหลด', '', ''],
        ['อัปโหลด', '{}'.format(User_Detail.objects.filter(is_upload=True).exclude(user__is_superuser=True).count()),
         'ยังไม่อัปโหลด',
         '{}'.format(User_Detail.objects.filter(is_upload=False).exclude(user__is_superuser=True).count())],
        ['ดาวน์โหลด', '{}'.format(CertificateFile.objects.filter(download_date__isnull=False).count()),
         'ยังไม่ดาวน์โหลด', '{}'.format(CertificateFile.objects.filter(download_date__isnull=True).count())],
        ['', '', '', ''],
        ['ตารางแสดงรายละเอียดวันที่อัปโหลดและดาวน์โหลด', '', '', ''],
        ['ลำดับที่', 'โรงพยาบาล', 'วันที่อัปโหลด', 'วันที่ดาวน์โหลด'],
    ]

    for count, item in datas.items():
        start = item['hospital'].username.index('บาล') + 3 if 'บาล' in item['hospital'].username else 0
        hospital = item['hospital'].username[start:]
        data += [
            [count + 1,
             hospital if len(hospital) <= 27 else hospital[0:27] + '...',
             item['upload_date'],
             item['download_date']]
        ]

    table = Table(data, colWidths=(2.2 * cm,6 * cm,4 * cm,4 * cm),rowHeights=1 * cm, vAlign='TOP', ) #colWidths=(2.2 * cm,6 * cm,4 * cm,4 * cm)
    table.setStyle(TableStyle([
        ('SPAN', (1, 0), (3, 0)),
        ('SPAN', (0, 2), (-1, 2)),
        ('ALIGN', (1, 0), (-1, 0), 'CENTER'),
        ('FONT', (1, 0), (-1, 0), 'THSarabunB'),#ศูนย์สนับสนุน
        ('FONTSIZE', (1, 0), (-1, 0), 30),  # header
        ('FONT', (0, 2), (-1, 2), 'THSarabun'),# วันที่
        ('FONTSIZE', (0, 2), (-1, 2), 18),
        ('FONT', (0, 4), (-1, 4), 'THSarabunB'),#ตารางสรุป
        ('FONTSIZE', (0, 4), (-1, 4), 20),  # header
        ('FONT', (0, 5), (-1, 6), 'THSarabun'),#อัปโหลด
        ('FONTSIZE', (0, 5), (-1, 6), 18),  # header
        ('FONT', (0, 8), (-1, 8), 'THSarabunB'),  # ตารางแสดงรายละเอียดวันที่
        ('FONTSIZE', (0, 8), (-1, 8), 20),  # header
        ('FONT', (0, 9), (-1, -1), 'THSarabun'),#ลำดับที่
        ('FONTSIZE', (0, 9), (-1, -1), 20),
        ('SPAN', (0, 4), (-1, 4)),
        ('ALIGN', (0, 4), (-1, 4), 'CENTER'),
        ('SPAN', (0, 8), (-1, 8)),
        ('ALIGN', (0, 8), (-1, 8), 'CENTER'),
        ('BOX', (0, 5), (-1, 6), 1, (0, 0, 0)),  # box in content
        ('INNERGRID', (0, 5), (-1, 6), 0.25, colors.black),
        ('BOX', (0, 9), (-1, -1), 1, (0, 0, 0)),  # box in content
        ('INNERGRID', (0, 9), (-1, -1), 0.25, colors.black),##ลำดับที่
        ('LINEBELOW', (0, 5), (-1, 6), 0.5, colors.black),
        ('ALIGN', (1, 5), (1, 6), 'CENTER'),
        ('ALIGN', (3, 5), (3, 6), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),

    ]))


    elems = [table]

    doc.build(elems)


    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


@login_required
def home(request, hospital_id=None,path=None):
    email_authen = None
    email_valid = None
    cert_date = []
    if request.user.is_authenticated:
        try:
            users = User.objects.all()
            if request.user.is_superuser:
                certs = CertificateFile.objects.all().order_by('-create_date')
            else:
                certs = CertificateFile.objects.filter(hospital_id=request.user.id)
            # date_th(cert)
        except:
            certs = CertificateFile.objects.filter()
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        if 'email' in request.POST:
            position = request.POST['position']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            number = request.POST['number']
            email_authen = request.POST['email']
            email_valid = request.POST['email_valid']
            if email_authen == email_valid:
                User_Detail.objects.filter(user_id=request.user.id).update(position=position, number=number)
                user.email = email_authen
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                messages.success(request, 'email success')
            else:
                messages.success(request, 'emails are not match')
                return render(request, 'general_app/home.html',
                              context={'email_authen': email_authen, 'email_valid': email_valid,
                                       'first_name': first_name,
                                       'last_name': last_name,
                                       'position': position,
                                       'number': number})
        if cert_date:
            cert_date = date_th(certs.create_date)
        return render(request, 'general_app/home.html',
                      {'certs': zip(certs, cert_date), 'users': users, 'email_authen': email_authen,
                       'email_valid': email_valid})  # 'certform': certform,
    elif hospital_id != None:
        if not request.user.is_superuser:
            CertificateFile.objects.filter(pk=hospital_id).update(download_date=datetime.date.today())
            # return HttpResponseRedirect(reverse('home'))
        else:
            pass
        file_server = pathlib.Path(path)
        if not file_server.exists():
            messages.error(request, 'file not found.')
        else:
            file_to_download = open(str(file_server), 'rb')
            response = FileResponse(file_to_download, content_type='application/force-download')
            response['Content-Disposition'] = 'inline; filename="a_name_to_file_client_hint"'
            return response
        return redirect(path)
        # return HttpResponseRedirect(reverse('home'))
    cert_date = date_th(certs)
    context = {'certs': zip(certs, cert_date), 'email_authen': email_authen, 'email_valid': email_valid,
               'users': users, }  # 'certform': certform,
    return render(request, 'general_app/home.html', context)


@login_required
def profile(request):
    state = None
    if request.method == "POST":
        form_auth = UserProfileForm(request.POST, instance=request.user)  # instance is update that user request
        form_user = User_DetailForm(request.POST)
        # print(form_auth)
        if form_user.is_valid():
            User.objects.filter(id=request.user.id).update(email=request.POST['email'],
                                                           first_name=request.POST['first_name'],
                                                           last_name=request.POST['last_name'])
            User_Detail.objects.filter(user_id=request.user.id).update(number=request.POST['number'],
                                                                       position=request.POST['position'])
            try:
                if User_Detail.objects.get(user_id=request.user.id).user_id:
                    # update
                    a = User_Detail.objects.filter(pk=request.user.user_detail.id).update(
                        province=form_user.cleaned_data['province'],
                        address=form_user.cleaned_data['address'],
                        ministry=form_user.cleaned_data['ministry'],
                        code=form_user.cleaned_data['code'])
                    messages.success(request, 'updated profile complete')

            except:
                profile = form_user.save(commit=False)
                profile.user = request.user
                profile.save()
        return HttpResponseRedirect(reverse(('profile')))
    else:
        form_auth = UserProfileForm(instance=request.user)
        try:
            form_user = User_DetailForm(instance=User_Detail.objects.get(pk=request.user.user_detail.id))  # instance
        except:
            form_user = User_DetailForm()
    form_user.fields['province'].queryset = Province.objects.filter(is_show=True)
    form_user.fields['ministry'].queryset = Ministry.objects.filter(is_show=True)
    context = {
        'form_user': form_user,
        'form_auth': form_auth,
        'user_information': {
            'user': User.objects.get(id=request.user.id),
            'detail': User_Detail.objects.get(user_id=request.user.id)
        },
        'state': state
    }

    return render(request, 'general_app/profile.html', context)


@login_required
def configuration(request):
    try:
        form_configuration = Configuration.objects.get(pk=1)
    except:
        form_configuration = Configuration.objects.create(pk=1)
    state = None
    if request.method == "POST":
        if 'add_province' in request.POST:
            if Province.objects.filter(province=request.POST['add_province']).exists():
                Province.objects.filter(province=request.POST['add_province']).update(is_show=1)
            else:
                Province.objects.create(province=request.POST['add_province'])
            state = 'เพิ่มจังหวัด {} เสร็จสิ้น'.format(request.POST['add_province'])
            messages.success(request, state)
            return HttpResponseRedirect(reverse('configuration'))
        elif 'add_ministry' in request.POST:
            if Ministry.objects.filter(ministry=request.POST['add_ministry']).exists():
                Ministry.objects.filter(ministry=request.POST['add_ministry']).update(is_show=1)
            else:
                Ministry.objects.create(ministry=request.POST['add_ministry'])
            state = 'เพิ่มกระทรวง {} เสร็จสิ้น'.format(request.POST['add_ministry'])
            messages.success(request, state)
            return HttpResponseRedirect(reverse('configuration'))
        elif 'select_province' in request.POST:
            Province.objects.filter(province=request.POST['select_province']).update(is_show=False)
            state = 'ลบจังหวัด {} เสร็จสิ้น'.format(request.POST['select_province'])
            messages.success(request, state)
            return HttpResponseRedirect(reverse('configuration'))
        elif 'select_ministry' in request.POST:
            Ministry.objects.filter(ministry=request.POST['select_ministry']).update(is_show=False)
            state = 'ลบกระทรวง {} เสร็จสิ้น'.format(request.POST['select_ministry'])
            messages.success(request, state)
            return HttpResponseRedirect(reverse('configuration'))
        elif 'is_send' in request.POST:
            form_configuration.sender_mail_status = not form_configuration.sender_mail_status
            form_configuration.save()
            messages.success(request, 'การตั้งค่าการส่งอีเมลถูกเปลี่ยนสถานะเรียบร้อย')
            return HttpResponseRedirect(reverse('configuration'))
        elif 'is_delete' in request.POST:
            form_configuration.delete_date_status = not form_configuration.delete_date_status
            form_configuration.save()
            messages.success(request,'การตั้งค่าการลบถูกเปลี่ยนสถานะเรียบร้อย')
            return HttpResponseRedirect(reverse('configuration'))
        else:
            Configuration.objects.filter(pk=1).update(delete_date=request.POST['delete_date'],send_mail_date=request.POST['send_mail_date'])
            state = 'เปลี่ยนการตั้งค่า วันที่ลบ: {}ปี วันที่ส่งอีเมล: {}เดือน'.format(Configuration.objects.get(id=1).delete_date,Configuration.objects.get(id=1).send_mail_date)
            messages.success(request, state)
            return HttpResponseRedirect(reverse('configuration'))
    province = Province.objects.filter(is_show=True)
    ministry = Ministry.objects.filter(is_show=True)
    context = {'form_configuration': form_configuration, 'province': province, 'ministry': ministry,
               'state': state}
    return render(request, 'general_app/configuration.html', context)


@login_required
def manage_user(request):
    try:
        a = Configuration.objects.get(id=1).delete_date
    except:
        a = -2
    state = None
    date = None
    form_user_detail = User_DetailForm()
    form_user_creation = UserCreationForm()
    users = User.objects.all()
    if request.method == 'POST':
        form_user_detail = User_DetailForm(request.POST)
        form_user_creation = UserCreationForm(request.POST)
        date = request.POST['cal_date_add_user']
        # cal_date = request.POST['cal_date']
        cal_date = '{}-{}-{}'.format(int(str(date).split('-')[2]) - 543, str(date).split('-')[1],
                                     str(date).split('-')[0])
        if form_user_creation.data['password'] == form_user_creation.data['confirm_password']:
            if form_user_detail and not User.objects.filter(username=request.POST['username']).exists():
                form_user_creation = User.objects.create_user(request.POST['username'], request.POST['email'],
                                                              request.POST['password'],
                                                              is_superuser=request.POST['is_superuser'])
                form_user_detail = User_Detail.objects.create(province_id=request.POST['province'],
                                                              address=request.POST['address'],
                                                              ministry_id=request.POST['ministry'],
                                                              cal_date=str(cal_date),
                                                              user_id=form_user_creation.id,
                                                              code=request.POST['code'],
                                                              password=request.POST['password'])
                state = 'register success'
                form_user_detail = User_DetailForm()
                form_user_creation = UserCreationForm()

            else:
                form_user_creation = form_user_creation
                form_user_detail = form_user_detail
                form_user_creation.username = ''
                state = 'exist user'
        else:  # password not match
            form_user_creation = form_user_creation
            form_user_detail = form_user_detail
            state = 'password not match'
    form_user_detail.fields['province'].queryset = Province.objects.filter(is_show=True)
    form_user_detail.fields['ministry'].queryset = Ministry.objects.filter(is_show=True)
    context = {'users': zip(users, User_Detail.objects.all()), 'form_user_detail': form_user_detail,
               'form_user_creation': form_user_creation, 'state': state, 'date': date}
    return render(request, 'general_app/manage_users.html', context)


@login_required
def edit_user(request):
    print("edit_user")
    users = User.objects.all()
    pk = User.objects.get(username=request.POST['username']).id
    name = User_Detail.objects.get(user_id=pk)
    # try:
    #     name = User_Detail.objects.get(user_id=pk)
    # except:
    #     name = User_Detail.objects.create(user_id=pk)
    if request.method == 'POST':
        form_user_detail = User_DetailForm(request.POST, instance=User_Detail.objects.get(user_id=name.user_id))
        user = User.objects.filter(id=pk)
        form_user = UserProfileForm(request.POST, instance=User.objects.get(id=name.user_id))
        cal_date = request.POST['cal_date_add_user'].split('-')
        User_Detail.objects.filter(user_id=pk).update(province_id=form_user_detail.data['province'],
                                                      ministry_id=form_user_detail.data['ministry'],
                                                      code=form_user_detail.data['code'],
                                                      address=form_user_detail.data['address'],
                                                      cal_date='{}-{}-{}'.format(str(int(cal_date[2]) - 543),
                                                                                 cal_date[1], cal_date[0]),
                                                      position=request.POST['position'])
        User.objects.filter(id=pk).update(email=form_user_detail.data['email'], first_name=request.POST['first_name'],
                                          last_name=request.POST['last_name'])
        user.update(email=request.POST['email'])
        return HttpResponseRedirect(reverse('manage_user'))
        # return HttpResponseRedirect(reverse('manage_user'))

    return HttpResponseRedirect(reverse('manage_user'))


@login_required
def delete_record(request, pk):
    id_user = CertificateFile.objects.get(id=pk).hospital_id
    # print(User_Detail.objects.get(user_id=id_user).is_upload)
    User_Detail.objects.filter(user_id=id_user).update(is_upload=False)
    # print(User_Detail.objects.get(user_id=id_user).is_upload)
    try:
        CertificateFile.objects.get(id=pk).delete()
        messages.success(request, 'deleted complete')
    except:
        messages.error(request, 'File does not exist')
    # User_Detail.objects.filter(user_id=request.user.id).update(is_upload=False)
    return HttpResponseRedirect(reverse('home'))


@login_required
def delete_user(request, name):
    id = User.objects.filter(username__contains=name)[0].id
    # User.objects.get(id=66).delete()
    try:
        User.objects.get(id=id).delete()
        messages.error(request, 'deleted user complete')
    except User.DoesNotExist:
        messages.error(request, 'User does not exist')
    return HttpResponseRedirect(reverse('manage_user'))


@login_required
def dashboard(request):
    data = {}
    state_upload = None
    state_download = None
    try:
        search = request.GET.getlist('search_users')
    except:
        search = None
    date_range_default_start = datetime.datetime(int(datetime.datetime.now().year) + 543, datetime.datetime.now().month,
                                                 datetime.datetime.now().day).strftime("%m/%d/%Y")  # for date_range
    date_range_default_end = datetime.datetime(int(datetime.datetime.now().year) + 543, datetime.datetime.now().month,
                                               datetime.datetime.now().day).strftime("%m/%d/%Y")  # for date_range
    # if 'daterange' in request.GET:
    if 'daterange' in request.GET:
        date_range = str(request.GET['daterange']).split('-')
        date_range_default_start = date_range[0]
        date_range_default_end = date_range[1]
        date_start = datetime.date(int(str(date_range[0]).split('/')[2]) - 543, int(str(date_range[0]).split('/')[0]),
                                   int(str(date_range[0]).split('/')[1]))
        date_end = datetime.date(int(str(date_range[1]).split('/')[2]) - 543, int(str(date_range[1]).split('/')[0]),
                                 int(str(date_range[1]).split('/')[1]))
    else:
        date_start = datetime.date.today()
        date_end = datetime.date.today()
    if not 'search_users' in request.GET and not (date_start != date_end):
        data = fecth_report(User.objects.all())
    elif 'search_users' in request.GET and not (date_start != date_end):
        data = fecth_report(User.objects.filter(username__in=request.GET.getlist('search_users')))
    elif date_start != date_end and not 'search_users' in request.GET:
        # search = User.objects.filter(username__in=request.GET.getlist('search_users'))
        data = fecth_report(CertificateFile.objects.filter(create_date__range=[str(date_start), str(date_end)]))
    elif date_start != date_end and 'search_users' in request.GET:
        id = User.objects.filter(username__in=request.GET.getlist('search_users')).values_list('id')
        data = fecth_report(
            CertificateFile.objects.filter(hospital_id__in=id).filter(create_date__range=[date_start, date_end]))
    if 'uploaded' in request.GET:
        new_data = {}
        for obj in data:
            if data[obj]['upload_date'] != '':
                new_data[obj] = data[obj]
        data = new_data
        state_upload = 'uploaded'
    elif 'not_upload' in request.GET:
        new_data = {}
        for obj in data:
            if not data[obj]['upload_date'] != '':
                new_data[obj] = data[obj]
        data = new_data
        state_upload = 'not_upload'
    if 'downloaded' in request.GET:
        new_data = {}
        for obj in data:
            if data[obj]['download_date'] != '':
                new_data[obj] = data[obj]
        data = new_data
        state_download = 'downloaded'
    elif 'not_download' in request.GET:
        new_data = {}
        for obj in data:
            if not data[obj]['download_date'] != '':
                new_data[obj] = data[obj]
        data = new_data
        state_download = 'not_download'
    if 'pdf' in request.GET:
        respone = create_pdf(data)
        return respone
    context = {
        'data': data,
        'users': User.objects.all().exclude(is_superuser=True),
        'date_range_default_start': date_range_default_start,
        'date_range_default_end': date_range_default_end,
        'searched': search,
        'state_upload': state_upload,
        'state_download': state_download
    }
    return render(request, 'general_app/dashboard.html', context)


@login_required
def test(request):
    return render(request, 'general_app/test.html', )


def fecth_report(obj):
    data = {}
    count = 0
    users = obj
    try:
        for user in users:
            user.id = user.hospital_id
    except:
        pass
    for user in users:
        # if not user.is_superuser:
        if User_Detail.objects.get(user_id=user.id).is_upload and CertificateFile.objects.filter(
                hospital_id=user.id).order_by('-create_date'):
            upload = CertificateFile.objects.filter(hospital_id=user.id).order_by('-create_date')[0]
            download_date = date_th(upload.download_date)[0] if upload.download_date != None else ''
            upload = date_th(upload.create_date)[0]
        else:
            upload = ''
            download_date = ''
        data[count] = {'hospital': user, 'download_date': download_date,
                       'upload_date': upload}
        count += 1
    return data


@login_required
def upload_certificate(request):
    try:
        verify_certificateform = Verify_CertificateForm(request.POST, request.FILES)
    except:
        verify_certificateform = Verify_CertificateForm()
    if request.method == "POST":
        if request.FILES and 'upload_file' in request.POST:
            if verify_certificateform.is_valid():
                try:
                    Verify_Certificatefile.objects.get(hospital_id=request.POST['hospital']).delete()
                    messages.error(request, 'uploaded file complete')
                except:
                    messages.error(request, 'uploaded file complete')
                # verify_certificateform.user_create = request.user.username
                # verify_certificateform.save()
                obj = verify_certificateform.save(commit=False)
                obj.user_create = request.user.username
                obj.save()
                email = []
                for obj in User.objects.filter(is_superuser=True).exclude(id=request.user.id):
                    email.append(obj.email)
                try:
                    send_mail(
                        'ใบรับรองเครื่องมือทางการแพทย์',
                        'ศูนย์สนับสนุนบริการที่7 ได้อัปโหลดใบรับรองเครื่องมือแพทย์บนเว็บไซต์{} \nกรุณาตรวจสอบความถูกต้องเอกสารของ{}'.format(request._current_scheme_host,User.objects.get(id=request.POST['hospital']).username),
                        '',
                        email,
                        fail_silently=False,
                    )
                except:
                    pass
            return HttpResponseRedirect(reverse('upload_certificate'))
        elif 'cert_id' in request.POST and not request.FILES:  ## editing
            Verify_Certificatefile.objects.filter(pk=request.POST['cert_id']).update(
                editing_message=request.POST['editing_message'], user_create=request.user.username,
                create_date=datetime.date.today())
            cert_editing = Verify_Certificatefile.objects.get(pk=request.POST['cert_id']).user_create
            messages.error(request, 'edited file complete')
            try:
                send_mail(
                    '{}ใบรับรองเกิดข้อผิดพลาด กรุณาแก้ไข'.format(User.objects.get(
                        pk=Verify_Certificatefile.objects.get(pk=request.POST['cert_id']).hospital_id).username),
                    '{}เอกสารเกิดข้อผิดพลาด กรุณาแก้ไข {}'.format(User.objects.get(
                        pk=Verify_Certificatefile.objects.get(pk=request.POST['cert_id']).hospital_id).username,
                                                                  request.POST['editing_message']),
                    '',
                    [User.objects.get(username=cert_editing).email],
                    fail_silently=False,
                )
            except:
                pass
            return HttpResponseRedirect(reverse('upload_certificate'))
        elif 'delete_cert' in request.POST and request.POST['delete_cert'] != '':
            try:
                file_cert = Verify_Certificatefile.objects.get(pk=request.POST['delete_cert'])
                file_cert.delete()
                messages.error(request, 'delete file complete')
            except:
                pass
            return HttpResponseRedirect(reverse('upload_certificate'))
        elif 'confirm_cert' in request.POST and request.user.username != Verify_Certificatefile.objects.get(
                id=request.POST['cert_id']).user_create:
            # Verify_Certificatefile.objects.get(pk=request.POST['delete_cert_id']).delete()
            post = request.POST.copy()
            post['hospital'] = User.objects.get(username=request.POST['hospital_id']).id
            certifi_form = CertificateForm(post, request.FILES)
            if certifi_form.is_valid():
                certifi_form.save()
                Verify_Certificatefile.objects.get(id=request.POST['cert_id']).delete()
                User_Detail.objects.filter(user_id=certifi_form.data['hospital']).update(is_upload=True)
                if User_Detail.objects.filter(is_upload=True).count() == User.objects.filter(is_superuser=False).count() or date.today().month == 10:
                    User_Detail.objects.all().update(is_upload=False)
                try:
                    user_email = User.objects.get(username=request.POST['hospital_id']).email
                except:
                    user_email = None
                try:
                    send_mail(
                        'ใบรับรองเครื่องมือทางการแพทย์',
                        'ศูนย์สนับสนุนบริการที่7 ได้ดำเนินการอัปโหลดใบรายงานผลทดสอบ สอบเทียบเรียบร้อยแล้ว ท่านสามารถดาวโหลดได้ที่ {} โดย username และ password ที่ท่านลงทะเบียนไว้ \n\nกลุ่มวิศวกรรมการแพทย์ ศูนย์สนับสนุนบริการสุขภาพที่7 \nTel. 043-243738 \nE-mail : saraban-hss7@hss.mail.go.th'.format(request._current_scheme_host),
                        '',
                        [user_email],
                        fail_silently=False,
                    )
                except:
                    pass
            return HttpResponseRedirect(reverse('upload_certificate'))
    verify_certificate_editing = Verify_Certificatefile.objects.filter(editing_message__isnull=False).exclude(
        editing_message__exact='')
    verify_certificate_confirm = Verify_Certificatefile.objects.filter(editing_message='')
    for index, file in enumerate(verify_certificate_editing):
        verify_certificate_editing[index].create_date = date_th(file.create_date)
    for index, file in enumerate(verify_certificate_confirm):
        verify_certificate_confirm[index].create_date = date_th(file.create_date)
    context = {
        'verify_certificateform': verify_certificateform,
        'verify_certificate_editing': verify_certificate_editing,
        'verify_certificate_confirm': verify_certificate_confirm,

    }
    return render(request, 'general_app/upload_certificate.html', context)


def changepassword_done(request):
    return HttpResponseRedirect(reverse('home'))


def change_password(request):
    if request.method == "POST":
        user_id = User.objects.get(username=request.user).id
        old_password = User_Detail.objects.get(user_id=user_id).password
        if request.POST['old_password'] == old_password:
            set_password = User.objects.get(id=user_id)
            set_password.set_password(str(request.POST['new_password2']))
            set_password.save()
            User_Detail.objects.filter(user_id=user_id).update(password=str(request.POST['new_password2']))
            update_session_auth_hash(request, set_password)
            messages.success(request, 'change_password_done')
        else:
            messages.success(request, 'old password not match')
            # return render(request,'general_app/profile.html',context={'not_match':True})
    return HttpResponseRedirect(reverse('profile'))
