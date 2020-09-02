from django.contrib import messages, auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
# from django.urls import reverse_lazy
from accounts.forms import RegisterForm
from accounts.models import AuthUser, extendUserDetails
# from django.core.mail import send_mail, EmailMessage, get_connection
# Create your views here.
from mask_detection import settings


# connection = get_connection()


@login_required(login_url='admin-login')
def signup(response):
    if response.method == "POST":
        fetch_first_name = response.POST.get('first_name')
        fetch_last_name = response.POST.get('last_name')
        fetch_username = response.POST.get('username')
        fetch_email = response.POST.get('email')
        fetch_company_name = response.POST.get('companyName')
        fetch_mobile_number = response.POST.get('mobileNumber')
        print("email ", fetch_email)
        print("Company Name", fetch_company_name)
        print("Mobile Number", fetch_mobile_number)
        form = RegisterForm(response.POST)
        user_details = extendUserDetails()
        if form.is_valid():
            user = form.save(commit=False)

            # send_mail(subject, message, from_email, recipient_list, fail_silently=False, auth_user=None,
            #           auth_password=None, connection=None, html_message=None)¶

            # user.is_superuser = True
            user.is_staff = True

            # Start For ==> extendUserDetails table add details #
            user_details.first_name = fetch_first_name
            user_details.last_name = fetch_last_name
            user_details.username = fetch_username
            user_details.email = fetch_email
            user_details.company_name = fetch_company_name
            user_details.mobile_number = fetch_mobile_number

            print("EBUCB", user_details.email)
            # End extendUserDetails

            # user.is_active = False
            user.save()

            # return redirect("login")
            user_details.save()

            # email_subject = 'Activate Your Account'
            # email_message = 'Welcome to Hogist! '
            # email_body = 'Testing'
            # email = EmailMessage(
            #     email_subject,
            #     email_body,
            #     settings.EMAIL_HOST_USER,
            #     [user_details.email],
            # )
            # email.send(fail_silently=False)
            #
            # print("EMIAO", email.send())
            # connection.open()
            # subject = 'Thank you for subcribing our system'
            # message = 'Welcome to the Hogist mask detection and Social Distancing Service'
            # from_email = settings.EMAIL_HOST_USER
            # con = [
            #     settings.EMAIL_HOST_USER,
            #     settings.EMAIL_HOS_PASSWORD,
            #     False,
            # ]
            # print("CONNE",con)
            # to_list = [fetch_email, settings.EMAIL_HOST_USER]
            # send_mail(subject=subject, message='bwebc', from_email=from_email, connection=con,
            #           recipient_list=[str(user_details.email)], fail_silently=False)
            # send_mail(subject, message, from_email, to_list, fail_silently=True)
            return redirect("admin_userlist")
    else:
        print("else ma")
        form = RegisterForm()
        # return HttpResponse('error')
    return render(response, "signup.html", {'form': form})


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email)
        print(password)
        user = authenticate(username=email, password=password)
        print("USER", user)
        if user:
            login(request, user)
            print("Under GAYU")
            return redirect('index')
            # return HttpResponse('hi success,' + user.username)
        else:
            client_msg = "Oops you Entered Wrong Email and Password"
            return render(request, 'login.html', {'error_client_message': client_msg})
            # return redirect('login')
    return render(request, 'login.html')

    # @user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('login'))


def admin_login(request):
    if request.method == 'POST':
        fetch_email = request.POST.get('email')
        fetch_pasword = request.POST.get('password')
        print(fetch_email)
        user = authenticate(username=fetch_email, password=fetch_pasword)
        if user.is_superuser == True:
            login(request, user)
            return redirect('admin-index')
        elif user.is_superuser == False:
            message = "Oops...You Cannot access this Page...!! 😐"
            return render(request, 'admin/admin_login.html', {'error_message': message})
        # else:
        #     message = messages.error("Please try again...!!")
        #     return render(request, 'admin/admin_login.html', {'error_message':message})

        # try:
        #     adminDetails = admin_details.objects.get(email=fetch_email, password=fetch_pasword)
        #     if adminDetails is not None:
        #         return redirect('admin-index')
        # except admin_details.DoesNotExist:
        #     msg = messages.error(request, "Invalid Email or Password...Please Try Again")
        #     # print(msg)
        #     return render(request, "admin/admin_login.html")
        # for x in adminDetails:
        #     print(x.email)
        #     if x.email == fetch_email and x.password == fetch_pasword:
        #         return render(request, 'admin/admin-index.html')
        #     else:
        #         messages.error(request,"Invalid Email or Password...Please Try Again")
        #         # message = "Invalid Email or Password...Please Try Again"
        #         return render(request, 'admin/admin_login.html')
    return render(request, 'admin/admin_login.html')


@login_required(login_url='admin-login')
def admin_index(request):
    admin = []
    user = []

    admin_count = AuthUser.objects.filter(is_superuser=True).count()
    user_count = AuthUser.objects.filter(is_staff=True, is_superuser=False).count()

    admin.append(admin_count)
    user.append(user_count)

    content = {
        'total_admin': admin_count,
        'total_user': user_count,
        'admin_chart': admin,
        'user_chart': user
    }
    print("total admin", admin_count)
    print("total users", user_count)
    if request.method == 'POST':

        # total_admin = 0
        # total_user = 0
        # for x in data:
        #     if x.is_superuser is not None:
        #         total_admin += 1
        #     if x.is_superuser is  None:
        #         total_user += 1

        email1 = request.POST.get('addAdminEmail')
        print("email is ", email1)
        try:
            # Add User as Admin
            auth_user = AuthUser.objects.get(email=email1)
            auth_user.is_superuser = True
            auth_user.save()
            if auth_user is not None:
                return render(request, 'admin/admin_list.html')
        except AuthUser.DoesNotExist:
            return render(request, 'admin/admin-index.html')
    return render(request, 'admin/admin-index.html', content)


@login_required(login_url='admin-login')
def admin_UserList(request):
    userlist = AuthUser.objects.filter(is_staff=True, is_superuser=False)
    extendUser = extendUserDetails.objects.all()
    content = {
        'users_list': userlist,
        'extendUser': extendUser
    }
    # remove_user = request.POST.get('removeUser')
    # print("remove user", remove_user)
    if request.method == 'POST':
        remove_user = request.POST.get('removeUserEmail')
        print("remove_user", remove_user)
        try:
            removeUserAuthTable = AuthUser.objects.get(email=remove_user).delete()
            removeUserExtendUserTable = extendUserDetails.objects.get(email=remove_user).delete()
            message = {
                'message': removeUserAuthTable
            }
            return redirect('admin_userlist')
        except:
            return render(request, "admin/admin_UserList.html")
        return redirect('admin_userlist')
    return render(request, 'admin/admin_UserList.html', content)


@login_required(login_url='admin-login')
def admin_list(request):
    aadminList = AuthUser.objects.filter(is_superuser=True)
    content = {
        'admin_list': aadminList
    }
    return render(request, 'admin/admin_list.html', content)


@login_required(login_url='admin-login')
def admin_logout(request):
    auth.logout(request)
    return render(request, 'admin/admin_login.html')


@login_required(login_url='admin-login')
def admin_setting(request):
    current_user_username = request.user.username
    current_user_email = request.user.email
    current_user_firstname = request.user.first_name
    current_user_lastname = request.user.last_name
    current_user_date_join = request.user.date_joined
    data = {
        'username': current_user_username,
        'email': current_user_email,
        'firstname': current_user_firstname,
        'lastname': current_user_lastname,
        'datejoin': current_user_date_join
    }
    return render(request, 'admin/admin_setting.html', data)
