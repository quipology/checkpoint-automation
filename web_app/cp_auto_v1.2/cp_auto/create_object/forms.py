from django import forms

class GenerateSidsForm(forms.Form):
	username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Enter MDS username..'}))
	password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'placeholder': 'Enter MDS password..'}))

### Add Host Forms:
class AddHostFormCommercial(forms.Form):
	name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Should be IP\'s host name', 'class': 'form-control col-md-4'}))
	ip_address = forms.GenericIPAddressField(protocol='IPv4', widget=forms.TextInput(attrs={'placeholder': 'IP address', 'class': 'form-control col-md-4'}))
	comment = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Should be host\'s FQDN', 'class': 'form-control col-md-4'}))
	# add_to_grp = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'v-on:click': 'addToGrpFunc'}))
	grp_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control col-md-4', 'placeholder': 'Enter Existing Group Name'}))

class AddHostFormGovernment(forms.Form):
	name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Should be IP\'s host name', 'class': 'form-control col-md-4'}))
	ip_address = forms.GenericIPAddressField(protocol='IPv4', widget=forms.TextInput(attrs={'placeholder': 'IP address', 'class': 'form-control col-md-4'}))
	comment = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Should be host\'s FQDN', 'class': 'form-control col-md-4'}))
	# add_to_grp = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'v-on:click': 'addToGrpFunc'}))
	grp_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control col-md-4', 'placeholder': 'Enter Existing Group Name'}))

class AddHostFormAll(forms.Form):
	name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Should be IP\'s host name', 'class': 'form-control col-md-4'}))
	ip_address = forms.GenericIPAddressField(protocol='IPv4', widget=forms.TextInput(attrs={'placeholder': 'IP address', 'class': 'form-control col-md-4'}))
	comment = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Should be host\'s FQDN', 'class': 'form-control col-md-4'}))
	# add_to_grp = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'v-on:click': 'addToGrpFunc'}))
	grp_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control col-md-4', 'placeholder': 'Enter Existing Group Name'}))

### Add Network Forms:
class AddNetworkFormCommercial(forms.Form):
	name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Object Name', 'class': 'form-control col-md-4'}), label='Object Name')
	subnet = forms.GenericIPAddressField(protocol='IPv4', widget=forms.TextInput(attrs={'placeholder': 'Subnet', 'class': 'form-control col-md-4'}), label='Subnet')
	subnet_mask = forms.GenericIPAddressField(protocol='IPv4', widget=forms.TextInput(attrs={'placeholder': 'Subnet Mask', 'class': 'form-control col-md-4'}), label='Subnet Mask')
	comment = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Comment', 'class': 'form-control col-md-4'}), label='Comment (optional)', required=False)
	# add_to_grp = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'v-on:click': 'addToGrpFunc'}))
	grp_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control col-md-4', 'placeholder': 'Enter Existing Group Name'}))

class AddNetworkFormGovernment(forms.Form):
	name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Object Name', 'class': 'form-control col-md-4'}), label='Object Name')
	subnet = forms.GenericIPAddressField(protocol='IPv4', widget=forms.TextInput(attrs={'placeholder': 'Subnet', 'class': 'form-control col-md-4'}), label='Subnet')
	subnet_mask = forms.GenericIPAddressField(protocol='IPv4', widget=forms.TextInput(attrs={'placeholder': 'Subnet Mask', 'class': 'form-control col-md-4'}), label='Subnet Mask')
	comment = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Comment', 'class': 'form-control col-md-4'}), label='Comment (optional)', required=False)
	# add_to_grp = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'v-on:click': 'addToGrpFunc'}))
	grp_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control col-md-4', 'placeholder': 'Enter Existing Group Name'}))

class AddNetworkFormAll(forms.Form):
	name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Object Name', 'class': 'form-control col-md-4'}), label='Object Name')
	subnet = forms.GenericIPAddressField(protocol='IPv4', widget=forms.TextInput(attrs={'placeholder': 'Subnet', 'class': 'form-control col-md-4'}), label='Subnet')
	subnet_mask = forms.GenericIPAddressField(protocol='IPv4', widget=forms.TextInput(attrs={'placeholder': 'Subnet Mask', 'class': 'form-control col-md-4'}), label='Subnet Mask')
	comment = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Comment', 'class': 'form-control col-md-4'}), label='Comment (optional)', required=False)
	# add_to_grp = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'v-on:click': 'addToGrpFunc'}))
	grp_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control col-md-4', 'placeholder': 'Enter Existing Group Name'}))

### Add Network Group Forms:
class AddNetworkGroupFormCommercial(forms.Form):
	name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Object-Group Name', 'class': 'form-control col-md-4'}), label='Network Group Name')

class AddNetworkGroupFormGovernment(forms.Form):
	name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Object-Group Name', 'class': 'form-control col-md-4'}), label='Network Group Name')

class AddNetworkGroupFormAll(forms.Form):
	name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Object-Group Name', 'class': 'form-control col-md-4'}), label='Network Group Name')

### Copy Network Group Forms:
COMMERCIAL_CHOICES = [
	('government', 'Government')
	]
GOVERNMENT_CHOICES = [
	('commercial', 'Commercial')
	]

class CopyNetworkGroupCommercial(forms.Form):
	domain = forms.ChoiceField(choices=COMMERCIAL_CHOICES, label='Select Domain to Copy From', widget=forms.Select(attrs={'class': 'form-control col-md-1'}))
	grp_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Object-Group Name', 'class': 'form-control col-md-4'}), label='Name of the Network Group to Copy')

class CopyNetworkGroupGovernment(forms.Form):
	domain = forms.ChoiceField(choices=GOVERNMENT_CHOICES, label='Select Domain to Copy From', widget=forms.Select(attrs={'class': 'form-control col-md-1'}))
	grp_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Object-Group Name', 'class': 'form-control col-md-4'}), label='Name of the Network Group to Copy')

### Add Service Forms:
SERVICE_TYPES = [
	('tcp', 'TCP'),
	('udp', 'UDP')
	]
class AddService(forms.Form):
	name = forms.CharField(max_length=100, label='Service Object Name', widget=forms.TextInput(attrs={'placeholder': 'Service Object Name', 'class': 'form-control col-md-4'}))
	service_type = forms.ChoiceField(choices=SERVICE_TYPES, label='Service Type', widget=forms.Select(attrs={'class': 'form-control col-md-1'}))
	port = forms.CharField(max_length=11, label='Port Number/Range', widget=forms.TextInput(attrs={'placeholder': 'ex.: 445 or range: 110-115', 'class': 'form-control col-md-4'}))
	comment = forms.CharField(max_length=200, required=False, label='Comment (optional)', widget=forms.TextInput(attrs={'placeholder': 'Comment', 'class': 'form-control col-md-4'}))
	
	def clean_port(self):
		passed_port = self.cleaned_data.get('port')
		pool = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()+=_.,<>[]'
		for i in passed_port:
			if i in pool:
				raise forms.ValidationError('Not a valid port number. Please try again')
		return passed_port
