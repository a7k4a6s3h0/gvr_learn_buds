from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from . permissions import RedirectAuthenticatedUserMixin
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from django.urls import reverse_lazy
from django.urls import reverse
from .otp import generate_otp, validate_otp
from .models import AdditionalDetails, CustomUser, OTP, UserPersonalDetails
from .forms import *
from django.views import View
# Create your views here.

# def demo(request):
    # return render(request, 'base_files/base.html')

def login_view(request):
    return render(request, 'login.html')
def perdet_view(request):
    return render(request, 'personal details.html')
def jobst(request):
    return render(request, 'job status.html')
def jobd(request):
    return render(request, 'Job Details.html')
def jobd1(request):
    return render(request, 'Job Details2.html')
def relation(request):
    return render(request, 'Relationship.html')
def interest(request):
    return render(request, 'Interested.html')
def adddet(request):
    return render(request, 'Additional details.html')

def user_details(request):
    return render(request, 'User_profile_templates/user_pr_1.html')

def user_details_2(request):
    return render(request, 'User_profile_templates/user_pr_2.html')


def user_details_3(request):
    return render(request, 'User_profile_templates/user_pr_3.html')

def user_details_4(request):
    return render(request, 'User_profile_templates/user_pr_4.html')


def user_details_5(request):
    return render(request, 'User_profile_templates/user_pr_5.html')

def user_details_6(request):
    return render(request, 'User_profile_templates/user_pr_6.html')


def AuthPage(request):

    context = {
        'experance_level': ['Beginner', 'Intermediate', 'Expert'],
        'marital_status': ['Unmarried', 'Divorced']
    }
    return render(request, 'auth/auth.html',context)



def error_404(request):
    return render(request, 'Errors/404.html')


def error_403(request):
    return render(request, 'Errors/403.html')


# ................................backend code starting..............................................


class SignupView(FormView):
    
    template_name = 'auth/auth.html'  # The template to render
    form_class = CreateUser
    # success_url = reverse_lazy('signup')  # URL to redirect to after successful form submission

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['experance_level'] = ['entry', 'mid', 'senior']
        # context['experance_level'] = ['Beginner', 'Intermediate', 'Expert']
        context['marital_status'] = ['Unmarried', 'Divorced']
        return context
    
    def get_form_kwargs(self):
        """
        Passes the request data to the form.
        """
        # Get the default form kwargs
        kwargs = super().get_form_kwargs()

        # Add the request data to the form kwargs
        # kwargs['data'] = self.request.POST or None
        # kwargs['files'] = self.request.FILES or None

        print(kwargs, "***********************************")

        return kwargs

    def form_valid(self, form):
        # Handle form validation and user creation here

        
        user = form.save()  # Save the form data to create a new user
        print(f"User created: {user}")  # Debugging

        if user:
            # Generate OTP after the user is created
            otp_code = generate_otp(user)
            print(f"Generated OTP: {otp_code}")  # Debugging
            self.request.session['user'] = user.email
            # Add a message to the context that OTP was generated successfully
            messages.success(self.request, "OTP generated successfully.")


        response = super().form_valid(form)

        print(response, "response...................!!!!!!!!!!!!!")  # Debugging
        return response
    

    def form_invalid(self, form):
        # Render the form with errors and trigger the signup modal
        return self.render_to_response(self.get_context_data(form=form, show_signup_modal=True))

    # Redirect to the CheckOTPView URL
    def get_success_url(self):
        # Store context data in the session
        self.request.session['purpose'] = 'newuser_verification'
        # sending message for otp useage
        messages.success(self.request, "For user verification..!!")
        return reverse('check_otp')
    
# code need to change remember
class CheckOTPView(RedirectAuthenticatedUserMixin, FormView):
    purpose_1 : str = ''
    template_name = 'auth/otp_input.html'  # The template to render
    form_class = GenerateOTP


    def get_url(self, purpose):
        url_dict = {
            'newuser_verification':'home',
            'pass_verification':'auth_page',
            'reset_pass_verification': 'pass_reset_2'
        }
        return url_dict.get(purpose, None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Retrieve context data from the session
        context['purpose'] = self.request.session.get('purpose', None)
        return context

    # If no request purpose is found, redirect to the login page (or any other page)
    def get(self, request: HttpRequest, *args: str, **kwargs: dict) -> HttpResponse:

        self.purpose_1 = self.request.session.get('purpose', None)   # Retrieve purpose from session
        
        if not self.purpose_1:
            # If no purpose is found, redirect to the login page (or any other page)
            messages.error(self.request, "Unauthorized access. Please try again.")
            return redirect(reverse('auth_page'))
        
        return super().get(request, *args, **kwargs)  # Call the parent's get method
    
    def form_valid(self, form):
        
        # Retrieve the cleaned data from the form
        User_otp_code = ''.join([form.cleaned_data['digit1'],
                            form.cleaned_data['digit2'],
                            form.cleaned_data['digit3'],
                            form.cleaned_data['digit4']])  
        
        # Retrieve the purpose from the session
        purpose = self.request.session.get('purpose', None)
        boolen, msg, = validate_otp(User_otp_code)
        if boolen:
            # create session for user
            current_user = OTP.objects.get(otp_code=User_otp_code)
            if purpose == 'newuser_verification':
                print("in session creation")
                login(self.request, current_user.user)
            # OTP is valid
            # messages.success(self.request, msg)
            return super().form_valid(form)
        else:
            # OTP is invalid
            form.add_error(None, msg)
            return self.form_invalid(form)

    
    def get_success_url(self):
        
        purpose = self.request.session.get('purpose', None)  # Remove purpose from session

        # Get the URL name from the purpose
        url_name = self.get_url(purpose)

        if url_name:
            # If the URL name is valid, reverse it
            return reverse_lazy(url_name)
        else:
            # If the URL name is None, redirect to a default page or raise an error
            messages.error(self.request, "Unable to determine the redirect URL. Please try again.")
            return reverse_lazy('auth_page')


class ResendOTPView(FormView):
    template_name = 'auth/otp_input.html'
    # success_url = reverse_lazy('check_otp')  # URL to redirect to after successful OTP generation

    # Define a dummy form class if your view requires a form but you don't need any input
    class DummyForm(forms.Form):
        pass

    form_class = DummyForm  # Specify a form class even if it's a dummy one

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Retrieve context data from the session
        context['purpose'] = self.request.session.get('purpose', None)
        return context


    def get(self, request, *args, **kwargs):
        # Retrieve the purpose and user email from the session
        purpose = self.request.session.get('purpose')
        user_email = self.request.session.get('user')

        if not purpose:
            # If no purpose is found, redirect to the login page (or any other page)
            messages.error(self.request, "No purpose found. Please try again.")
            return redirect(reverse('auth_page'))
        elif not user_email:
            # If no user email is found, redirect to the login page (or any other page)
            messages.error(self.request, "No user email found. Please try again.")
            return redirect(reverse('auth_page'))

        try:
            current_user = CustomUser.objects.get(email=user_email)  # Ensure you're using the correct model
            # Generate OTP after the user is found
            otp_code = generate_otp(current_user)
            print(f"Generated OTP: {otp_code}")  # Debugging
            messages.success(self.request, "Resend OTP generated successfully")
            return super().get(request, *args, **kwargs)  # Call the parent's get method to render the form

        except CustomUser.DoesNotExist:
            # If the user does not exist, redirect to the login page (or any other page)
            messages.error(self.request, "User does not exist. Please try again.")
            return redirect(reverse('auth_page'))

class LoginView(FormView):

    template_name = 'auth/auth.html'
    form_class = LoginForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        """
        If the form is valid, authenticate and log in the user.
        """
        email_or_phone = form.cleaned_data['email_or_phone']
        password = form.cleaned_data['password']

        user = authenticate(email=email_or_phone, password=password)

        if user is not None:
            login(self.request, user)
            return super().form_valid(form)  # Redirects to success_url
        else:
            # Add a non-field error to the form
            form.add_error(None, "Invalid username or password.")
            return self.form_invalid(form)  # Redirects to error handling
    
    def form_invalid(self, form):
        # Render the form with errors and trigger the login modal
        return self.render_to_response(self.get_context_data(form=form, show_login_modal=True))
    
    def get_success_url(self):
        # Redirect to a success URL after form submission
        return reverse_lazy('home')
    

class UserLogout(LoginRequiredMixin,View):
    login_url = 'auth_page'
    def get(self, request):
        logout(request)
        # Redirect to the login page or any other page after logout
        return redirect('auth_page')

class ForgotPassword(FormView):
    template_name = 'auth/auth.html'
    form_class = ForgotPasswordForm
    # success_url = reverse_lazy('check_otp')

    def form_valid(self, form):
        password = form.cleaned_data['current_password']
        current_user = CustomUser.objects.get(password=password)
        if check_password(password, current_user.password):
            messages.error(self.request, "Not Found..!!!")
        else:
            current_user.set_password(password)  # Set the new password (Django will hash it)
            current_user.save()  # Save the updated user
            messages.success(self.request, "Password changed successfully.")

        return super().form_valid(form)
    
    def get_success_url(self):
        # sending message for otp useage
        messages.success(self.request, "Verification for Password Changing..!!")
        # Redirect to a success URL after form submission
        return reverse_lazy('auth_page')
    
class ResetPassword(RedirectAuthenticatedUserMixin, FormView):
    template_name = 'auth/auth.html'
    form_class = ResetPasswordForm
    items = ['email', 'phone']

    def form_valid(self, form):
        email_or_phone = form.cleaned_data.get('email_or_phone', None)
        
        try:
            if '@' in email_or_phone:
                user = CustomUser.objects.get(email=email_or_phone)
            else:
                user = CustomUser.objects.get(phone=email_or_phone)
            self.request.session['user'] = user.email
            otp_code = generate_otp(user)
            print(f"Generated OTP: {otp_code}")  # Debugging
            messages.success(self.request, f"OTP sent to your {self.items}")
            
            # Redirect to the OTP verification page
            return super().form_valid(form)
        
        except CustomUser.DoesNotExist:
            # Handle the case where the user does not exist
            messages.error(self.request, "User doesn't exist..!!")
            # Render the form with errors without redirecting
            # return self.form_invalid(form)
            return self.render_to_response(self.get_context_data(form=form, show_resetPass_modal=True))

    def get_success_url(self):
        # Store context data in the session
        self.request.session['purpose'] = 'reset_pass_verification'
        
        # Sending message for OTP usage
        messages.success(self.request, "Verification for password changing..!!")
        # Redirect to a success URL after form submission
        return reverse_lazy('check_otp')

class ResetPassword_2(FormView):

    template_name = 'auth/get_pass.html'
    form_class = ResetPasswordForm_2
    # success_url = reverse('auth_page')

    # If no request purpose is found, redirect to the login page (or any other page)
    def get(self, request: HttpRequest, *args: str, **kwargs: dict) -> HttpResponse:

        # Perform validation here
        user_email = request.session.get('user', None)

        if not user_email:
            # If no user is found in the session, redirect to the login page with an error message
            messages.error(request, "Unauthorized access. Please try again.")
            return redirect(reverse('auth_page'))

        return super().get(request, *args, **kwargs)  # type: ignore

    def form_valid(self, form):
        # Retrieve the user from the session
        try:
            password = form.cleaned_data.get('password_2')
            user_email = self.request.session.pop('user', None)            
            user = CustomUser.objects.get(email=user_email)
            user.set_password(password)
            user.save()
            messages.success(self.request, "Password changed successfully")
            return super().form_valid(form)
        except CustomUser.DoesNotExist:
            # Handle the case where the user does not exist
            messages.error(self.request, "User doesn't exist..!!")
            # Render the form with errors without redirecting
            return self.form_invalid(form)
        
    def get_success_url(self):
        # Redirect to a success URL after form submission
        self.request.session.pop('user', None) # remove user data from session 
        self.request.session.pop('purpose', None)
        return reverse_lazy('auth_page')


class UserPersonalDetailsView(FormView):
    template_name = 'auth/auth.html'
    form_class = UserPersonalDetailsForm


    def get_form_kwargs(self):
        """
        Passes the request data to the form.
        """
        kwargs = super().get_form_kwargs()
        # Get the default form kwargs
        kwargs['user'] = self.request.user  # Pass the user to the form

        print(kwargs, "***********************************")

        return kwargs


    def form_valid(self, form):
        photos = form.files.getlist('photos', None)
        print(photos,"****************************************")
        details = form.save()
        print(details,"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        return super().form_valid(form)
    
    def form_invalid(self, form: Any) -> HttpResponse:
        print("in")
        return self.render_to_response(self.get_context_data(form=form, show_personaldetails_modal=True))
    
    def get_success_url(self) -> str:
        return reverse_lazy('auth_page')
    

class JobDetailsView(FormView):
    template_name = 'auth/auth.html'
    form_class = JobDetailsForm    

    def get_form_kwargs(self):
        """
        Passes the request data to the form.
        """
        kwargs = super().get_form_kwargs()
        # Get the default form kwargs
        # kwargs['user'] = self.request.user  # Pass the user to the form

        print(kwargs, "***********************************")

        return kwargs

    def form_valid(self, form: Any) -> HttpResponse:
        job = form.save(commit=False)
        print(job,"jjjjjjjjjjjjjjjjjjjjjjjjjj")
        return super().form_valid(form)
    
    def form_invalid(self, form: Any) -> HttpResponse:
        
        return self.render_to_response(self.get_context_data(form=form, show_jobdetails_modal=True))
    
    def get_success_url(self) -> str:
        return reverse_lazy('auth_page')
    

class AdditionalDetailsView(FormView):
    template_name = 'auth/auth.html'
    form_class = AdditionalDetailsForm

    def form_valid(self, form: Any) -> HttpResponse:
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return super().get_success_url()