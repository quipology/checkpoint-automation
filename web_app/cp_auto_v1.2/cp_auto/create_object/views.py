import web_base
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import (
	GenerateSidsForm,
	AddHostFormCommercial,
	AddHostFormGovernment,
	AddHostFormAll,
	AddNetworkFormCommercial,
	AddNetworkFormGovernment,
	AddNetworkFormAll,
	AddNetworkGroupFormCommercial,
	AddNetworkGroupFormGovernment,
	AddNetworkGroupFormAll,
	CopyNetworkGroupCommercial,
	CopyNetworkGroupGovernment,
	AddService
	)


# Create your views here.
@login_required
def home(request):
	context = {}
	return render(request, 'home/home.html', context)

###########################
### Generate Token View ###
###########################
@login_required
def generate_sids(request):
	if request.method == 'GET':
		form = GenerateSidsForm()
		context = {'form': form}
		return render(request, 'gen_sids/gen_sids.html', context)

	elif request.method == 'POST':
		form = GenerateSidsForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			sids = web_base.login(username, password)
			if sids == False:
				form = GenerateSidsForm()
				error = 'Login failed - try again.'
				context = {'form': form, 'error': error}
				return render(request, 'gen_sids/failed_login.html', context)
			else:
				# Checkpoint SID tokens:
				com_sid = sids[0]
				gov_sid = sids[1] 

				# Add Checkpoint SID tokens to user's web session:
				request.session['com_sid'] = com_sid
				request.session['gov_sid'] = gov_sid
				request.session.set_expiry(3600)

				form = GenerateSidsForm()
				context = {'form': form, 'comsid': com_sid, 'govsid': gov_sid}
				return render(request, 'gen_sids/recvd_sids_new.html', context)
		else:
			form = GenerateSidsForm()
			error = 'Invalid input.'
			context = {'form': form, 'error': error}
			return render(request, 'gen_sids/gen_sids.html', context)

######################
### Add Host Views ###
######################
@login_required
def add_host_commercial(request):
	if request.method == 'GET':

		# If user hasn't gotten their tokens yet, force them to login:
		if request.session.get('com_sid') == None:
			return redirect('gensids')

		form = AddHostFormCommercial()
		context = {'form': form}
		return render(request, 'addhost/add_host_commercial.html', context)

	elif request.method == 'POST':
		form = AddHostFormCommercial(request.POST)
		if form.is_valid():
			# com_sid = form.cleaned_data.get('com_sid')
			com_sid = request.session.get('com_sid')
			name = form.cleaned_data.get('name')
			ip_address = form.cleaned_data.get('ip_address')
			comment = form.cleaned_data.get('comment')
			grp_name = form.cleaned_data.get('grp_name')
			if not comment:
				if grp_name:
					status = web_base.add_host(com_sid, name, ip_address, add_to_grp=True, grp_name=grp_name)
				else:
					status = web_base.add_host(com_sid, name, ip_address)
			elif comment:
				if grp_name:
					status = web_base.add_host(com_sid, name, ip_address, comments=comment, add_to_grp=True, grp_name=grp_name)
				else:
					status = web_base.add_host(com_sid, name, ip_address, comments=comment)
			if status == 200:
				web_base.publish_changes(com_sid)
				success = "Host '{}' added successfully!".format(name)
				context = {'form': form, 'success': success}
				return render(request, 'addhost/add_host_commercial.html', context)
			else:
				error = "Failed to add host '{}' - {}".format(name, status)
				context = {'form': form, 'error': error} 
				return render(request, 'addhost/add_host_commercial.html', context)
		else:
			error = 'Invalid input.'
			context = {'form': form, 'error': error}
			return render(request, 'addhost/add_host_commercial.html', context)

@login_required
def add_host_government(request):
	if request.method == 'GET':

		# If user hasn't gotten their tokens yet, force them to login:
		if request.session.get('com_sid') == None:
			return redirect('gensids')

		form = AddHostFormGovernment()
		context = {'form': form}
		return render(request, 'addhost/add_host_government.html', context)

	elif request.method == 'POST':
		form = AddHostFormGovernment(request.POST)
		if form.is_valid():
			# gov_sid = form.cleaned_data.get('gov_sid')
			gov_sid = request.session.get('gov_sid')
			name = form.cleaned_data.get('name')
			ip_address = form.cleaned_data.get('ip_address')
			comment = form.cleaned_data.get('comment')
			grp_name = form.cleaned_data.get('grp_name')
			if not comment:
				if grp_name:
					status = web_base.add_host(gov_sid, name, ip_address, add_to_grp=True, grp_name=grp_name)
				else:
					status = web_base.add_host(gov_sid, name, ip_address)
			elif comment:
				if grp_name:
					status = web_base.add_host(gov_sid, name, ip_address, comments=comment, add_to_grp=True, grp_name=grp_name)
				else:
					status = web_base.add_host(gov_sid, name, ip_address, comments=comment)
			if status == 200:
				web_base.publish_changes(gov_sid)
				success = "Host '{}' added successfully!".format(name)
				context = {'form': form, 'success': success}
				return render(request, 'addhost/add_host_government.html', context)
			else:
				error = "Failed to add host '{}' - {}".format(name, status)
				context = {'form': form, 'error': error} 
				return render(request, 'addhost/add_host_government.html', context)
		else:
			error = 'Invalid input.'
			context = {'form': form, 'error': error}
			return render(request, 'addhost/add_host_government.html', context) 

@login_required
def add_host_all(request):
	if request.method == 'GET':

		# If user hasn't gotten their tokens yet, force them to login:
		if request.session.get('com_sid') == None:
			return redirect('gensids')

		form = AddHostFormAll()
		context = {'form': form}
		return render(request, 'addhost/add_host_all.html', context)

	elif request.method == 'POST':
		form = AddHostFormAll(request.POST)
		if form.is_valid():
			com_sid = request.session.get('com_sid')
			gov_sid = request.session.get('gov_sid')
			name = form.cleaned_data.get('name')
			ip_address = form.cleaned_data.get('ip_address')
			comment = form.cleaned_data.get('comment')
			grp_name = form.cleaned_data.get('grp_name')
			if not comment:
				if grp_name:
					com_status = web_base.add_host(com_sid, name, ip_address, add_to_grp=True, grp_name=grp_name)
					gov_status = web_base.add_host(gov_sid, name, ip_address, add_to_grp=True, grp_name=grp_name)
				else:
					com_status = web_base.add_host(com_sid, name, ip_address)
					gov_status = web_base.add_host(gov_sid, name, ip_address)
			elif comment:
				if grp_name:
					com_status = web_base.add_host(com_sid, name, ip_address, comments=comment, add_to_grp=True, grp_name=grp_name)
					gov_status = web_base.add_host(gov_sid, name, ip_address, comments=comment, add_to_grp=True, grp_name=grp_name)
				else:
					com_status = web_base.add_host(com_sid, name, ip_address, comments=comment)
					gov_status = web_base.add_host(gov_sid, name, ip_address, comments=comment)
			
			# All domain success:
			if com_status == 200 and gov_status == 200:
				web_base.publish_changes(com_sid)
				web_base.publish_changes(gov_sid)
				success = "Host '{}' added successfully! to domains:".format(name)
				domains = 'Commercial, Government'
				context = {'form': form, 'success': success, 'domains': domains}
				return render(request, 'addhost/add_host_all.html', context)

			# Some domain success:
			context = {}
			if com_status == 200:
				web_base.publish_changes(com_sid)
				com_success = "Host '{}' added successfully to Commercial Domain".format(name)
				context['com_success'] = com_success
			elif com_status != 200:
				com_error = "Host '{}' not added to Commercial Domain - ".format(name) + com_status
				context['com_error'] = com_error
				web_base.discard_changes(com_sid)

			if gov_status == 200:
				web_base.publish_changes(gov_sid)
				gov_success = "Host '{}' added successfully to Government Domain".format(name)
				context['gov_success'] = gov_success
			elif gov_status != 200:
				gov_error = "Host '{}' not added to Government Domain - ".format(name) + gov_status
				context['gov_error'] = gov_error
				web_base.discard_changes(gov_sid)

			context['form'] = form
			return render(request, 'addhost/add_host_all.html', context)
		else:
			error = 'Input invalid.'
			context = {'form': form, 'error': error}
			return render(request, 'addhost/add_host_all.html', context)

#########################
### Add Network Views  ##
#########################
@login_required
def add_network_commercial(request):
	if request.method == 'GET':

		# If user hasn't gotten their tokens yet, force them to login:
		if request.session.get('com_sid') == None:
			return redirect('gensids')

		form = AddNetworkFormCommercial()
		context = {'form': form}
		return render(request, 'addnetwork/add_network_commercial.html', context)
	
	elif request.method == 'POST':
		form = AddNetworkFormCommercial(request.POST)
		if form.is_valid():
			# com_sid = form.cleaned_data.get('com_sid')
			com_sid = request.session.get('com_sid')
			name = form.cleaned_data.get('name')
			subnet = form.cleaned_data.get('subnet')
			subnet_mask = form.cleaned_data.get('subnet_mask')
			comment = form.cleaned_data.get('comment')
			grp_name = form.cleaned_data.get('grp_name')
			if not comment:
				if grp_name:
					status = web_base.add_network(com_sid, name, subnet, subnet_mask, add_to_grp=True, grp_name=grp_name)
				else:
					status = web_base.add_network(com_sid, name, subnet, subnet_mask)
			elif comment:
				if grp_name:
					status = web_base.add_network(com_sid, name, subnet, subnet_mask, comments=comment, add_to_grp=True, grp_name=grp_name)
				else:
					status = web_base.add_network(com_sid, name, subnet, subnet_mask, comments=comment)
			if status == 200:
				web_base.publish_changes(com_sid)
				success = 'Network {} added successfully!'.format(name)
				context = {'form': form, 'success': success}
				return render(request, 'addnetwork/add_network_commercial.html', context)
			else:
				web_base.discard_changes(com_sid)
				error = "Failed to add network '{}'.".format(name)
				context = {'form': form, 'error': error}
				return render(request, 'addnetwork/add_network_commercial.html', context)
		else:
			error = 'Input invalid.'
			context = {'form': form, 'error': error}
			return render(request, 'addnetwork/add_network_commercial.html', context)

@login_required
def add_network_government(request):
	if request.method == 'GET':

		# If user hasn't gotten their tokens yet, force them to login:
		if request.session.get('com_sid') == None:
			return redirect('gensids')

		form = AddNetworkFormGovernment()
		context = {'form': form}
		return render(request, 'addnetwork/add_network_government.html', context)
	
	elif request.method == 'POST':
		form = AddNetworkFormGovernment(request.POST)
		if form.is_valid():
			gov_sid = request.session.get('gov_sid')
			name = form.cleaned_data.get('name')
			subnet = form.cleaned_data.get('subnet')
			subnet_mask = form.cleaned_data.get('subnet_mask')
			comment = form.cleaned_data.get('comment')
			grp_name = form.cleaned_data.get('grp_name')
			if not comment:
				if grp_name:
					status = web_base.add_network(gov_sid, name, subnet, subnet_mask, add_to_grp=True, grp_name=grp_name)
				else:
					status = web_base.add_network(gov_sid, name, subnet, subnet_mask)
			elif comment:
				if grp_name:
					status = web_base.add_network(gov_sid, name, subnet, subnet_mask, comments=comment, add_to_grp=True, grp_name=grp_name)
				else:
					status = web_base.add_network(gov_sid, name, subnet, subnet_mask, comments=comment)
			if status == 200:
				web_base.publish_changes(gov_sid)
				success = 'Network {} added successfully!'.format(name)
				context = {'form': form, 'success': success}
				return render(request, 'addnetwork/add_network_government.html', context)
			else:
				web_base.discard_changes(gov_sid)
				error = "Failed to add network '{}'.".format(name)
				context = {'form': form, 'error': error}
				return render(request, 'addnetwork/add_network_government.html', context)
		else:
			error = 'Input invalid.'
			context = {'form': form, 'error': error}
			return render(request, 'addnetwork/add_network_government.html', context)	

@login_required
def add_network_all(request):
	if request.method == 'GET':

		# If user hasn't gotten their tokens yet, force them to login:
		if request.session.get('com_sid') == None:
			return redirect('gensids')

		form = AddNetworkFormAll()
		context = {'form': form}
		return render(request, 'addnetwork/add_network_all.html', context)
	
	elif request.method == 'POST':
		form = AddNetworkFormAll(request.POST)
		if form.is_valid():
			com_sid = request.session.get('com_sid')
			gov_sid = request.session.get('gov_sid')
			name = form.cleaned_data.get('name')
			subnet = form.cleaned_data.get('subnet')
			subnet_mask = form.cleaned_data.get('subnet_mask')
			comment = form.cleaned_data.get('comment')
			grp_name = form.cleaned_data.get('grp_name')
			if not comment:
				if grp_name:
					com_status = web_base.add_network(com_sid, name, subnet, subnet_mask, add_to_grp=True, grp_name=grp_name)
					gov_status = web_base.add_network(gov_sid, name, subnet, subnet_mask, add_to_grp=True, grp_name=grp_name)
				else:
					com_status = web_base.add_network(com_sid, name, subnet, subnet_mask)
					gov_status = web_base.add_network(gov_sid, name, subnet, subnet_mask)
			elif comment:
				if grp_name:
					com_status = web_base.add_network(com_sid, name, subnet, subnet_mask, comments=comment, add_to_grp=True, grp_name=grp_name)
					gov_status = web_base.add_network(gov_sid, name, subnet, subnet_mask, comments=comment, add_to_grp=True, grp_name=grp_name)
				else:
					com_status = web_base.add_network(com_sid, name, subnet, subnet_mask, comments=comment)
					gov_status = web_base.add_network(gov_sid, name, subnet, subnet_mask, comments=comment)
		
			# All domain success:
			if com_status == 200 and gov_status == 200:
				web_base.publish_changes(com_sid)
				web_base.publish_changes(gov_sid)
				success = "Network '{}' added successfully! to domains:".format(name)
				domains = 'Commercial, Government'
				context = {'form': form, 'success': success, 'domains': domains}
				return render(request, 'addnetwork/add_network_all.html', context)

			# Some domain success:
			context = {}
			if com_status == 200:
				web_base.publish_changes(com_sid)
				com_success = "Network '{}' added successfully to Commercial Domain".format(name)
				context['com_success'] = com_success
			elif com_status != 200:
				com_error = "Network '{}' not added to Commercial Domain - ".format(name) + com_status
				context['com_error'] = com_error
				web_base.discard_changes(com_sid)

			if gov_status == 200:
				web_base.publish_changes(gov_sid)
				gov_success = "Network '{}' added successfully to Government Domain".format(name)
				context['gov_success'] = gov_success
			elif gov_status != 200:
				gov_error = "Network '{}' not added to Government Domain - ".format(name) + gov_status
				context['gov_error'] = gov_error
				web_base.discard_changes(gov_sid)

			context['form'] = form
			return render(request, 'addnetwork/add_network_all.html', context)

		else:
			error = 'Input invalid.'
			context = {'form': form, 'error': error}
			return render(request, 'addnetwork/add_network_all.html', context)	

#########################
### Add Network Group  ##
#########################
@login_required
def add_network_grp_commercial(request):
	if request.method == 'GET':

		# If user hasn't gotten their tokens yet, force them to login:
		if request.session.get('com_sid') == None:
			return redirect('gensids')

		form = AddNetworkGroupFormCommercial()
		context = {'form': form}
		return render(request, 'addnetworkgroup/add_network_group_commercial.html', context)

	elif request.method == 'POST':
		form = AddNetworkGroupFormCommercial(request.POST)
		if form.is_valid():
			# com_sid = form.cleaned_data.get('com_sid')
			com_sid = request.session.get('com_sid')
			name = form.cleaned_data.get('name')
			status = web_base.add_network_obj_grp(com_sid, name)
			if status == 200:
				web_base.publish_changes(com_sid)
				success = 'Network Group {} added successfully!'.format(name)
				context = {'form': form, 'success': success}
				return render(request, 'addnetworkgroup/add_network_group_commercial.html', context)
			else:
				web_base.discard_changes(com_sid)
				error = "Failed to add network group '{}'.".format(name)
				context = {'form': form, 'error': error}
				return render(request, 'addnetworkgroup/add_network_group_commercial.html', context)
		else:
			error = 'Input invalid.' 
			context = {'form': form, 'error': error}
			return render(request, 'addnetworkgroup/add_network_group_commercial.html', context)
@login_required
def add_network_grp_government(request):
	if request.method == 'GET':

		# If user hasn't gotten their tokens yet, force them to login:
		if request.session.get('com_sid') == None:
			return redirect('gensids')

		form = AddNetworkGroupFormGovernment()
		context = {'form': form}
		return render(request, 'addnetworkgroup/add_network_group_government.html', context)

	elif request.method == 'POST':
		form = AddNetworkGroupFormGovernment(request.POST)
		if form.is_valid():
			gov_sid = request.session.get('gov_sid')
			name = form.cleaned_data.get('name')
			status = web_base.add_network_obj_grp(gov_sid, name)
			if status == 200:
				web_base.publish_changes(gov_sid)
				success = 'Network Group {} added successfully!'.format(name)
				context = {'form': form, 'success': success}
				return render(request, 'addnetworkgroup/add_network_group_government.html', context)
			else:
				web_base.discard_changes(gov_sid)
				error = "Failed to add network group '{}'.".format(name)
				context = {'form': form, 'error': error}
				return render(request, 'addnetworkgroup/add_network_group_government.html', context)
		else:
			error = 'Input invalid.' 
			context = {'form': form, 'error': error}
			return render(request, 'addnetworkgroup/add_network_group_government.html', context)
@login_required
def add_network_grp_all(request):
	if request.method == 'GET':

		# If user hasn't gotten their tokens yet, force them to login:
		if request.session.get('com_sid') == None:
			return redirect('gensids')

		form = AddNetworkGroupFormAll()
		context = {'form': form}
		return render(request, 'addnetworkgroup/add_network_group_all.html', context)

	elif request.method == 'POST':
		form = AddNetworkGroupFormAll(request.POST)
		if form.is_valid():
			com_sid = request.session.get('com_sid')
			gov_sid = request.session.get('gov_sid')
			name = form.cleaned_data.get('name')
			com_status = web_base.add_network_obj_grp(com_sid, name)
			gov_status = web_base.add_network_obj_grp(gov_sid, name)
		
			# All domain success:
			if com_status == 200 and gov_status == 200:
				web_base.publish_changes(com_sid)
				web_base.publish_changes(gov_sid)
				success = "Network '{}' added successfully! to domains:".format(name)
				domains = 'Commercial, Government'
				context = {'form': form, 'success': success, 'domains': domains}
				return render(request, 'addnetworkgroup/add_network_group_all.html', context)

			# Some domain success:
			context = {}
			if com_status == 200:
				web_base.publish_changes(com_sid)
				com_success = "Network '{}' added successfully to Commercial Domain".format(name)
				context['com_success'] = com_success
			elif com_status != 200:
				print(com_status)
				com_error = "Network '{}' not added to Commercial Domain - ".format(name) + com_status
				print(com_error)
				context['com_error'] = com_error
				web_base.discard_changes(com_sid)

			if gov_status == 200:
				web_base.publish_changes(gov_sid)
				gov_success = "Network '{}' added successfully to Government Domain".format(name)
				context['gov_success'] = gov_success
			elif gov_status != 200:
				gov_error = "Network '{}' not added to Government Domain - ".format(name) + gov_status
				context['gov_error'] = gov_error
				web_base.discard_changes(gov_sid)

			context['form'] = form
			return render(request, 'addnetworkgroup/add_network_group_all.html', context)

		else:
			error = 'Input invalid.' 
			context = {'form': form, 'error': error}
			return render(request, 'addnetworkgroup/add_network_group_all.html', context)

#######################################
### Replicate Existing Object-Group  ##
#######################################
@login_required
def copy_network_grp_commercial(request):
	if request.method == 'GET':

		# If user hasn't gotten their tokens yet, force them to login:
		if request.session.get('com_sid') == None:
			return redirect('gensids')

		form = CopyNetworkGroupCommercial()
		context = {'form': form}
		return render(request, 'copynetworkgroup/commercial_copynetworkgrp.html', context)

	elif request.method == 'POST':
		form = CopyNetworkGroupCommercial(request.POST)
		if form.is_valid():
			com_sid = request.session.get('com_sid')
			gov_sid = request.session.get('gov_sid')

			domain = form.cleaned_data.get('domain')
			grp_name = form.cleaned_data.get('grp_name')

			# Get source domain to copy from and set as source_sid:
			if domain == 'government':
				source_sid = gov_sid

			members = web_base.show_grp_obj(source_sid, grp_name)
			if members:
				
				# Objects that had issues and will require manual add
				issues = []

				# Create group:
				added_grp_status = web_base.add_network_obj_grp(com_sid, grp_name)

				# If object group already exists:
				if 'exists' in added_grp_status:

					# Loop through each member of the provided object group and create member if it does NOT exist and add to copied group:
					for i in members:

						# @@ Host Object @@
						if len(i) == 3:
							name, ip_address, comments = i[0], i[1], i[2]
							
							# Check to see if host object already exist:
							host_exist = web_base.show_host(com_sid, name)
							
							# Host object does not exist so create host object:
							if host_exist == None:
								status_code = web_base.add_host(com_sid, name, ip_address, comments=comments, add_to_grp=True, grp_name=grp_name)
								if status_code == 200:
									web_base.publish_changes(com_sid)
									continue
								else:
									issues.append(name)
									web_base.discard_changes(com_sid)
							
							# Host already exists - add to the group:
							else:
								status_code = web_base.edit_host(com_sid, name, add_group=True, grp_name=grp_name)
								if status_code == 200:
									web_base.publish_changes(com_sid)
								else:
									issues.append(name)
									web_base.discard_changes(com_sid)

						# @@ Network Object @@
						elif len(i) == 4:
							name, subnet, subnet_mask, comments = i[0], i[1], i[2], i[3]

							# Check to see if network object already exist:
							network_exist = web_base.show_network(com_sid, name)

							# Network object does not exist so create network object:
							if network_exist == None:
								status_code = web_base.add_network(com_sid, name, subnet, subnet_mask, comments=comments, add_to_grp=True, grp_name=grp_name)
								if status_code == 200:
									web_base.publish_changes(com_sid)
									continue
								else:
									issues.append(name)
									web_base.discard_changes(com_sid)

							# Network object already exists - add to the group:
							else:
								status_code = web_base.edit_network(com_sid, name, add_group=True, grp_name=grp_name)
								if status_code == 200:
									web_base.publish_changes(com_sid)
								else:
									issues.append(name)
									web_base.discard_changes(com_sid)
					
					# One final saving of changes:
					web_base.publish_changes(com_sid)

					# If there were any objects with issues:
					if issues:
						success = 'Network Group {} copied, but the following objects had issues and will require a manual add: {}'.format(grp_name, issues)
					# No issues:
					else:
						success = 'Network Group {} copied successfully!'.format(grp_name)
					
					context = {'form': form, 'success': success}
					return render(request, 'copynetworkgroup/commercial_copynetworkgrp.html', context)

				# If object group creation successful:
				elif added_grp_status == 'success':

					# Loop through each member of the provided object group and create member if it does NOT exist and add to copied group:
					for i in members:

						# @@ Host Object @@
						if len(i) == 3:
							name, ip_address, comments = i[0], i[1], i[2]
							
							# Check to see if host object already exist:
							host_exist = web_base.show_host(com_sid, name)
							
							# Host object does not exist so create host object:
							if host_exist == None:
								status_code = web_base.add_host(com_sid, name, ip_address, comments=comments, add_to_grp=True, grp_name=grp_name)
								if status_code == 200:
									web_base.publish_changes(com_sid)
									continue
								else:
									issues.append(name)
									web_base.discard_changes(com_sid)
							
							# Host already exists - add to the group:
							else:
								status_code = web_base.edit_host(com_sid, name, add_group=True, grp_name=grp_name)
								if status_code == 200:
									web_base.publish_changes(com_sid)
								else:
									issues.append(name)
									web_base.discard_changes(com_sid)

						# @@ Network Object @@
						elif len(i) == 4:
							name, subnet, subnet_mask, comments = i[0], i[1], i[2], i[3]

							# Check to see if network object already exist:
							network_exist = web_base.show_network(com_sid, name)

							# Network object does not exist so create network object:
							if network_exist == None:
								status_code = web_base.add_network(com_sid, name, subnet, subnet_mask, comments=comments, add_to_grp=True, grp_name=grp_name)
								if status_code == 200:
									web_base.publish_changes(com_sid)
									continue
								else:
									issues.append(name)
									web_base.discard_changes(com_sid)

							# Network object already exists - add to the group:
							else:
								status_code = web_base.edit_network(com_sid, name, add_group=True, grp_name=grp_name)
								if status_code == 200:
									web_base.publish_changes(com_sid)
								else:
									issues.append(name)
									web_base.discard_changes(com_sid)

					# One final saving of changes:
					web_base.publish_changes(com_sid)

					# If there were any objects with issues:
					if issues:
						success = 'Network Group {} copied, but the following objects had issues and will require a manual add: {}'.format(grp_name, issues)
					# No issues:
					else:
						success = 'Network Group {} copied successfully!'.format(grp_name)
					
					context = {'form': form, 'success': success}
					return render(request, 'copynetworkgroup/commercial_copynetworkgrp.html', context)



				# Object group does NOT currently exist AND unable to create object group:
				else:
					web_base.discard_changes(com_sid)
					error = 'Failed to create Network Group on destination domain - {}'.format(added_grp_status) 
					context = {'form': form, 'error': error}
					return render(request, 'copynetworkgroup/commercial_copynetworkgrp.html', context)
			
			# Provided object group does NOT have any memebers:
			else:
				error = 'No members in Network Object-Group {} or group does not exist on source domain.'.format(grp_name) 
				context = {'form': form, 'error': error}
				return render(request, 'copynetworkgroup/commercial_copynetworkgrp.html', context)
		
		# User form input is invalid:
		else:
			error = 'Input invalid.' 
			context = {'form': form, 'error': error}
			return render(request, 'copynetworkgroup/commercial_copynetworkgrp.html', context)

@login_required
def copy_network_grp_government(request):
	if request.method == 'GET':

		# If user hasn't gotten their tokens yet, force them to login:
		if request.session.get('com_sid') == None:
			return redirect('gensids')

		form = CopyNetworkGroupGovernment()
		context = {'form': form}
		return render(request, 'copynetworkgroup/government_copynetworkgrp.html', context)

	elif request.method == 'POST':
		form = CopyNetworkGroupGovernment(request.POST)
		if form.is_valid():
			com_sid = request.session.get('com_sid')
			gov_sid = request.session.get('gov_sid')

			domain = form.cleaned_data.get('domain')
			grp_name = form.cleaned_data.get('grp_name')

			# Get source domain to copy from and set as source_sid:
			if domain == 'commercial':
				source_sid = com_sid

			members = web_base.show_grp_obj(source_sid, grp_name)
			if members:
				
				# Objects that had issues and will require manual add
				issues = []

				# Create group:
				added_grp_status = web_base.add_network_obj_grp(gov_sid, grp_name)

				# If object group already exists:
				if 'exists' in added_grp_status:

					# Loop through each member of the provided object group and create member if it does NOT exist and add to copied group:
					for i in members:

						# @@ Host Object @@
						if len(i) == 3:
							name, ip_address, comments = i[0], i[1], i[2]
							
							# Check to see if host object already exist:
							host_exist = web_base.show_host(gov_sid, name)
							
							# Host object does not exist so create host object:
							if host_exist == None:
								status_code = web_base.add_host(gov_sid, name, ip_address, comments=comments, add_to_grp=True, grp_name=grp_name)
								if status_code == 200:
									web_base.publish_changes(gov_sid)
									continue
								else:
									issues.append(name)
									web_base.discard_changes(gov_sid)
							
							# Host already exists - add to the group:
							else:
								status_code = web_base.edit_host(gov_sid, name, add_group=True, grp_name=grp_name)
								if status_code == 200:
									web_base.publish_changes(gov_sid)
								else:
									issues.append(name)
									web_base.discard_changes(gov_sid)

						# @@ Network Object @@
						elif len(i) == 4:
							name, subnet, subnet_mask, comments = i[0], i[1], i[2], i[3]

							# Check to see if network object already exist:
							network_exist = web_base.show_network(gov_sid, name)

							# Network object does not exist so create network object:
							if network_exist == None:
								status_code = web_base.add_network(gov_sid, name, subnet, subnet_mask, comments=comments, add_to_grp=True, grp_name=grp_name)
								if status_code == 200:
									web_base.publish_changes(gov_sid)
									continue
								else:
									issues.append(name)
									web_base.discard_changes(gov_sid)

							# Network object already exists - add to the group:
							else:
								status_code = web_base.edit_network(gov_sid, name, add_group=True, grp_name=grp_name)
								if status_code == 200:
									web_base.publish_changes(gov_sid)
								else:
									issues.append(name)
									web_base.discard_changes(gov_sid)
					
					# One final saving of changes:
					web_base.publish_changes(gov_sid)

					# If there were any objects with issues:
					if issues:
						success = 'Network Group {} copied, but the following objects had issues and will require a manual add: {}'.format(grp_name, issues)
					# No issues:
					else:
						success = 'Network Group {} copied successfully!'.format(grp_name)
					
					context = {'form': form, 'success': success}
					return render(request, 'copynetworkgroup/government_copynetworkgrp.html', context)

				# If object group creation successful:
				elif added_grp_status == 'success':
					
					# Loop through each member of the provided object group and create member if it does NOT exist and add to copied group:
					for i in members:

						# @@ Host Object @@
						if len(i) == 3:
							name, ip_address, comments = i[0], i[1], i[2]
							
							# Check to see if host object already exist:
							host_exist = web_base.show_host(gov_sid, name)
							
							# Host object does not exist so create host object:
							if host_exist == None:
								status_code = web_base.add_host(gov_sid, name, ip_address, comments=comments, add_to_grp=True, grp_name=grp_name)
								if status_code == 200:
									web_base.publish_changes(gov_sid)
									continue
								else:
									issues.append(name)
									web_base.discard_changes(gov_sid)
							
							# Host already exists - add to the group:
							else:
								status_code = web_base.edit_host(gov_sid, name, add_group=True, grp_name=grp_name)
								if status_code == 200:
									web_base.publish_changes(gov_sid)
								else:
									issues.append(name)
									web_base.discard_changes(gov_sid)

						# @@ Network Object @@
						elif len(i) == 4:
							name, subnet, subnet_mask, comments = i[0], i[1], i[2], i[3]

							# Check to see if network object already exist:
							network_exist = web_base.show_network(gov_sid, name)

							# Network object does not exist so create network object:
							if network_exist == None:
								status_code = web_base.add_network(gov_sid, name, subnet, subnet_mask, comments=comments, add_to_grp=True, grp_name=grp_name)
								if status_code == 200:
									web_base.publish_changes(gov_sid)
									continue
								else:
									issues.append(name)
									web_base.discard_changes(gov_sid)

							# Network object already exists - add to the group:
							else:
								status_code = web_base.edit_network(gov_sid, name, add_group=True, grp_name=grp_name)
								if status_code == 200:
									web_base.publish_changes(gov_sid)
								else:
									issues.append(name)
									web_base.discard_changes(gov_sid)

					# One final saving of changes:
					web_base.publish_changes(gov_sid)

					# If there were any objects with issues:
					if issues:
						success = 'Network Group {} copied, but the following objects had issues and will require a manual add: {}'.format(grp_name, issues)
					# No issues:
					else:
						success = 'Network Group {} copied successfully!'.format(grp_name)
					
					context = {'form': form, 'success': success}
					return render(request, 'copynetworkgroup/government_copynetworkgrp.html', context)



				# Object group does NOT currently exist AND unable to create object group:
				else:
					web_base.discard_changes(gov_sid)
					error = 'Failed to create Network Group on destination domain - {}'.format(added_grp_status) 
					context = {'form': form, 'error': error}
					return render(request, 'copynetworkgroup/government_copynetworkgrp.html', context)
			
			# Provided object group does NOT have any memebers:
			else:
				error = 'No members in Network Object-Group {} or group does not exist on source domain.'.format(grp_name) 
				context = {'form': form, 'error': error}
				return render(request, 'copynetworkgroup/government_copynetworkgrp.html', context)
		
		# User form input is invalid:
		else:
			error = 'Input invalid.' 
			context = {'form': form, 'error': error}
			return render(request, 'copynetworkgroup/government_copynetworkgrp.html', context)


###############################
### Add Service Ports Views  ##
###############################
@login_required
def add_service_commercial(request):
	if request.method == 'GET':

		# If user hasn't gotten their tokens yet, force them to login:
		if request.session.get('com_sid') == None:
			return redirect('gensids')

		form = AddService()
		context = {'form': form}
		return render(request, 'addservice/add_service_commercial.html', context)

	elif request.method == 'POST':
		form = AddService(request.POST)
		if form.is_valid():
			name = form.cleaned_data.get('name')
			service_type = form.cleaned_data.get('service_type')
			port = form.cleaned_data.get('port')
			comment = form.cleaned_data.get('comment')

			com_sid = request.session.get('com_sid')

			if service_type == 'tcp':
				if not comment:
					status = web_base.add_service_tcp(com_sid, name, port)
				else:
					status = web_base.add_service_tcp(com_sid, name, port, comment=comment)

				if status == 200:
					web_base.publish_changes(com_sid)
					success = "TCP Service '{}' added successfully!".format(name)
					context = {'form': form, 'success': success}
					return render(request, 'addservice/add_service_commercial.html', context)
				else:
					web_base.discard_changes(com_sid)
					error = "Failed to add TCP service '{}' - {}".format(name, status)
					context = {'form': form, 'error': error} 
					return render(request, 'addservice/add_service_commercial.html', context)
			
			elif service_type == 'udp':
				if not comment:
					status = web_base.add_service_udp(com_sid, name, port)
				else:
					status = web_base.add_service_udp(com_sid, name, port, comment=comment)

				if status == 200:
					web_base.publish_changes(com_sid)
					success = "UDP Service '{}' added successfully!".format(name)
					context = {'form': form, 'success': success}
					return render(request, 'addservice/add_service_commercial.html', context)
				else:
					web_base.discard_changes(com_sid)
					error = "Failed to add UDP service '{}' - {}".format(name, status)
					context = {'form': form, 'error': error} 
					return render(request, 'addservice/add_service_commercial.html', context)
		# If Form is not valid:
		else:
			form = AddService(request.POST)
			error = 'Invalid input.'
			context = {'form': form, 'error': error}
			return render(request, 'addservice/add_service_commercial.html', context)

@login_required
def add_service_government(request):
	if request.method == 'GET':

		# If user hasn't gotten their tokens yet, force them to login:
		if request.session.get('gov_sid') == None:
			return redirect('gensids')

		form = AddService()
		context = {'form': form}
		return render(request, 'addservice/add_service_government.html', context)

	elif request.method == 'POST':
		form = AddService(request.POST)
		if form.is_valid():
			name = form.cleaned_data.get('name')
			service_type = form.cleaned_data.get('service_type')
			port = form.cleaned_data.get('port')
			comment = form.cleaned_data.get('comment')

			gov_sid = request.session.get('gov_sid')

			if service_type == 'tcp':
				if not comment:
					status = web_base.add_service_tcp(gov_sid, name, port)
				else:
					status = web_base.add_service_tcp(gov_sid, name, port, comment=comment)

				if status == 200:
					web_base.publish_changes(gov_sid)
					success = "TCP Service '{}' added successfully!".format(name)
					context = {'form': form, 'success': success}
					return render(request, 'addservice/add_service_government.html', context)
				else:
					web_base.discard_changes(gov_sid)
					error = "Failed to add TCP service '{}' - {}".format(name, status)
					context = {'form': form, 'error': error} 
					return render(request, 'addservice/add_service_government.html', context)
			
			elif service_type == 'udp':
				if not comment:
					status = web_base.add_service_udp(gov_sid, name, port)
				else:
					status = web_base.add_service_udp(gov_sid, name, port, comment=comment)

				if status == 200:
					web_base.publish_changes(gov_sid)
					success = "UDP Service '{}' added successfully!".format(name)
					context = {'form': form, 'success': success}
					return render(request, 'addservice/add_service_government.html', context)
				else:
					web_base.discard_changes(gov_sid)
					error = "Failed to add UDP service '{}' - {}".format(name, status)
					context = {'form': form, 'error': error} 
					return render(request, 'addservice/add_service_government.html', context)
		# If Form is not valid:
		else:
			form = AddService(request.POST)
			error = 'Invalid input.'
			context = {'form': form, 'error': error}
			return render(request, 'addservice/add_service_commercial.html', context)

@login_required
def add_service_all(request):
	if request.method == 'GET':

		# If user hasn't gotten their tokens yet, force them to login:
		if request.session.get('com_sid') == None:
			return redirect('gensids')

		form = AddService()
		context = {'form': form}
		return render(request, 'addservice/add_service_all.html', context)

	elif request.method == 'POST':
		form = AddService(request.POST)
		if form.is_valid():
			name = form.cleaned_data.get('name')
			service_type = form.cleaned_data.get('service_type')
			port = form.cleaned_data.get('port')
			comment = form.cleaned_data.get('comment')

			com_sid = request.session.get('com_sid')
			gov_sid = request.session.get('gov_sid')

			if service_type == 'tcp':
				if not comment:
					com_status = web_base.add_service_tcp(com_sid, name, port)
					gov_status = web_base.add_service_tcp(gov_sid, name, port)

				else:
					com_status = web_base.add_service_tcp(com_sid, name, port, comment=comment)
					gov_status = web_base.add_service_tcp(gov_sid, name, port, comment=comment)

				if com_status == 200 and gov_status == 200:
					web_base.publish_changes(com_sid)
					web_base.publish_changes(gov_sid)
					success = "TCP Service '{}' added successfully!".format(name)
					context = {'form': form, 'success': success}
					return render(request, 'addservice/add_service_all.html', context)
				elif com_status == 200 and gov_status != 200:
					web_base.publish_changes(com_sid)
					web_base.discard_changes(gov_sid)
					com_success = "Commercial TCP Service '{}' added successfully!".format(name)
					gov_error = "Failed to add Government TCP service '{}' - {}".format(name, gov_status)
					context = {'form': form, 'gov_error': gov_error, 'com_success': com_success} 
					return render(request, 'addservice/add_service_all.html', context)
				elif gov_status == 200 and com_status != 200:
					web_base.publish_changes(gov_sid)
					web_base.discard_changes(com_sid)
					gov_success = "Government TCP Service '{}' added successfully!".format(name)
					com_error = "Failed to add Commercial TCP service '{}' - {}".format(name, com_status)
					context = {'form': form, 'com_error': com_error, 'gov_success': gov_success} 
					return render(request, 'addservice/add_service_all.html', context)
				else:
					com_error = "Failed to add Commercial TCP service '{}' - {}".format(name, com_status)
					gov_error = "Failed to add Government TCP service '{}' - {}".format(name, gov_status)
					context = {'form': form, 'com_error': com_error, 'gov_error': gov_error} 
					return render(request, 'addservice/add_service_all.html', context)
			
			elif service_type == 'udp':
				if not comment:
					com_status = web_base.add_service_udp(com_sid, name, port)
					gov_status = web_base.add_service_udp(gov_sid, name, port)

				else:
					com_status = web_base.add_service_udp(com_sid, name, port, comment=comment)
					gov_status = web_base.add_service_udp(gov_sid, name, port, comment=comment)

				if com_status == 200 and gov_status == 200:
					web_base.publish_changes(com_sid)
					web_base.publish_changes(gov_sid)
					success = "UDP Service '{}' added successfully!".format(name)
					context = {'form': form, 'success': success}
					return render(request, 'addservice/add_service_all.html', context)
				elif com_status == 200 and gov_status != 200:
					web_base.publish_changes(com_sid)
					web_base.discard_changes(gov_sid)
					com_success = "Commercial UDP Service '{}' added successfully!".format(name)
					gov_error = "Failed to add Government UDP service '{}' - {}".format(name, gov_status)
					context = {'form': form, 'gov_error': gov_error, 'com_success': com_success} 
					return render(request, 'addservice/add_service_all.html', context)
				elif gov_status == 200 and com_status != 200:
					web_base.publish_changes(gov_sid)
					web_base.discard_changes(com_sid)
					gov_success = "Government UDP Service '{}' added successfully!".format(name)
					com_error = "Failed to add Commercial UDP service '{}' - {}".format(name, com_status)
					context = {'form': form, 'com_error': com_error, 'gov_success': gov_success} 
					return render(request, 'addservice/add_service_all.html', context)
				else:
					com_error = "Failed to add Commercial UDP service '{}' - {}".format(name, com_status)
					gov_error = "Failed to add Government UDP service '{}' - {}".format(name, gov_status)
					context = {'form': form, 'com_error': com_error, 'gov_error': gov_error} 
					return render(request, 'addservice/add_service_all.html', context)
		# If Form is not valid:
		else:
			form = AddService(request.POST)
			error = 'Invalid input.'
			context = {'form': form, 'error': error}
			return render(request, 'addservice/add_service_all.html', context)
		