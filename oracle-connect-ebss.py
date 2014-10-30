import cx_Oracle
import sys
from datetime import date

def convertToGMT(hour):
	print 'hour', hour
	### Convert to Integer to do math
	hour = int(hour) + 5
	print hour

	### If hour is over 24, roll back using modulus
	if hour > 24:
		print hour, 'is greater than 24'
		hour = hour % 24
		hour = '0' + str(hour)
		#print hour

	print 'GMT', hour
	
	### Convert back to string
	hour = str(hour)

	### because we lose the leading 0 when we convert to INT above ###
	if len(hour) == 1:
		hour = '0' + hour
		print 'Padded Hour with 0'
	return hour

def convertDate(incoming_date):
	#Convert Oracle_Datetime (2006, 10, 25, 20, 24, 8) to yymmddhhmmss  GMT
	#print incoming_date.strftime("%d, %m, %y, %H, %M, %S")
	string_date = incoming_date.strftime("%d, %m, %Y, %H, %M, %S")
	day, month, year, hour, minute, second = string_date.split(',')
	day = day.strip()
	year = year.strip()
	month = month.strip()
	second = second.strip()
	minute = minute.strip()
	hour = hour.strip()
	hour = convertToGMT(hour)
	newdate = year+month+day+hour+minute+second
	newdate = newdate.strip()
	return newdate

def main():

	 ### Load LDAP Settings ##############
	fo = open("settings_oracle.txt", "r+")
	username = fo.readline().strip()
	password = fo.readline().strip()
	server = fo.readline().strip()
	serviceID = fo.readline().strip()	

	foutput = open("oracle_users2.txt", "w+")

	try:
		
		con = cx_Oracle.connect(username + '/' + password + '@' + server + '/' + serviceID)
		print con.version

		cursor = con.cursor()
		cursor.arraysize = 150000
	 	
		try:
			
			### Attributes stored in Oracle DB
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

			######## Run Query ############
			cursor.execute("SELECT * FROM D5768PGM.V_EBSS_VSTR_DTLS")
			#cursor.execute("SELECT * FROM D5768PGM.V_EBSS_VSTR_DTLS WHERE USER_ID = 'RENNOC' and LAST_UPDATE_DATETIME >= '25-OCT-06'")
			
			#cursor.execute("SELECT * FROM D5768PGM.V_EBSS_VSTR_DTLS WHERE LAST_UPDATE_DATETIME >= '25-OCT-06'")
			
			#cursor.execute("SELECT * FROM D5768PGM.V_EBSS_VSTR_DTLS WHERE USER_ID = 'RENNOC' or USER_ID = 'elephant' or USER_ID = 'SGREENE'") 
			#cursor.execute("SELECT * FROM D5768PGM.V_EBSS_VSTR_DTLS WHERE USER_ID = 'RENNOC' or USER_ID = 'elephant' or USER_ID = 'SGREENE' or USER_ID = 'DRCOCOA'")	
			## Always returns 30 columns in the same order #######
    	
			print "Query Returned - Fetching Data"
			data = cursor.fetchall()
			#print data
			#print type(data)

			i = 0
			for result in data:
	   			#print result
				# result should be a tuple, so this should work
				print result
				print len(result), 'attributes returned'
				attribute_dict = {}
				
				#### Load all thef fields - Most will not be used ##########
				oracle_vstr_id = result[0]   #Unique ID for ESS DB
				oracle_userName = result[1]
				oracle_title = result[2]
				oracle_firstName = result[3]
				oracle_lastName = result[4]
				oracle_birthDate = result[5]
				oracle_gender = result[6]
				oracle_email_address = result[7]   # Not Specified
				oracle_customerCode_id = result[8] 
				oracle_customerType = result[9]
				oracle_userSpecialtyID = result[10]
				oracle_userSpecialty = result[11]
				oracle_registrationDate = result[12]
				oracle_latestUpdate = result[13]
				oracle_validationStatus = result[14]
				oracle_validationType = result[15]
				oracle_crm_id = result[16]  # not
				logically_deleted = result[17]  # not
				referral_code = result[18]  # not
				email_status = result[19]  # not
				campaign_id = result[20]  # not
				cpm_email_id = result[21] # not
				cpm_id = result[22] # not
				oracle_addressLine1 = result[23]
				oracle_addressLine2 = result[24]
				oracle_addressLine3 = result[25]
				oracle_city = result[26]
				oracle_postalCode = result[27]
				oracle_newsletter = result[28]
				oracle_addressComplement = result[29]

				print "processing User:", oracle_userName
				print 'birthdate', oracle_birthDate

				##### Convert Datetime to custom date format #######
				if oracle_registrationDate is not None:
					oracle_registrationDate = convertDate(oracle_registrationDate)
					print 'oracle_registrationDate:', oracle_registrationDate
				if oracle_latestUpdate is not None:
					oracle_latestUpdate = convertDate(oracle_latestUpdate)
					print 'oracle_latestUpdate:', oracle_latestUpdate
	 			
				if  oracle_birthDate is not None:
					#print oracle_birthDate, type(oracle_birthDate)
					oracle_birthDate = convertDate(oracle_birthDate)


				### None Checking for the attributes we care about	
				if oracle_title  is None:
					oracle_title = ''
				if oracle_latestUpdate is None:
					oracle_latestUpdate = ''
				if oracle_customerType is None:
					oracle_customerType = ''
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

				try:
					print 'writing user:', i	
						
					foutput.write(oracle_userName + "|" +  oracle_firstName +  "|" + oracle_lastName + "|" + oracle_title + "|" + oracle_customerType +  "|" + oracle_registrationDate \
					+ "|" + oracle_latestUpdate  + "|" + oracle_userSpecialty  +  "|" + oracle_validationStatus  +  "|" + oracle_addressComplement +  "|" \
					+  oracle_addressLine1  +  "|" + oracle_addressLine2  +  "|" + oracle_birthDate +  "|" + oracle_city + "|" + oracle_gender + "|" \
					+ oracle_postalCode + '\n')

					print 'Done with', i
					
				except:
					print - 'Failed to write', oracle_userName, 'to file'

				i = i + 1

			cursor.close()
			print i, "users returned"
			        	
		
		except cx_Oracle.DatabaseError as e:
	    		error, = e.args
	    		if error.code == 955:
		        	print('Table already exists')
	    		if error.code == 1031:
	   	   		print("Insufficient privileges - are you sure you're using the owner account?")
	  	  	print(error.code)
	   		print(error.message)
	   		print(error.context)
		
		con.close()

	except:
	    print "Failed to Connect or Processing Error"
	    
	foutput.close()	

if __name__ == "__main__":
    main()

