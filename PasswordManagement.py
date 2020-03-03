import sys
import os
import argon2
import uuid

# separate words from numbers 
def Enroll(username, password):
	# checks if username is enrolled. If not then append to file 
	with open('UserNamePasswordFile.txt', 'r+') as f:
		#initialize file with headers to be able to append
		FoundCollision = False
		for line in f:
			for word in line.split():
				if word == username:
					print ("Error: username already entered")
					print ("Rejected")
					FoundCollision = True 
					sys.exit(-1)
		#if username is not in file then we check its password with the 4 cases
		# [num]
		# [word]
		# [numword]
		# [wordnum]
		if FoundCollision == False:
			#first case [num]
			if password.isdigit():
				print("Error: Password entered violates [num] property")
				print("Rejected")
				FoundCollision = True
				sys.exit(-1)
				# give error message and dont go to next line
			with open('dictionary.txt','r') as f2, open('UserNamePasswordFile.txt', 'a') as f:
				numOfLine = 0;
				for line2 in f2:
					numOfLine+=1
					#second case [word]
					if line2.strip() == password:
						print("Error: Password entered violates [word] property")
						print("Rejected")
						FoundCollision = True	
						sys.exit(-1)
						FoundCollision = True
					if any(char.isdigit() for char in password):
						if line2.strip() in password: #check to see if there is a char next to an int
							print("Error: This password violates [wordnum] or [numword] property")
							print("Rejected")
							FoundCollision = True
							sys.exit(-1)
				if FoundCollision == False:
					f.write(username + " ")
					f.write(password + "\n")
					print ("Accepted\n")
					return
								

def Authenticate(usernameInput, new_pass):
	
	hashed_password = hash_password(new_pass)
	print("The string to store in the database is: " + hashed_password)
	passwordInput = raw_input("Now please enter a password again to check: ")
	
	with open('UserNamePasswordFile.txt', 'r') as f:
		FoundCollision = False
		for line in f:
			if usernameInput == line.split()[0] and new_pass == line.split()[1]:
				if check_password(hashed_password, passwordInput):
					print("You entered the right password according to hash\n")
					print ("Access Granted\n")
					FoundCollision = False
					sys.exit(0)
		print("I am sorry but the password does not match or the username you entered is not in the password file\n")
		print("Access Denied\n")
		sys.exit(-1)
				
				
def hash_password(password):
	salt = uuid.uuid4().hex
	h = argon2.argon2_hash(password, salt) + ':' + salt
	return h
	
	
def check_password(hashed_password, user_password):
	password, salt = hashed_password.split(':')
	return password == argon2.argon2_hash(user_password, salt)



def Main():
	print ("UserName: " + sys.argv[1] + "\n" + "Password: " + sys.argv[2])
	p = Enroll(sys.argv[1],sys.argv[2])
	yes = raw_input("Do you want to authenticate (Yes) or (No)?:" + " " + "\n")
	if yes == "Yes":
		usernameInput = raw_input("Enter Username:" + " ")
		new_pass = raw_input("Please enter a password to authenticate with hash: ")
		k = Authenticate(usernameInput,new_pass) 
	else:
		sys.exit(0)	
	
Main()
	

	
	
	
	