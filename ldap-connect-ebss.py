import ldap,sys
import os.path
from bs4 import BeautifulSoup

#### Load Specialty Dictionary from File #########
specialty = {}
specnamefile = open("speciality_names.txt", "r+")
speccodefile = open("speciality_codes.txt", "r+")
for spec in specnamefile:
	specialty[spec] = speccodefile.readline().strip()

designation = {}
profdesnamefile = open("prof_designation_names.txt", "r+")
customercodefile = open("customer_codes.txt", "r+")
for des in profdesnamefile:
	designation[des] = customercodefile .readline().strip()

def getSpecialtyCode(specialtyName):

	specialtyName = specialtyName.strip()
	print "Assessing speciality", specialtyName
	
	specialtycode = ''
	for item, val in specialty.items():
			#print item, val
			if specialtyName == item.strip():
				specialtycode = val
				print 'found specialty code', val
				break
			else:
				#print specialtyName, "does not match", item
				#print len(specialtyName), len(item)
				pass

	return specialtycode;

def getCustomerCode(designationName):

	designationName = designationName.strip()
	customer_code = ''
	for item, val in designation.items():
		if designationName == item.strip():
			customer_code = val
			print 'found customer code', val
			break
		else:
			#print "Found No Designation"
			pass

	### Additional Logic ###		

	return customer_code	

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
	header_row_more = "initials,insurer1,insurer2,insurer3,language,lastName,lastNameVocatif,licenseIssuingBody,licenseIssuingBody2,licenseNumber,licenseNumber2,mobileNumber,organisation,organisationCity,organisationName,password,phoneNumber,postalCode,practicingHcp,privacyPolicy,privacyPolicyDate,promotionCode,province,registrationDate,registrationStatus,salutation,secondName,smsConsent,studentId,termsOfUse,termsOfUseDate,title,userName,userSpecialty,validationDate,validationStatus,jobTitle,licenseNumber3,professionalDesignation"
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
	 	userfile = open("oracle_users2.txt", "r+")

		print "Opened File"

	 	counter = 1
	 	#### Debug Counting #####
		SSHA_count = 0
		SHA_count = 0

	 	for user in userfile:

	 		# decode what you receive:	
	 		user = user.decode('iso8859-1')

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
			oracle_postalCode = ''
			oracle_salutation = ''
			oracle_title = ''
			oracle_userName = ''
			oracle_professionalDesignation = ''

			print 'loading user', counter

			## Split fails for that user..need to count commas
			oracle_userName, oracle_firstName, oracle_lastName, oracle_title, oracle_professionalDesignation, oracle_registrationDate, oracle_latestUpdate, oracle_userSpecialty, oracle_validationStatus, oracle_addressComplement, oracle_addressLine1, oracle_addressLine2, oracle_birthDate, oracle_city, oracle_gender, oracle_postalCode = user.split('|')
			
			oracle_userName = oracle_userName.strip()
			oracle_firstName = oracle_firstName.strip()
			oracle_lastName = oracle_lastName.strip()
			oracle_title = oracle_title.strip()
			oracle_professionalDesignation = oracle_professionalDesignation.strip()
			oracle_registrationDate = oracle_registrationDate.strip()
			oracle_latestUpdate = oracle_latestUpdate.strip()
			oracle_userSpecialty = oracle_userSpecialty.strip()
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
			if oracle_professionalDesignation is None:
				oracle_professionalDesignation = ''
			if oracle_registrationDate is None:
				oracle_registrationDate = ''	
			if oracle_userSpecialty is None:
				oracle_userSpecialty = ''	
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
			ldap_locale = 'eng-US'
			language = 'eng-US'

			#### LDAP Attributes
			ldap_uid = ''
			ldap_cn = ''
			ldap_emailAddress = ''
			ldap_password = ''
			ldap_phoneNumber = ''

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
			privacyPolicy = '0'
			privacyPolicyDate = '20141029000000'   # TO DO - make Today more dynamic
			termsOfUse = '0'
			termsOfUseDate = '20141029000000'   #  TO DO - make Today more dynamic
			validationDate = ''
			citizenId = ''
			countryOfResidence = ''
			crmMemberId  = ''
			department  = ''
			district  = ''
			expirationDate  = ''
			grade = ''
			fax  = ''
			federationId  = ''   
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
			jobTitle = ''
			licenseNumber = ''
			licenseNumber2 = ''
			licenseNumber3 = ''
			professionalDesignation = ''
			CredentialType = ''
			CredentialNumber = ''
			CredentialIssuer = ''
			CredentialStatus = ''
			state_license_flag = 'NO'
			AMA_license_flag = 'NO'
			AOA_license_flag = 'NO'
			workphn_flag = 'NO'		

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
													if item[:6] == '{SSHA}':
														print "SSHA Found"
														SSHA_count = SSHA_count + 1
														print "Current SSHA count:", SSHA_count
													elif item[:5] == '{SHA}':
														print "SHA Found"
														SHA_count = SHA_count + 1
														print "Current SHA count:", SHA_count	

											if attribute == "mrkInternetCredential":
												for item in val:
													print "mrkInternetCredential",item
													try:
														soup = BeautifulSoup(item)
														for CredentialIssuer in soup('issuer'):
															#### Check to see the issuer of license
															if CredentialIssuer.text[:3] == 'US-' and len(CredentialIssuer.text) == 5:
																print "state condition matched"
																state_license_flag = 'YES'
																licenseIssuingBody = CredentialIssuer.text[3:]
															elif CredentialIssuer.text[2:] == '-AOA':
																print "AOA condition matched"
																AOA_license_flag = 'YES'
															elif CredentialIssuer.text[2:] == '-AMA':
																print "AMA condition matched"
																AMA_license_flag = 'YES'
														#for CredentialType in soup('type'):
														#	print CredentialType.text
														for CredentialNumber in soup('number'):
															if state_license_flag == 'YES':
																licenseNumber = CredentialNumber.text
															if AOA_license_flag == 'YES':
																licenseNumber2 = CredentialNumber.text
															if AMA_license_flag == 'YES':
																licenseNumber3 = CredentialNumber.text		

														#for CredentialStatus in soup('status'):
														#### Reset Flags for next License Eval	
														state_license_flag = 'NO'
														AMA_license_flag = 'NO'
														AOA_license_flag = 'NO'
													except:
														print "failed to parse mrkInternetCredential"
											if attribute == "mrkInternetTelephoneNumber":
												for item in val:
													print "mrkInternetTelephoneNumber",item	
													try:
														soup = BeautifulSoup(item)
														for phonetype in soup('type'):
															#### Check to see type of Phone
															if phonetype.text == 'WORKPHN':
																workphn_flag = 'YES'
															if phonetype.text == 'FAX':
																fax_flag = 'YES'	
															print phonetype.text
														for phonenum in soup('number'):
															#### Check to see the issuer of license
															print phonenum.text	
															if workphn_flag == 'YES':
																## May need to format and remove -
																ldap_phoneNumber = phonenum.text.strip()
																ldap_phoneNumber = ldap_phoneNumber.replace('-','')
																ldap_phoneNumber = ldap_phoneNumber.replace('+','')
																ldap_phoneNumber = ldap_phoneNumber.replace(' ','')
																print "formatted Phone Number", ldap_phoneNumber
															else:
																print 'Not a Work Phone - Skipping'
																pass
															if fax_flag == 'YES':
																fax = phonenum.text.strip()
																fax = fax.replace('-','')
																fax = fax.replace('+','')
																fax = fax.replace(' ','')
																print "formatted Fax Number", fax
														workphn_flag = 'NO'
														fax_flag = 'NO'
													except:
														print "failed to parse mrkInternetTelephoneNumber"
											"""			
											if attribute == "mrkinternetProfDesignation":
												for item in val:
													print "mrkinternetProfDesignation",item	
													### Will need to do a lookup conversion...use dictionary
											if attribute == "mrkInternetMedicalSpecialtyAlt":
												for item in val:
													print "mrkInternetMedicalSpecialtyAlt",item		
													### Will need to do a lookup conversion...use dictionary
											"""				
																
								except:
									print "Error Iterating through Dictionary"
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
		
			if len(oracle_userSpecialty) > 0:
				print "Moving into specality with", oracle_userSpecialty
				## Convert MedicalSpecialty to CODE
				oracle_userSpecialtyName = oracle_userSpecialty
				oracle_userSpecialty = getSpecialtyCode(oracle_userSpecialty)	
	
			print "Looking up Professional Designation", oracle_professionalDesignation
			## Convert ProfessionalDesignation to CustomoerType
			if len(oracle_professionalDesignation) > 0:
				oracle_customerType = getCustomerCode(oracle_professionalDesignation)
				if oracle_professionalDesignation.strip() == 'M.D.':
					print 'oracle_userSpecialty:', oracle_userSpecialty
					print 'oracle_userSpecialtyName', oracle_userSpecialtyName
					if oracle_userSpecialty.strip() == '216.12' or oracle_userSpecialty.strip() == '216.63'  or oracle_userSpecialty.strip() == '216.46' or oracle_userSpecialty.strip() == '216.35':
						 if oracle_userSpecialtyName.strip() != 'Public Health':
							oracle_customerType = '102.7'
						 	print "Enacted General M.D. Code"
						 else:
						 	print "Almost Enacted General M.D. Code "	
			else:
				print "No designation, skipping customer code lookup"	
			
			print type(oracle_firstName)
			print type(oracle_lastName)

			oracle_firstName = oracle_firstName.encode('utf-8')
			oracle_lastName = oracle_lastName.encode('utf-8')
			oracle_gender = oracle_gender.encode('utf-8')
			oracle_addressLine1 = oracle_addressLine1.encode('utf-8')
			oracle_addressLine2 = oracle_addressLine2.encode('utf-8')
			oracle_addressComplement = oracle_addressComplement.encode('utf-8')
			oracle_addressType = oracle_addressType.encode('utf-8')
			oracle_city = oracle_city.encode('utf-8')
			oracle_latestUpdate = oracle_latestUpdate.encode('utf-8')

			
			print "firstname:" + oracle_firstName
			print "lastname:" + oracle_lastName
			print "fieldOfStudy:" + fieldOfStudy
			print "oracle_gender:" + oracle_gender
			print "firstNameVocatif:" + firstNameVocatif
			print "oracle_addressLine1:" + oracle_addressLine1
			print "oracle_addressLine2:" + oracle_addressLine2
			print "oracle_addressComplement:" + oracle_addressComplement
			print 'oracle_addressType:' + oracle_addressType
			print 'oracle_birthDate' + oracle_birthDate
			print 'LastUpdate' + oracle_latestUpdate

			#foutput.write(fieldOfStudy + '","' + oracle_firstName + '","' + firstNameVocatif + '","' + initials + '","' + oracle_gender + grade + '","' + graduationInstitute + '","' +  graduationYear + '","' + '\n')
			

			###### User Complete - Write To File ########
			print "writing", oracle_userName, "To File"
			
			foutput.write('"' + operation + '","'  + uump_uid + '","' + ldap_cn + '","' + ldap_CountryOfRegistration  + '","'  + ldap_locale  + '","')
			foutput.write(msdCorporateInfo + '","' + msdCorporateInfoLastUpdate + '","' + msdPathInfo + '","' + msdPathInfoLastUpdate + '","')
			foutput.write(msdProductInfo + '","' + msdProductInfoLastUpdate + '","' + uniAnnouncements + '","' + uniAnnouncementsLastUpdate + '","')
			foutput.write(uniMedicalEducation + '","' + uniMedicalEducationLastUpdate + '","' + uniMedicalUpdates + '","' + uniMedicalUpdatesLastUpdate + '","')
			foutput.write(oracle_latestUpdate + '","' + oracle_addressComplement + '","' + oracle_addressLine1 + '","' + oracle_addressLine2 + '","' + oracle_addressType  +  '","')
			foutput.write(oracle_birthDate + '","' + citizenId + '","')
			foutput.write(oracle_city + '","')
			foutput.write(countryOfResidence + '","' + crmMemberId  + '","')
			foutput.write(oracle_customerType + '","' + department + '","' + district + '","' + ldap_emailAddress + '","'  + expirationDate + '","' + fax  + '","' + federationId + '","')
			foutput.write(fieldOfStudy + '","' + oracle_firstName + '","'  + firstNameVocatif + '","' + oracle_gender  + '","' + grade + '","' + graduationInstitute + '","' +  graduationYear + '","' + initials + '","')	
			foutput.write(insurer1 + '","' + insurer2 + '","' + insurer3 + '","' + language  + '","'  + oracle_lastName + '","' + lastNameVocatif  + '","')
			foutput.write(licenseIssuingBody + '","' + licenseIssuingBody2 + '","' + licenseNumber + '","' + licenseNumber2 + '","' + mobileNumber  + '","'  + organisation  + '","')
			foutput.write(organisationCity + '","' + organisationName + '","' + ldap_password + '","' + ldap_phoneNumber + '","' + oracle_postalCode + '","' + practicingHcp  + '","')
			foutput.write(privacyPolicy + '","' + privacyPolicyDate + '","' + promotionCode + '","' + province + '","' + oracle_registrationDate + '","')
			foutput.write(registrationStatus + '","' + oracle_salutation + '","' + secondName + '","' + smsConsent  + '","'  + studentId  + '","')
			foutput.write(termsOfUse + '","' + termsOfUseDate + '","' + oracle_title + '","' + ldap_uid + '","' + oracle_userSpecialty + '","' + validationDate  + '","')
			foutput.write(oracle_validationStatus + '","' + jobTitle + '","' + licenseNumber3 + '","' + oracle_professionalDesignation)
			foutput.write('"\n')				
			
			'''
			foutput.write('"' + operation + '","'  + uump_uid + '","' + ldap_cn + '","'  + ldap_CountryOfRegistration  + '","'   + ldap_locale  + '","' \
				+ msdCorporateInfo + '","' + msdCorporateInfoLastUpdate + '","' + msdPathInfo + '","' + msdPathInfoLastUpdate + '","' \
				+ msdProductInfo + '","' + msdProductInfoLastUpdate + '","' + uniAnnouncements + '","' + uniAnnouncementsLastUpdate + '","' \
				+ uniMedicalEducation + '","' + uniMedicalEducationLastUpdate + '","' + uniMedicalUpdates + '","' + uniMedicalUpdatesLastUpdate + '","' \
				+ oracle_latestUpdate + '","' + oracle_addressComplement + '","' + oracle_addressLine1 + '","' + oracle_addressLine2 + '","' + oracle_addressType  +  '","' \
				+ oracle_birthDate + '","' + citizenId + '","' + oracle_city + '","' + countryOfResidence + '","' + crmMemberId  + '","' \
				+ oracle_customerType + '","' + department + '","' + district + '","' + ldap_emailAddress + '","'  + expirationDate + '","' + fax  +  '","' + federationId + '","' \
				+ fieldOfStudy + '","' + oracle_firstName + '","'  + firstNameVocatif + '","' + oracle_gender  + '","' + grade + '","' + graduationInstitute + '","' +  graduationYear + '","' + initials + '","' \
				+ insurer1 + '","' + insurer2 + '","' + insurer3 + '","' + language  + '","'  + oracle_lastName + '","' + lastNameVocatif  + '","'  \
				+ licenseIssuingBody + '","' + licenseIssuingBody2 + '","' + licenseNumber + '","' + licenseNumber2 + '","' + mobileNumber  + '","'  + organisation  + '","'  \
				+ organisationCity + '","' + organisationName + '","' + ldap_password + '","' + ldap_phoneNumber + '","' + oracle_postalCode + '","' + practicingHcp  + '","' \
				+ privacyPolicy + '","' + privacyPolicyDate + '","' + promotionCode + '","' + province + '","' + oracle_registrationDate + '","' \
				+ registrationStatus + '","' + oracle_salutation + '","' + secondName + '","' + smsConsent  + '","'  + studentId  + '","' \
				+ termsOfUse + '","' + termsOfUseDate + '","' + oracle_title + '","' + ldap_uid + '","' + oracle_userSpecialty + '","' + validationDate  + '","' \
				+ oracle_validationStatus + '","' + jobTitle + '","' + licenseNumber3 + '","' + oracle_professionalDesignation +'"\n')	
			'''
			counter = counter + 1	

	except:
	      print "Connection error"

	fdebug.write('SSHA Count: ' + str(SSHA_count) + '\n')
	fdebug.write('SHA Count: ' + str(SHA_count) + '\n')     
	fo.close()
	foutput.close()
	fdebug.close()      

if __name__ == "__main__":
    main()