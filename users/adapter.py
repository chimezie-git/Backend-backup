from allauth.account.adapter import DefaultAccountAdapter


class CustomAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=False):
        
        user = super().save_user(request, user, form, commit)
        data = form.cleaned_data
        user.email_verified = data.get('email_verified')[0]
        user.phone_verified = data.get('phone_verified')[0]
        user.phone_number = data.get('phone_number')
        user.otp_code = data.get('otp_code')
        user.otp_time = data.get('otp_time')
        user.referral_code = data.get('referral_code')
        user.save()
        return user