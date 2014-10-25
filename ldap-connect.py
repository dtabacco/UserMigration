import ldap,sys
import os.path

def main():

	 ### Load LDAP Settings ##############
	fo = open("settings_ldap.txt", "r+")
	username = fo.readline().strip()
	password = fo.readline().strip()
	server = fo.readline().strip()
	baseDN = fo.readline().strip()	

	foutput = open("bds_import.txt", "w+")
	
	try:
		l = ldap.initialize(server)

		###### Doesn't actually authenticate until the search is performed ########
		l.simple_bind(username, password)

		#### LDAP Search Settings ############################
		searchScope = ldap.SCOPE_SUBTREE
		retrieveAttributes = None #["uid"]
		searchFilter = "uid=tabacco"

		# Dummy Connection - Not sure why this is necessary
		ldap_result_id = l.search(baseDN, searchScope, 'uid=no-one', retrieveAttributes)
		result_type, result_data = l.result(ldap_result_id, 0)

		#### Open User File from Oracle #######
	 	userfile = open("oracle_users.txt", "r+")

	 	counter = 1

	 	for user in userfile:
	 		print 'user: ', counter
	 		searchFilter = "uid=" + user	
	 		print "searchFilter:", searchFilter 
			
	 		#### Retry Logic - for flukey fails ################
			give_up = "false"
			done = "false"
			attempts = 0	

			### hardcoded attributes
			operation = 'ADD'
			ldap_CountryOfRegistration = 'US'
			ldap_locale = 'eng_IN'
			language = 'eng_IN'

			#### LDAP Attributes
			ldap_uid = ''
			ldap_cn = ''
			ldap_emailAddress = ''
			ldap_password = ''

			### Ignored Attributes
			uump_uid = ''	
			msdCorporateInfo = ''
			msdCorporateInfoLastUpdate = ''
			msdPathInfo = ''
			msdPathInfoLastUpdate = ''
			msdProductInfo = ''
			msdProductInfoLastUpdate = ''
			uniAnnouncements = ''
			uniAnnouncementsLastUpdate = ''
			uniMedicalEducation = ''
			uniMedicalEducationLastUpdate = ''
			uniMedicalUpdates = ''
			uniMedicalUpdatesLastUpdate = ''
			privacyPolicy = ''
			privacyPolicyDate = ''
			termsOfUse = ''
			termsOfUseDate = ''
			validationDate = ''
			citizenId = ''
			countryOfResidence = ''
			crmMemberId  = ''
			department  = ''
			district  = ''
			expirationDate  = ''
			fax  = ''
			federationId  = ''   # Check this one
			fieldOfStudy  = ''
			firstNameVocatif = ''
			initials = ''
			insurer1 = ''
			insurer2 = ''
			insurer3 = ''
			lastNameVocatif = ''
			licenseIssuingBody = ''
			licenseIssuingBody2 = ''
			mobileNumber = ''
			organisation = ''
			organisationCity = ''
			organisationName = ''
			practicingHcp = ''
			promotionCode = ''
			province = ''
			registrationStatus = ''
			secondName = ''
			smsConsent = ''
			studentId = ''



			### Attributes Loaded From Oracle File
			oracle_latestUpdate = ''
			oracle_customerType = ''
			oracle_firstName = ''
			oracle_lastName = ''
			oracle_registrationDate = ''
			oracle_userName = ''  # using ldap_uid for now
			oracle_userSpecialty = ''
			oracle_validationStatus = ''
			oracle_addressComplement = ''
			oracle_addressLine1 = ''
			oracle_addressLine2 = ''
			oracle_addressType = ''
			oracle_birthDate = ''
			oracle_city = ''
			oracle_gender = ''
			oracle_licenseNumber = ''
			oracle_licenseNumber2 = ''
			oracle_phoneNumber = ''
			oracle_postalCode = ''
			oracle_salutation = ''
			oracle_title = ''


			##### Start Search ############################
			while give_up == "false" and done == "false":
				try:
					ldap_result_id = l.search(baseDN, searchScope, searchFilter, retrieveAttributes)
					
					result_set = []
					while 1:
						result_type, result_data = l.result(ldap_result_id, 0)
						#print result_type
						#print result_data
						for all_attributes in result_data:
							#print "printing The Tuple"
							for attribute_dict in all_attributes:	
								try:
									for attribute, val in attribute_dict.items():
											#print "attribute:", attribute
											if attribute == "mail":
												for item in val:
													print "mail:",item
													ldap_emailAddress = item	
											if attribute == "uid":
												for item in val:
													print "uid:",item
													ldap_uid = item
											if attribute == "cn":
												for item in val:
													print "cn",item		
													ldap_cn = item
											if attribute == "userPassword":
												for item in val:
													print "password",item		
													ldap_password = item				
								except:
									#print "Error Iterating through Dictionary"
									pass
				
						
						if result_type == 101:
							print "Not found - repeat"
							attempts = attempts + 1
							if attempts >= 2:
								give_up = "true"
							break
						if result_type == 100:
							#print "Done"
							done = "true"
							break					

						if (result_data == []):
							break
						else:
							## here you don't have to append to a list
							## you could do whatever you want with the individual entry
							## The appending to list is just for illustration. 
							if result_type == ldap.RES_SEARCH_ENTRY:
								result_set.append(result_data)
					#print result_set
				except:
					print "Search Error"

			###### User Complete - Write To File ########
			foutput.write('"' + operation + '","'  + ldap_cn + '","' + uump_uid + '","'  + ldap_CountryOfRegistration  + '","'   + ldap_locale  + '","' \
				+ msdCorporateInfo + '","' + msdCorporateInfoLastUpdate + '","' + msdPathInfo + '","' + msdPathInfoLastUpdate + '","' \
				+ msdProductInfo + '","' + msdProductInfoLastUpdate + '","' + uniAnnouncements + '","' + uniAnnouncementsLastUpdate + '","' \
				+ uniMedicalEducation + '","' + uniMedicalEducationLastUpdate + '","' + uniMedicalUpdates + '","' + uniMedicalUpdatesLastUpdate + '","' \
				+ oracle_latestUpdate + '","' + oracle_customerType + '","' + ldap_emailAddress + '","' + oracle_firstName + '","' \
				+ oracle_lastName + '","' + ldap_password + '","' + privacyPolicy + '","' + privacyPolicyDate + '","' + oracle_registrationDate  + '","' \
				+ termsOfUse + '","' + termsOfUseDate + '","' + ldap_uid + '","' + oracle_userSpecialty + '","' + validationDate  + '","' \
				+ oracle_validationStatus + '","' + oracle_addressComplement + '","' + oracle_addressLine1 + '","' + oracle_addressLine2 + '","' + oracle_addressType  + '","' \
				+ oracle_birthDate + '","' + citizenId + '","' + oracle_city + '","' + countryOfResidence + '","' + crmMemberId  + '","' \
				+ department + '","' + district + '","' + expirationDate + '","' + firstNameVocatif + '","' + oracle_gender  + '","' \
				+ initials + '","' + insurer1 + '","' + insurer2 + '","' + insurer3 + '","' + language  + '","'  + lastNameVocatif  + '","'  \
				+ licenseIssuingBody + '","' + licenseIssuingBody2 + '","' + oracle_licenseNumber + '","' + oracle_licenseNumber2 + '","' + mobileNumber  + '","'  + organisation  + '","'  \
				+ organisationCity + '","' + organisationName + '","' + oracle_phoneNumber + '","' + oracle_postalCode + '","' + practicingHcp  + '","'  + promotionCode  + '","'  \
				+ province + '","' + registrationStatus + '","' + oracle_salutation + '","' + secondName + '","' + smsConsent  + '","'  + studentId  + '","' + oracle_title   \
				+ '"'  "\n")	
			
			counter = counter + 1	

	except:
	      print "Connection error"

	fo.close()
	foutput.close()      

if __name__ == "__main__":
    main()