# Generated by Django 3.1.3 on 2021-08-10 09:45

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('branchs', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='SavingType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('detail', models.CharField(default='', max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='', max_length=100)),
                ('middle_name', models.CharField(default='', max_length=100)),
                ('last_name', models.CharField(default='', max_length=100)),
                ('account_number', models.CharField(default='', max_length=100)),
                ('phone_number', models.CharField(default='', max_length=100)),
                ('document', models.ImageField(null=True, upload_to='Customer/documents')),
                ('photograph', models.ImageField(upload_to='Customer/Identification')),
                ('identification', models.ImageField(null=True, upload_to='Customer/Identification')),
                ('address', models.CharField(default='', max_length=100)),
                ('city', models.CharField(default='', max_length=100)),
                ('office_branch', models.CharField(default='', max_length=100)),
                ('active', models.BooleanField(default=False)),
                ('initial_deposit', models.FloatField(default=0)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('savings_type', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='branchs.ocssc_branch_office')),
            ],
        ),
        migrations.CreateModel(
            name='BankingHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('initial_value', models.FloatField(default=0, max_length=11, verbose_name=' ')),
                ('amount', models.FloatField(default=0, max_length=11, verbose_name=' ')),
                ('final_value', models.FloatField(default=0, max_length=6, verbose_name=' ')),
                ('transaction', models.CharField(max_length=100)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.customer')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone_number', models.CharField(blank=True, max_length=20)),
                ('photograph', models.ImageField(null=True, upload_to='user/photograph')),
                ('identification', models.ImageField(null=True, upload_to='user/Identification')),
                ('address', models.CharField(default='', max_length=100)),
                ('city', models.CharField(default='', max_length=100)),
                ('position', models.CharField(default='', max_length=100)),
                ('qualification_document', models.ImageField(null=True, upload_to='user/Qualification')),
                ('office_branch', models.CharField(max_length=100)),
                ('is_manager', models.BooleanField(default=False)),
                ('is_auditor', models.BooleanField(default=False)),
                ('is_customer_service', models.BooleanField(default=False)),
                ('is_system_admin', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=False)),
                ('date_of_hire', models.DateTimeField(null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
