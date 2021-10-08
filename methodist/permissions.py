from django.http import HttpResponse
from django.shortcuts import redirect


class LoginRequiredAndMethodistMixin:
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			if request.user.group.name != 'Методист':
				return redirect('auth')
		else:
			return redirect('auth')
		return super().dispatch(request, *args, **kwargs)