from django.contrib.auth.tokens import PasswordResetTokenGenerator

class UserVerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return f"{user.pk}{timestamp}{user.is_active}"

user_tokenizer_generate = UserVerificationTokenGenerator()
