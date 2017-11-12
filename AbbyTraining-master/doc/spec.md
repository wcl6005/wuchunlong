# API

## Auth

### Login
- URL: /signin
	- Method: POST
		- Data:
			- email: String
			- password: String
			- remember: Boolean, default False
		- Return:
			- Status: 200
			- Status: !200
				- message: String

### Logout
- URL: /signout
	- Method: GET

## User

### Users
- URL: /users
	- Method: POST
	- Method: GET

### User
- URL: /users/\<md5_id:id\>

## Course

## Chapter