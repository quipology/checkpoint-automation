#!/usr/bin/python
__author__ = 'Bobby Williams <bobby.williams@xxx.com>'

import base
import sys

menu = '''==============
Select Option:
==============
c1 - Add New Host Object (Commercial)
c2 - Add New Network Object (Commercial)
c3 - Add New Network Object-Group (Commercial)
c4 - Show/Replicate Existing Object-Group (Commercial --> Government)
c5 - List Object Groups (Commercial)
c6 - Add New TCP Port (Commercial)
c7 - Add New UDP Port (Commercial)
---------------------------------------------------------------------
g1 - Add New Host Object (Government)
g2 - Add New Network Object (Government)
g3 - Add New Network Object-Group (Government)
g4 - Show/Replicate Existing Object-Group (Government --> Commercial)
g5 - List Object Groups (Government)
g6 - Add New TCP Port (Government)
---------------------------------------------------------------------
a1 - Add New Host Object (To *ALL* Domains)
a2 - Add New Network Object (To *ALL* Domains)
a3 - Add New Network Object-Group (To *ALL* Domains)
a4 - Add New TCP port (To *ALL* Domains)
---------------------------------------------------------------------
sh - Show Host Object
sn - Show Network Object
---------------------------------------------------------------------
ceh - Edit Host Object

s - Show All Active User Sessions
q - Quit
---------------
> '''

def display_menu():
	selection = input(menu)
	return selection

def main():
	sids = base.login()
	com_sid = sids[0]
	gov_sid = sids[1]
	com_session_uid = sids[2]
	gov_session_uid = sids[3]
	print('=' * 30)
	print('Your Commercial session id is: {}'.format(com_session_uid))
	print('-' * 30)
	print('Your Government session id is: {}'.format(gov_session_uid))
	print('=' * 30)
	while True:
		selection = display_menu()

# ------------ STANDARD OPTIONS BEGIN ----------------
		if selection.upper() == 'Q':
			sys.exit()
		elif selection.upper() == 'P':
			com_task = base.publish_changes(com_sid)
			print('Commercial changes published! - {}'.format(com_task))
			gov_task = base.publish_changes(gov_sid)
			print('Government changes published! - {}'.format(gov_task))

		elif selection.upper() == 'D':
			base.discard_changes(com_sid)
			base.discard_changes(gov_sid)

		elif selection.upper() == 'S':
			base.show_sessions(com_sid, com_session_uid)
			base.show_sessions(gov_sid, gov_session_uid)
# ------------ STANDARD OPTIONS END ----------------


# --------------- Add Host Object BEGIN ---------------
		elif selection.upper() == 'C1':
			name = input('Enter Host Object Name:> ')
			while True:
				ip_address = input('Enter Host IP address:> ')
				try:
					ip_address_split = ip_address.split('.')
				except:
					print('Invalid IP address format, try again..')
				else:
					numbers = ''.join(ip_address_split)
					try:
						numbers = int(numbers)
					except:
						print('Invalid IP address format, try again..')
					else:
						break
			comment = input('Enter object comment/description (optional):> ')
			add_to_grp = input('Add this new object to an existing object-group? (y/n):> ')
			if add_to_grp.upper() == 'Y':
				add_to_grp = True
				grp_name = input('Group name that you wish to add this object to?:> ')
				print('Adding object {} to Commercial domain and adding it to object-group {}..'.format(name, grp_name))
				status_code = base.add_host(com_sid, name, ip_address, comments=comment, add_to_grp=add_to_grp, grp_name=grp_name)
				if status_code == 200:
					com_task = base.publish_changes(com_sid)
					print('Finished - changes published! Commercial Task id: {}'.format(com_task))
				else:
					base.discard_changes(com_sid)
					print('Something went wrong - changes aborted.')
			else:
				print('Adding object {} to Commercial domain..'.format(name))
				status_code = base.add_host(com_sid, name, ip_address, comments=comment)
				if status_code == 200:
					com_task = base.publish_changes(com_sid)
					print('Finished - changes published! Commercial Task id: {}'.format(com_task))
				else:
					base.discard_changes(com_sid)
					print('Something went wrong - changes aborted.')

		elif selection.upper() == 'G1':
			name = input('Enter Host Object Name:> ')
			while True:
				ip_address = input('Enter Host IP address:> ')
				try:
					ip_address_split = ip_address.split('.')
				except:
					print('Invalid IP address format, try again..')
				else:
					numbers = ''.join(ip_address_split)
					try:
						numbers = int(numbers)
					except:
						print('Invalid IP address format, try again..')
					else:
						break
			comment = input('Enter object comment/description (optional):> ')
			add_to_grp = input('Add this new object to an existing object-group? (y/n):> ')
			if add_to_grp.upper() == 'Y':
				add_to_grp = True
				grp_name = input('Group name that you wish to add this object to?:> ')
				print('Adding object {} to Government domain and adding it to object-group {}..'.format(name, grp_name))
				status_code = base.add_host(gov_sid, name, ip_address, comments=comment, add_to_grp=add_to_grp, grp_name=grp_name)
				if status_code == 200:
					gov_task = base.publish_changes(gov_sid)
					print('Finished - changes published! Government Task id: {}'.format(gov_task))
				else:
					base.discard_changes(gov_sid)
					print('Something went wrong - changes aborted.')
			else:
				print('Adding object {} to Government domain..'.format(name))
				status_code = base.add_host(gov_sid, name, ip_address, comments=comment)
				if status_code == 200:
					gov_task = base.publish_changes(gov_sid)
					print('Finished - changes published! Government Task id: {}'.format(gov_task))
				else:
					base.discard_changes(gov_sid)
					print('Something went wrong - changes aborted.')

		elif selection.upper() == 'A1':
			name = input('Enter Host Object Name:> ')
			while True:
				ip_address = input('Enter Host IP address:> ')
				try:
					ip_address_split = ip_address.split('.')
				except:
					print('Invalid IP address format, try again..')
				else:
					numbers = ''.join(ip_address_split)
					try:
						numbers = int(numbers)
					except:
						print('Invalid IP address format, try again..')
					else:
						break
			comment = input('Enter object comment/description (optional):> ')
			add_to_grp = input('Add this new object to an existing object-group? (y/n):> ')
			if add_to_grp.upper() == 'Y':
				add_to_grp = True
				grp_name = input('Group name that you wish to add this object to?:> ')
				print('Adding object {} to *ALL* domains and adding it to object-group {}..'.format(name, grp_name))
				com_status_code = base.add_host(com_sid, name, ip_address, comments=comment, add_to_grp=add_to_grp, grp_name=grp_name)
				gov_status_code = base.add_host(gov_sid, name, ip_address, comments=comment, add_to_grp=add_to_grp, grp_name=grp_name)
				if com_status_code == 200 and gov_status_code == 200:
					com_task = base.publish_changes(com_sid)
					gov_task = base.publish_changes(gov_sid)
					print('Finished - changes published! Task ids:')
					print('{} (Commercial)'.format(com_task))
					print('{} (Government)'.format(gov_task))
				else:
					base.discard_changes(com_sid)
					base.discard_changes(gov_sid)
					print('Something went wrong - changes aborted.')
			else:
				print('Adding object {} to *ALL* domains..'.format(name))
				com_status_code = base.add_host(com_sid, name, ip_address, comments=comment)
				gov_status_code = base.add_host(gov_sid, name, ip_address, comments=comment)
				if com_status_code == 200 and gov_status_code == 200:
					com_task = base.publish_changes(com_sid)
					gov_task = base.publish_changes(gov_sid)
					print('Finished - changes published! Task ids:')
					print('{} (Commercial)'.format(com_task))
					print('{} (Government)'.format(gov_task))
				else:
					base.discard_changes(com_sid)
					base.discard_changes(gov_sid)
					print('Something went wrong - changes aborted.')
# --------------- Add Host Object END ---------------

# --------------- Add Network Object BEGIN ---------------
		elif selection.upper() == 'C2':
			name = input('Enter Network Object Name:> ')
			subnet = input('Enter Subnet (without mask-length):> ')
			while '/' in subnet:
				print('Subnet only please without mask-length..')
				subnet = input('Enter Subnet (without mask-length):> ')
			subnet_mask = input('Enter Subnet Mask:> ')
			while '/' in subnet_mask:
				print('Subnet mask only please not mask-length..')
				subnet_mask = input('Enter Subnet Mask:> ')
			comment = input('Enter object comment/description (optional):> ')
			add_to_grp = input('Add this new object to an existing object-group? (y/n):> ')
			if add_to_grp.upper() == 'Y':
				add_to_grp = True
				grp_name = input('Group name that you wish to add this object to?:> ')
				print('Adding object {} to Commercial domain and adding it to object-group {}..'.format(name, grp_name))
				status_code = base.add_network(com_sid, name, subnet, subnet_mask, comments=comment, add_to_grp=add_to_grp, grp_name=grp_name)
				if status_code == 200:
					com_task = base.publish_changes(com_sid)
					print('Finished - changes published! Commercial Task id: {}'.format(com_task))
				else:
					base.discard_changes(com_sid)
					print('Something went wrong - changes aborted.')
			else:
				print('Adding object {} to Commercial domain..'.format(name))
				status_code = base.add_network(com_sid, name, subnet, subnet_mask, comments=comment)
				if status_code == 200:
					com_task = base.publish_changes(com_sid)
					print('Finished - changes published! Commercial Task id: {}'.format(com_task))
				else:
					base.discard_changes(com_sid)
					print('Something went wrong - changes aborted.')

		elif selection.upper() == 'G2':
			name = input('Enter Network Object Name:> ')
			subnet = input('Enter Subnet (without mask-length):> ')
			while '/' in subnet:
				print('Subnet only please without mask-length..')
				subnet = input('Enter Subnet (without mask-length):> ')
			subnet_mask = input('Enter Subnet Mask:> ')
			while '/' in subnet_mask:
				print('Subnet mask only please not mask-length..')
				subnet_mask = input('Enter Subnet Mask:> ')
			comment = input('Enter object comment/description (optional):> ')
			add_to_grp = input('Add this new object to an existing object-group? (y/n):> ')
			if add_to_grp.upper() == 'Y':
				add_to_grp = True
				grp_name = input('Group name that you wish to add this object to?:> ')
				print('Adding object {} to Government domain and adding it to object-group {}..'.format(name, grp_name))
				status_code = base.add_network(gov_sid, name, subnet, subnet_mask, comments=comment, add_to_grp=add_to_grp, grp_name=grp_name)
				if status_code == 200:
					gov_task = base.publish_changes(gov_sid)
					print('Finished - changes published! Government Task id: {}'.format(gov_task))
				else:
					base.discard_changes(gov_sid)
					print('Something went wrong - changes aborted.')
			else:
				print('Adding object {} to Government domain..'.format(name))
				status_code = base.add_network(gov_sid, name, subnet, subnet_mask, comments=comment)
				if status_code == 200:
					gov_task = base.publish_changes(gov_sid)
					print('Finished - changes published! Government Task id: {}'.format(gov_task))
				else:
					base.discard_changes(gov_sid)
					print('Something went wrong - changes aborted.')

		elif selection.upper() == 'A2':
			name = input('Enter Network Object Name:> ')
			subnet = input('Enter Subnet (without mask-length):> ')
			while '/' in subnet:
				print('Subnet only please without mask-length..')
				subnet = input('Enter Subnet (without mask-length):> ')
			subnet_mask = input('Enter Subnet Mask:> ')
			while '/' in subnet_mask:
				print('Subnet mask only please not mask-length..')
				subnet_mask = input('Enter Subnet Mask:> ')
			comment = input('Enter object comment/description (optional):> ')
			add_to_grp = input('Add this new object to an existing object-group? (y/n):> ')
			if add_to_grp.upper() == 'Y':
				add_to_grp = True
				grp_name = input('Group name that you wish to add this object to?:> ')
				print('Adding object {} to *ALL* domains and adding it to object-group {}..'.format(name, grp_name))
				com_status_code = base.add_network(com_sid, name, subnet, subnet_mask, comments=comment, add_to_grp=add_to_grp, grp_name=grp_name)
				gov_status_code = base.add_network(gov_sid, name, subnet, subnet_mask, comments=comment, add_to_grp=add_to_grp, grp_name=grp_name)
				if com_status_code == 200 and gov_status_code == 200:
					com_task = base.publish_changes(com_sid)
					gov_task = base.publish_changes(gov_sid)
					print('Finished - changes published! Task ids:')
					print('{} (Commercial)'.format(com_task))
					print('{} (Government)'.format(gov_task))
				else:
					base.discard_changes(com_sid)
					base.discard_changes(gov_sid)
					print('Something went wrong - changes aborted.')
			else:
				print('Adding object {} to *ALL* domains..'.format(name))
				com_status_code = base.add_network(com_sid, name, subnet, subnet_mask, comments=comment)
				gov_status_code = base.add_network(gov_sid, name, subnet, subnet_mask, comments=comment)
				if com_status_code == 200 and gov_status_code == 200:
					com_task = base.publish_changes(com_sid)
					gov_task = base.publish_changes(gov_sid)
					print('Finished - changes published! Task ids:')
					print('{} (Commercial)'.format(com_task))
					print('{} (Government)'.format(gov_task))
				else:
					base.discard_changes(com_sid)
					base.discard_changes(gov_sid)
					print(com_status_code, gov_status_code)
					print('Something went wrong - changes aborted.')
# --------------- Add Network Object END ---------------

		elif selection.upper() == 'C3':
			name = input('Enter Network Object-Group Name:> ')
			print('Adding object {} to Commercial domain..'.format(name))
			status_code = base.add_network_obj_grp(com_sid, name)
			if status_code == 200:
				com_task = base.publish_changes(com_sid)
				print('Finished - changes published! Commercial Task id: {}'.format(com_task))
			else:
				print('Something went wrong - changes aborted.')

		elif selection.upper() == 'G3':
			name = input('Enter Network Object-Group Name:> ')
			print('Adding object {} to Government domain..'.format(name))
			status_code = base.add_network_obj_grp(gov_sid, name)
			if status_code == 200:
				gov_task = base.publish_changes(gov_sid)
				print('Finished - changes published! Government Task id: {}'.format(com_task))
			else:
				print('Something went wrong - changes aborted.')

		elif selection.upper() == 'A3':
			name = input('Enter Network Object-Group Name:> ')
			print('Adding object {} to *ALL* domains..'.format(name))
			com_status_code = base.add_network_obj_grp(com_sid, name)
			gov_status_code = base.add_network_obj_grp(gov_sid, name)
			if com_status_code == 200 and gov_status_code == 200:
				gov_task = base.publish_changes(gov_sid)
				com_task = base.publish_changes(com_sid)
				print('Finished - changes published! Task ids:')
				print('{} (Commercial)'.format(com_task))
				print('{} (Government)'.format(gov_task))
			else:
				base.discard_changes(com_sid)
				base.discard_changes(gov_sid)
				print('Something went wrong - changes aborted.')

# def discard_changes(sid, uid=None):
# def add_network_obj_grp(sid, name):


# -------------- Show Network Object-Group/Replicate BEGIN -------------
		elif selection.upper() == 'C4':
			grp_name = input('(Commercial) Object Group Name:> ')
			members = base.show_grp_obj(com_sid, grp_name)
			replicate = input('Do you wish to replicate this object-group to the Government domain? (y/n):> ')
			# Check to see if user wants object-group replicated to Government Domain:
			if replicate.upper() == 'Y':
				print('Replicating {} to Government domain..'.format(grp_name))
				# First create the object-group on Government domain:
				added_grp_uid = base.add_network_obj_grp(gov_sid, grp_name)
				if added_grp_uid:
					for i in members:
						if len(i) == 3:
							name, ip_address, comments = i[0], i[1], i[2]
							status_code = base.add_host(gov_sid, name, ip_address, comments=comments, add_to_grp=True, grp_name=grp_name)
							# print(status_code) #test
							if status_code == 200:
								print('{} added!'.format(name))
								continue
							else:
								print('Something went wrong with adding {} to group {} - a manual add will be required'.format(name, grp_name))

						elif len(i) == 4:
							name, subnet, subnet_mask, comments = i[0], i[1], i[2], i[3]
							status_code = base.add_network(gov_sid, name, subnet, subnet_mask, comments=comments, add_to_grp=True, grp_name=grp_name)
							# print(status_code) #test
							if status_code == 200:
								print('{} added!'.format(name))
								continue
							else:
								print('Something went wrong with adding {} to group {} - a manual add will be required'.format(name, grp_name))
					
					gov_task = base.publish_changes(gov_sid)
					print('Finished - changes published! Government Task id: {}'.format(gov_task))
			
		elif selection.upper() == 'G4':
			grp_name = input('(Government) Object Group Name:> ')
			members = base.show_grp_obj(gov_sid, grp_name)
			replicate = input('Do you wish to replicate this object-group to the Commercial domain? (y/n):> ')
			# Check to see if user wants object-group replicated to Commercial Domain:
			if replicate.upper() == 'Y':
				print('Replicating {} to Commercial domain..'.format(grp_name))
				# First create the object-group on Commercial domain:
				added_grp_uid = base.add_network_obj_grp(com_sid, grp_name)
				if added_grp_uid:
					for i in members:
						if len(i) == 3:
							name, ip_address, comments = i[0], i[1], i[2]
							status_code = base.add_host(com_sid, name, ip_address, comments=comments, add_to_grp=True, grp_name=grp_name)
							# print(status_code) #test
							if status_code == 200:
								print('{} added!'.format(name))
								continue
							else:
								print('Something went wrong with adding {} to group {} - a manual add will be required'.format(name, grp_name))

						elif len(i) == 4:
							name, subnet, subnet_mask, comments = i[0], i[1], i[2], i[3]
							status_code = base.add_network(com_sid, name, subnet, subnet_mask, comments=comments, add_to_grp=True, grp_name=grp_name)
							# print(status_code) #test
							if status_code == 200:
								print('{} added!'.format(name))
								continue
							else:
								print('Something went wrong with adding {} to group {} - a manual add will be required'.format(name, grp_name))
					
					com_task = base.publish_changes(com_sid)
					print('Finished - changes published! Commercial Task id: {}'.format(com_task))
			
# -------------- Show Network Object-Group/Replicate END -------------

# ------------- Add New TCP PORT ------------------#
		elif selection.upper() == 'C6':
			name = input('TCP Port Name: ')
			port = input('TCP Port Number: ')
			status = base.add_service_tcp(com_sid, name, port)
			if status:
				com_task = base.publish_changes(com_sid)
				print('TCP Port object created successfully!')

# ------------- Add New UDP PORT ------------------#
		elif selection.upper() == 'C7':
			name = input('UDP Port Name: ')
			port = input('UDP Port Number: ')
			status = base.add_service_udp(com_sid, name, port)
			if status:
				com_task = base.publish_changes(com_sid)
				print('UDP Port object created successfully!')

# --------------  List Network Object Groups BEGIN ----------------		
		elif selection.upper() == 'C5':
			base.list_obj_grps(com_sid)
		elif selection.upper() == 'G5':
			base.list_obj_grps(gov_sid)
# --------------  List Network Object Groups END ----------------				

#---------------  Show Object BEGIN ------------------------#

		elif selection.upper() == 'SH':
			domain = input('A) Commercial\nB) Government\n> ')
			if domain.upper() == 'A':
				host_name = input('Host Object Name: ')
				base.show_host(com_sid, host_name)
			elif domain.upper() == 'B':
				host_name = input('Host Object Name: ')
				base.show_host(gov_sid, host_name)

		elif selection.upper() == 'SN':
			domain = input('A) Commercial\nB) Government\n> ')
			if domain.upper() == 'A':
				network_name = input('Network Object Name: ')
				base.show_host(com_sid, network_name)
			elif domain.upper() == 'B':
				network_name = input('Network Object Name: ')
				base.show_host(gov_sid, network_name)	
#---------------  Show Object END ------------------------#

#---------------  Edit Host Object BEGIN ------------------------#
		elif selection.upper() == 'CEH':
			host_name = input('Host Object Name you want to add to group: ')
			group_name = input('Name of the Group you want to add host object to: ')
			base.edit_host(com_sid, host_name, add_group=True, grp_name=group_name)
			com_task = base.publish_changes(com_sid)

#---------------  Edit Host Object END ------------------------#

		keep_going = input('-' * 40 +'\nHave another task (y/n)?> ')
		if keep_going.upper() == 'N':
			sys.exit()

if __name__ == '__main__':
	main()	
