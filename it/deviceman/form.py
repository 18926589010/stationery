from django import forms
from django.forms import fields
from deviceman.models import user_list, pc_list,dept_list,borrows


class UserModelForm(forms.ModelForm):

    class Meta:
        model = user_list    # 与models建立了依赖关系
        fields = "__all__"

class PcModelForm(forms.ModelForm):

    class Meta:
        model = pc_list    # 与models建立了依赖关系
        fields = "__all__"
        widgets = {

            'receive_date': forms.DateInput(attrs={'class': "form-control",
                                                   'placeholder': "YYYY-MM-DD"})
        }

class borrowsModelForm(forms.ModelForm):
    class Meta:
        model = borrows # 与models建立了依赖关系
        fields = "__all__"
