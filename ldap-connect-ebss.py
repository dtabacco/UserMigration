import ldap,sys
import os.path

def main():

	 ### Load LDAP Settings ##############
	fo = open("settings_ldap.txt", "r+")
	username = fo.readline().strip()
	password = fo.readline().strip()
	server = fo.readline().strip()
	baseDN = fo.readline().strip()	

	foutput = open("bds_import.csv", "w+")
	fdebug = open("bds_debug.txt", "w+")
	
	### This is not tested...if it crashes, look at this
	header_row = "lastUpdateType,userId,merckId,countryOfRegistration,locale,msdCorporateInfo,msdCorporateInfoLastUpdate,msdPathInfo,msdPathInfoLastUpdate,msdProductInfo,msdProductInfoLastUpdate,uniAnnouncements,uniAnnouncementsLastUpdate,uniMedicalEducation,uniMedicalEducationLastUpdate,uniMedicalUpdates,uniMedicalUpdatesLastUpdate,latestUpdate,addressComplement,addressLine1,addressLine2,addressType,birthDate,citizenId,city,countryOfResidence,crmMemberId,customerType,department,district,emailAddress,expirationDate,fax,federationId,fieldOfStudy,firstName,firstNameVocatif,gender,grade,graduationInstitute,graduationYear,"
	header_row_more = "initials,insurer1,insurer2,insurer3,language,lastName,lastNameVocatif,licenseIssuingBody,licenseIssuingBody2,licenseNumber,licenseNumber2,mobileNumber,organisation,organisationCity,organisationName,password,phoneNumber,postalCode,practicingHcp,privacyPolicy,privacyPolicyDate,promotionCode,province,registrationDate,registrationStatus,salutation,secondName,smsConsent,studentId,termsOfUse,termsOfUseDate,title,userName,userSpecialty,validationDate,validationStatus"
	header_row = header_row + header_row_more
	

	foutput.write(header_row + '\n')
	
	try:
		l = ldap.initialize(server)

		###### Doesn't actually authenticate until the search is performed ########
		l.simple_bind(username, password)

		#### LDAP Search Settings ############################
		searchScope = ldap.SCOPE_SUBTREE
		retrieveAttributes = None #["uid"]
		searchFilter = "uid="

		# Dummy Connection - Not sure why this is necessary
		ldap_result_id = l.search(baseDN, searchScope, 'uid=no-one', retrieveAttributes)
		result_type, result_data = l.result(ldap_result_id, 0)

		#### Open User File from Oracle #######
	 	userfile = open("oracle_users.txt", "r+")

		print "Opened File"

	 	counter = 1

	 	for user in userfile:

			### Attributes Loaded From Oracle File
			oracle_latestUpdate = ''
			oracle_customerType = ''
			oracle_firstName = ''
			oracle_lastName = ''
			oracle_registrationDate = ''
			oracle_userName = ''  
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
			oracle_userName = ''

			print 'loading user', counter

			## Split fails for that user..need to count commas
			oracle_userName, oracle_firstName, oracle_lastName, oracle_title, oracle_customerCode_id, oracle_registrationDate, oracle_latestUpdate, oracle_userSpecialtyID, oracle_validationStatus, oracle_addressComplement, oracle_addressLine1, oracle_addressLine2, oracle_birthDate, oracle_city, oracle_gender, oracle_postalCode = user.split('|')
			
			oracle_userName = oracle_userName.strip()
			oracle_firstName = oracle_firstName.strip()
			oracle_lastName = oracle_lastName.strip()
			oracle_title = oracle_title.strip()
			oracle_customerCode_id = oracle_customerCode_id.strip()
			oracle_registrationDate = oracle_registrationDate.strip()
			oracle_latestUpdate = oracle_latestUpdate.strip()
			oracle_userSpecialtyID = oracle_userSpecialtyID.strip()
			oracle_validationStatus = oracle_validationStatus.strip()
			oracle_addressComplement = oracle_addressComplement.strip()
			oracle_addressLine1 = oracle_addressLine1.strip()
			oracle_addressLine2 = oracle_addressLine2.strip()
			oracle_birthDate = oracle_birthDate.strip()
			oracle_city = oracle_city.strip()
			oracle_gender = oracle_gender.strip()
			oracle_postalCode = oracle_postalCode.strip()

			print "userName:", oracle_userName
			print "gender:", oracle_gender
			print "zip", oracle_postalCode

			### None Checking for the attributes we care about	
			if oracle_title  is None:
				oracle_title = ''
			if oracle_latestUpdate is None:
				oracle_latestUpdate = ''
			if oracle_customerCode_id is None:
				oracle_customerCode_id = ''
			if oracle_registrationDate is None:
				oracle_registrationDate = ''	
			if oracle_userSpecialtyID is None:
				oracle_userSpecialtyID = ''	
			if oracle_validationStatus is None:
				oracle_validationStatus = ''
			if oracle_addressComplement is None:
				oracle_addressComplement = ''
			if oracle_addressLine1 is None:
				oracle_addressLine1 = ''
			if oracle_addressLine2 is None:
				oracle_addressLine2 = ''
			if oracle_birthDate is None:
				oracle_birthDate = ''
			if oracle_city is None:
				oracle_city = ''
			if oracle_gender is None:
				oracle_gender = ''
			if oracle_postalCode is None:
				oracle_postalCode = ''
			if oracle_firstName is None:
				oracle_firstName = ''
			if oracle_lastName is None:
				oracle_lastName = ''	


	 		print 'user: ', counter
	 		#searchFilter = "uid=" + user
	 		searchFilter = "uid=" + oracle_userName	
	 		print "searchFilter:", searchFilter 
			
	 		#### Retry Logic - for flukey fails ################
			give_up = "false"
			done = "false"
			attempts = 0	

			### hardcoded attributes
			operation = 'ADD'
			ldap_CountryOfRegistration = 'US'
			ldap_locale = 'eng_US'
			language = 'eng_US'

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
			grade = ''
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
			graduationYear = ''
			graduationInstitute = ''
			secondName = ''
			smsConsent = ''
			studentId = ''			


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
							fdebug.write('Failed Attempt:' + oracle_userName + '\n')
							attempts = attempts + 1
							if attempts >= 5:
								give_up = "true"
								fdebug.write('Failed - Abandon:' + oracle_userName + '\n')
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
		
			print "zip", oracle_postalCode
			###### User Complete - Write To File ########
			print "writing", oracle_userName, "To File"
			foutput.write('"' + operation + '","'  + ldap_cn + '","' + uump_uid + '","'  + ldap_CountryOfRegistration  + '","'   + ldap_locale  + '","' \
				+ msdCorporateInfo + '","' + msdCorporateInfoLastUpdate + '","' + msdPathInfo + '","' + msdPathInfoLastUpdate + '","' \
				+ msdProductInfo + '","' + msdProductInfoLastUpdate + '","' + uniAnnouncements + '","' + uniAnnouncementsLastUpdate + '","' \
				+ uniMedicalEducation + '","' + uniMedicalEducationLastUpdate + '","' + uniMedicalUpdates + '","' + uniMedicalUpdatesLastUpdate + '","' \
				+ oracle_latestUpdate + '","' + oracle_addressComplement + '","' + oracle_addressLine1 + '","' + oracle_addressLine2 + '","' + oracle_addressType  +  '","' \
				+ oracle_birthDate + '","' + citizenId + '","' + oracle_city + '","' + countryOfResidence + '","' + crmMemberId  + '","' \
				+ oracle_customerType + '","' + department + '","' + district + '","' + ldap_emailAddress + '","'  + expirationDate + '","' + fax  +  '","' + federationId + '","' \
				+ fieldOfStudy + '","' + oracle_firstName + '","'  + firstNameVocatif + '","' + oracle_gender  + '","' + grade + '","' + graduationInstitute + '","' +  graduationYear + '","' + initials + '","' \
				+ insurer1 + '","' + insurer2 + '","' + insurer3 + '","' + language  + '","'  + oracle_lastName + '","' + lastNameVocatif  + '","'  \
				+ licenseIssuingBody + '","' + licenseIssuingBody2 + '","' + oracle_licenseNumber + '","' + oracle_licenseNumber2 + '","' + mobileNumber  + '","'  + organisation  + '","'  \
				+ organisationCity + '","' + organisationName + '","' + ldap_password + '","' + oracle_phoneNumber + '","' + oracle_postalCode + '","' + practicingHcp  + '","' \
				+ privacyPolicy + '","' + privacyPolicyDate + '","' + promotionCode + '","' + province + '","' + oracle_registrationDate + '","' \
				+ registrationStatus + '","' + oracle_salutation + '","' + secondName + '","' + smsConsent  + '","'  + studentId  + '","'
				+ termsOfUse + '","' + termsOfUseDate + '","' + oracle_title + '","' + ldap_uid + '","' + oracle_userSpecialty + '","' + validationDate  + '","' \
				+ oracle_validationStatus + '"\n')	
			
			counter = counter + 1	

	except:
	      print "Connection error"

	fo.close()
	foutput.close()      

if __name__ == "__main__":
    main()