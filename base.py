#!/usr/bin/python
__author__ = 'Bobby Williams <bobby.williams@xxx.com>'

import requests, json, getpass
requests.packages.urllib3.disable_warnings() 

base_url = 'https://<mds_ip>/web_api/'

def login():
	while True:
		username = input('username: ')
		password = getpass.getpass('password: ')

		com_login_info = {'user': username, 'password': password, 'domain': 'Commercial'}
		gov_login_info = {'user': username, 'password': password, 'domain': 'Government'}

		request_headers = {'Content-Type' : 'application/json'}

		# Get Sid for Commercial Domain:
		response = requests.post(base_url+'login', data=json.dumps(com_login_info), headers=request_headers, verify=False)
		response = json.loads(response.text)
		
		try:
			if response['sid']:
				com_sid = response['sid']
				com_session_uid = response['uid']
		except:
			print('Invalid username and/or password, try again..')
		else:
			# Get Sid for Govnernment Domain:
			response = requests.post(base_url+'login', data=json.dumps(gov_login_info), headers=request_headers, verify=False)
			response = json.loads(response.text)
			gov_sid = response['sid']
			gov_session_uid = response['uid']
			return com_sid, gov_sid, com_session_uid, gov_session_uid

def publish_changes(sid):
	# Publish changes:
	request_headers = {'Content-Type': 'application/json', 'X-chkp-sid': sid}
	# data = {'uid': domain_session_uid}
	data = {}
	response = requests.post(base_url+'publish', data=json.dumps(data), headers=request_headers, verify=False)
	if response.status_code == 200:
		response = json.loads(response.text)
		return response['task-id']


def discard_changes(sid, uid=None):
	# Discard changes:
	request_headers = {'Content-Type': 'application/json', 'X-chkp-sid': sid}
	if uid:
		data = {'uid': uid}
	else:
		data = {'uid': sid}
	response = requests.post(base_url+'discard', data=json.dumps(data), headers=request_headers, verify=False)
	if response.status_code == 200:
		response = json.loads(response.text)
		print('{} - {}'.format(response['message'], response['number-of-discarded-changes']))

def show_sessions(sid, domain_session_uid):
	# Discard changes:
	request_headers = {'Content-Type': 'application/json', 'X-chkp-sid': sid}
	
	data = {'limit': 500}
		
	response = requests.post(base_url+'show-sessions', data=json.dumps(data), headers=request_headers, verify=False)
	if response.status_code == 200:
		response = json.loads(response.text)
		total = response['total']
		for i in response['objects']:
			domain = i['domain'].get('name')
			uid = i.get('uid')
			if uid == domain_session_uid:
				print('{} - {} | *Your current session'.format(uid, domain))
			else:
				print('{} - {}'.format(uid, domain))
		print('-' * 20)
		print('Total {} sessions: {}'.format(domain, total))
		print('=' * 20)

def show_packages(sid):
	# Displays the list of packages:
	request_headers = {'Content-Type': 'application/json', 'X-chkp-sid': sid}

	data = {'limit': 500}

	response = requests.post(base_url+'show-packages', data=json.dumps(data), headers=request_headers, verify=False)

	response = json.loads(response.text)

	if response['packages']:
		for package in response['packages']:
			print(package['name'])
		print('Total: {}'.format(response['total']))

def show_networks(sid, offset=0):
	# Displays the list of network objects:
	request_headers = {'Content-Type': 'application/json', 'X-chkp-sid': sid}

	data = {'limit': 500, 'offset': offset}

	response = requests.post(base_url+'show-networks', data=json.dumps(data), headers=request_headers, verify=False)

	response = json.loads(response.text)

	if response['objects']:
		for obj in response['objects']:
			print(obj['name'])
		print('Total: {}'.format(response['total']))

def show_host(sid, name):
	# Display details of a host object:
	request_headers = {'Content-Type': 'application/json', 'X-chkp-sid': sid}

	data = {'name': name}

	response = requests.post(base_url+'show-host', data=json.dumps(data), headers=request_headers, verify=False)
	
	response = json.loads(response.text)

	if not response.get('ipv4-address'): # Object name doesn't exist
		return None
	else:
		return response['ipv4-address'], response['comments']

def show_network(sid, name):
	# Display details of a network(subnet) object:
	request_headers = {'Content-Type': 'application/json', 'X-chkp-sid': sid}

	data = {'name': name}

	response = requests.post(base_url+'show-network', data=json.dumps(data), headers=request_headers, verify=False)

	response = json.loads(response.text)

	if not response.get('subnet4'): # Object name doesn't exist
		return None
	else:
		return response['subnet4'], response['mask-length4'], response['subnet-mask'], response['comments']

def show_grp_obj(sid, name):
	# Displays the details of an object group:
	request_headers = {'Content-Type': 'application/json', 'X-chkp-sid': sid}

	data = {'name': name}

	response = requests.post(base_url+'show-group', data=json.dumps(data), headers=request_headers, verify=False)
	response = json.loads(response.text)

	print('--------------')
	print('Group Members:')
	print('--------------')
	total_members = len(response['members'])
	members = []
	if response.get('members'):
		for i in response['members']:
			if i['type'] == 'host':
				member = []
				details = show_host(sid, i['name'])
				address = details[0]
				comments = details[1]
				print('{} - {}'.format(i['name'], i['type']))
				print('\t{}'.format(comments))
				member += [i['name'], address, comments]
				members.append(member)

			elif i['type'] == 'network':
				member = []
				details = show_network(sid, i['name'])
				subnet = details[0]
				mask_length = details[1]
				subnet_mask = details[2]
				comments = details[3]
				print('{} - {}'.format(i['name'], i['type']))
				print('\t{}/{} ({})'.format(subnet, mask_length, subnet_mask))
				print('\tComments: {}\n'.format(comments))
				member += [i['name'], subnet, subnet_mask, comments]
				members.append(member)
		print('Total members: {}'.format(total_members))
		print(response)
		return members
	else:
		return None		

		
def list_obj_grps(sid):
	# Displays a list of object groups
	request_headers = {'Content-Type': 'application/json', 'X-chkp-sid': sid}

	data = {'limit': 500}

	response = requests.post(base_url+'show-groups', data=json.dumps(data), headers=request_headers, verify=False)

	response = json.loads(response.text)

	for i in response['objects']:
		print(i['name'])

def edit_host(sid, name, add_group=False, remove_group=False, grp_name=None):
	# Edit existing host:
	request_headers = {'Content-Type': 'application/json', 'X-chkp-sid': sid}

	if add_group == True:
		data = {'name': name, 'groups': {'add': grp_name}}
	elif remove_group == True:
		data = {'name': name, 'groups': {'remove': grp_name}}

	response = requests.post(base_url+'set-host', data=json.dumps(data),headers=request_headers, verify=False)

	if response.status_code == 200:
		print('success')
		print(response.text)
	elif response.status_code == 400:
		print(response.text)
	else:
		print(response.text)

def add_host(sid, name, ip_address, comments='', add_to_grp=False, grp_name=None):
	# Add host object:
	request_headers = {'Content-Type': 'application/json', 'X-chkp-sid': sid}

	if add_to_grp == True:
		data = {'name': name, 'ip-address': ip_address, 'comments': comments, 'groups': [grp_name]}
	else:
		data = {'name': name, 'ip-address': ip_address, 'comments': comments}

	response = requests.post(base_url+'add-host', data=json.dumps(data), headers=request_headers, verify=False)
	
	if response.status_code == 200:
		status = response.status_code
		return status
	elif response.status_code == 400:
		# print(response.text)
		response_data = json.loads(response.text)
		if response_data.get('warnings'): # If duplicate object error, return warning message
			print(response_data['warnings'][0]['message'])
		elif response_data.get('errors'):
			print(response_data['errors'][0]['message'])
		elif response_data.get('message'):
			print(response_data['message']) # If some other error, return the error message
	else:
		print('Unable to create host object {} - status code: {}'.format(name, response.status_code))
		# print(response.text)
		# response_data = json.loads(response.text)
		# print(response_data)

def add_network(sid, name, subnet, subnet_mask, comments='', add_to_grp=False, grp_name=None):
	# Add network object:
	request_headers = {'Content-Type': 'application/json', 'X-chkp-sid': sid}

	if add_to_grp == True:
		data = {'name': name, 'subnet': subnet, 'subnet-mask': subnet_mask, 'comments': comments, 'groups': [grp_name]}
	else:
		data = {'name': name, 'subnet': subnet, 'subnet-mask': subnet_mask, 'comments': comments}

	response = requests.post(base_url+'add-network', data=json.dumps(data), headers=request_headers, verify=False)
	
	if response.status_code == 200:
		status = response.status_code
		return status
	else:
		print('Unable to create network object {} - status code: {}'.format(name, response.status_code)) 

def add_network_obj_grp(sid, name):
	# Add object-group:
	request_headers = {'Content-Type': 'application/json', 'X-chkp-sid': sid}

	data = {'name': name}

	response = requests.post(base_url+'add-group', data=json.dumps(data), headers=request_headers, verify=False)

	if response.status_code == 200:
		status = response.status_code
		return status
	else:
		print('Something went wrong - maybe object group already exist')
		print(response.status_code)
		print(response.text)
	
def add_service_tcp(sid, name, port):
	# Add TCP port:
	request_headers = {'Content-Type': 'application/json', 'X-chkp-sid': sid}

	data = {'name': name, 'port': port}

	response = requests.post(base_url+'add-service-tcp', data=json.dumps(data), headers=request_headers, verify=False)

	if response.status_code == 200:
		status = response.status_code
		return status
	else:
		print('Unable to create tcp object {} - status code: {}'.format(name, response.status_code))
		
def add_service_udp(sid, name, port):
	# Add UDP port:
	request_headers = {'Content-Type': 'application/json', 'X-chkp-sid': sid}

	data = {'name': name, 'port': port}

	response = requests.post(base_url+'add-service-udp', data=json.dumps(data), headers=request_headers, verify=False)

	if response.status_code == 200:
		status = response.status_code
		return status
	else:
		print('Unable to create udp object {} - status code: {}'.format(name, response.status_code))

	


