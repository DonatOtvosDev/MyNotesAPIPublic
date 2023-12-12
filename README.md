# MyNotes
MyNotes is a simple not taking application with cloud saving. This represitory contains the API and the mobile aplication developed in flutter can be downloaded from the following link:
https://drive.google.com/file/d/152C7rmOlQy48ao9mjdTQa8kaFuWzW_Um/view?usp=sharing
The github represitory is at the following link:
https://github.com/DonatOtvosDev/MyNotesApp

## Dependencies
- fastapi[all]
- uvicorn[standard]
- python-jose[cryptography]
- passlib[bcrypt]
- SQLAlchemy
- pytest
- pytest-ordering
- httpx
- psycopg2

## Installation
Fork the represitory from github and enter the folder
Download dependencies
```bash
pip install -r requirements.txt
```
Run the project
```bash
python -m uvicorn main:app
```
Fast API's documetnation can be accessed at:
http://127.0.0.1:8000

## Usage
### User
  #### /register: You can register an account with username and password
  #### /token: You can request a token with you authentication details
  #### This token must be used for the following options and has to be include in the headers:
  \{"Authorization": "Bearer \(insert your token here\)"\}
  #### /user: returns your user info and your notes
  #### /deletelogin: you can delete you user information
  #### /note/\{note_id\}: It returns the note with the given id
  #### /createnote: It is the way to inatialize a new note with the content and title
  #### /updatenote: This is the method that changes the data of your note based on the provided id
  #### /deletenote: With this method you can delete the note at the given id
