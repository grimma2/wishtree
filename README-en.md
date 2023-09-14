#### <a href="https://github.com/grimma2/wishtree">Русский</a> / <a href="https://github.com/grimma2/wishtree/blob/main/README-en.md">English</a>

## About

Available at the link: https://quiz-game1.store

The "Tree of Good Deeds" project was created for a competition by a volunteer organization to organize the Tree of Good Deeds in the city. On the website, compassionate individuals can view letters from different children to Ded Moroz (Father Frost) and fulfill their wishes by selecting the letters they like and scheduling a meeting to deliver gifts.

## Functionality
- Email authentication, email confirmation, and user permissions.
- List of letters on the homepage, displayed in a slider. Each letter, except for the author, includes an image and the specified gift. Each letter has its own status (Not Selected, Selected, Reserved, Delivered), which is determined by the background color of the letter.
- Search for letters in the website header by gift and author's name.
- Sorting of letters based on their status.
- Ability to select letters as "Favorites" and reserve the selected letters on the Favorites page.
- Ability to view where to purchase the gift mentioned in the letter.
- List of letters for the administrator user, where they can change the letter's status.
- List of users for the administrator, who have already reserved some letters. The list includes the user's email and phone number for contact, as well as the number of reserved letters. The administrator has the ability to cancel reservations made by any user in case the user cannot be reached.

Create a Python virtual environment in the project directory:
```
python -m venv venv
```
Activate it:
```
venv/Scripts/activate
```
Install all dependencies:
```
pip install -r requirements.txt
```
Set the migrations:
```
python manage.py migrate
```
And finally, start the server:
```
python manage.py runserver
```
