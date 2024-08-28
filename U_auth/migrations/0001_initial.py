# Generated by Django 5.0.8 on 2024-08-28 14:05

import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionalDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_married', models.BooleanField(default=False)),
                ('auual_income', models.BigIntegerField()),
                ('family_type', models.CharField(max_length=50)),
                ('family_name', models.CharField(max_length=50)),
                ('father_name', models.CharField(max_length=50)),
                ('father_occupation', models.CharField(max_length=50)),
                ('mother_name', models.CharField(max_length=50)),
                ('mother_occupation', models.CharField(max_length=50)),
                ('total_siblings', models.IntegerField()),
                ('total_siblings_married', models.IntegerField()),
                ('height', models.IntegerField()),
                ('weight', models.IntegerField()),
                ('blood_group', models.CharField(max_length=50)),
                ('religion', models.CharField(max_length=50)),
                ('caste_or_community', models.CharField(max_length=50)),
                ('complexion', models.CharField(max_length=50, null=True)),
            ],
            options={
                'verbose_name': 'Additional Detail',
                'verbose_name_plural': 'Additional Details',
            },
        ),
        migrations.CreateModel(
            name='Country_codes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_code', models.CharField(max_length=10, unique=True)),
                ('country_name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='languages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserPersonalDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.IntegerField()),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=10)),
                ('dob', models.DateField()),
                ('smoking_habits', models.BooleanField(default=False, verbose_name='Smoking Habits')),
                ('drinking_habits', models.BooleanField(default=False, verbose_name='Drinking Habits')),
                ('qualification', models.CharField(max_length=50)),
                ('profile_pic', models.ImageField(blank=True, default='img/default_pic.png', upload_to='images/')),
                ('short_video', models.FileField(blank=True, null=True, upload_to='videos/')),
                ('is_employer', models.BooleanField(default=False)),
                ('is_employee', models.BooleanField(default=False)),
                ('is_jobseeker', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'User Personal Detail',
                'verbose_name_plural': 'User Personal Details',
            },
        ),
        migrations.CreateModel(
            name='UserDisabilities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disability_type', models.CharField(max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='U_auth.additionaldetails')),
            ],
        ),
        migrations.CreateModel(
            name='Pictures',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photos', models.ImageField(blank=True, upload_to='images/')),
                ('add_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='U_auth.userpersonaldetails', verbose_name='reverse_user_pic')),
            ],
        ),
        migrations.CreateModel(
            name='Intrestes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intrest', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='U_auth.userpersonaldetails')),
            ],
        ),
        migrations.CreateModel(
            name='Hobbies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hobby', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='U_auth.userpersonaldetails')),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('phone', models.CharField(max_length=10, unique=True, validators=[django.core.validators.RegexValidator(message='Phone number must be 10 digits only.', regex='^\\d{10}$')])),
                ('is_online', models.BooleanField(default=False)),
                ('country_details', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reverse_User_country', to='U_auth.country_codes')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_language', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reverse_User_lang', to='U_auth.languages')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='userpersonaldetails',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_details', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Relationship_Goals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_short', models.BooleanField(default=False)),
                ('is_long', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp_code', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_validated', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Job_Details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=100)),
                ('job_title', models.CharField(max_length=100)),
                ('designation', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=100)),
                ('experiences_level', models.CharField(choices=[('entry', 'Entry Level'), ('mid', 'Mid Level'), ('senior', 'Senior Level')], max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='additionaldetails',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
