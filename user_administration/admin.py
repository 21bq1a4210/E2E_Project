from django.contrib import admin
from .models import Class, CustomUser, Branch, Student, Role, HeadOfDepartment, Counsellor, ClassTeacher
from .escalation_models import EscalationStructure
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, SetPasswordForm, BaseUserCreationForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'role', 'image', 'password')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'role', 'image')


# Register your models here.
@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('branch', 'section')


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['branch']


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'image', 'role')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'id', 'roll_no', 'branch', 'year', 'counsellor', 'class_room')


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['role']


@admin.register(EscalationStructure)
class EscalationStructureAdmin(admin.ModelAdmin):
    list_display = ('id', 'role')


@admin.register(HeadOfDepartment)
class HeadOfDepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'branch')


@admin.register(Counsellor)
class CounsellorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')


@admin.register(ClassTeacher)
class ClassTeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'class_room')

