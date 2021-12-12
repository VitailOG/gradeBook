from django.shortcuts import redirect


class LoginRequiredAndMethodistPermissions:
	user = None

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			if request.user.group.name != self.user:
				print(self.user)
				return redirect('auth')
		else:
			return redirect('auth')
		return super().dispatch(request, *args, **kwargs)
