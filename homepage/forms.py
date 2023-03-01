from django import forms
from .models import UserRequest


class StockRequestForm(forms.ModelForm):
    class Meta:
        model = UserRequest
        fields = ["symbol", "start_date", "end_date", "num_epochs", "batch_size"]
# class SignUpForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ["firstname", "lastname", "phone", "email", "username", "password"]
#         labels = {"firstname": "First Name", "lastname": "Last Name", "phone": "Phone Number", "email": "Email Address", "username": "Desired Username", "password": "Password"}



# class StudentSignUpForm(UserCreationForm):
#     first_name = forms.CharField(required=True)
#     last_name = forms.CharField(required=True)
#     phone_number = forms.CharField(required=True)
#     class_name = forms.CharField(required=True)

#     class Meta(UserCreationForm.Meta):
#         model = User
    
#     @transaction.atomic
#     def data_save(self):
#         user = super().save(commit=False)
#         user.first_name = self.cleaned_data.get('first_name')
#         user.last_name = self.cleaned_data.get('last_name')
#         user.is_student = True
#         user.save()
#         student = Student.objects.create(user=user)
#         student.class_name = self.cleaned_data.get('class_name')
#         student.phone_number = self.cleaned_data.get('phone_number')
#         student.save()
#         return user


# class TeacherSignUpForm(UserCreationForm):
#     first_name = forms.CharField(required=True)
#     last_name = forms.CharField(required=True)
#     department = forms.CharField(required=True)

#     class Meta(UserCreationForm.Meta):
#         model = User
    
#     @transaction.atomic
#     def data_save(self):
#         user = super().save(commit=False)
#         user.first_name = self.cleaned_data.get('first_name')
#         user.last_name = self.cleaned_data.get('last_name')
#         user.is_teacher = True
#         user.save()
#         teacher = teacher.objects.create(user=user)
#         teacher.phone_number = self.cleaned_data.get('phone_number')
#         teacher.department = self.cleaned_data.get('department')
#         teacher.save()
#         return user