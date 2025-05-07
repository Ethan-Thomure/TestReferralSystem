# Test Referral System

This was a college final project. This terminal-based application is based around the management of the two tables in the database:

# Dropoff Table
This table represents when a teacher/professor drops off test(s), the columns associated are:
- id [Integer]
- test_name [VARCHAR]
- date_in [Date]
- instructor_name [VARCHAR]
- initial_amount [Integer]
- current_amount [Integer]

# Pickup Table
This table represents when a teacher/professor picks up their test(s), the tests could be completed or expired:
- id [Integer]
- CE (Completed or Expired) [VARCHAR(1)]
- student_name [VARCHAR]
- test_name [VARCHAR]
- HN (Homework or Notecard) [VARCHAR(1)]
- date_in [Date]
- date_out [Date]
- staff_initial [VARCHAR]
- SFMP (Sent/Filed/Mailed/Pickup) [VARCHAR]
- instructor_name [VARCHAR]
- dropoff_id [Integer]
- is_resolved [Boolean]

# Installation
clone the repository

# Usage
As this is a Python Project, go to where you cloned this project, then run in your terminal:
```bash
python main.py
```
I have found that the IDE that I used it in doesn't really display very well (PyCharm), as I imported from sqlalchemy, prettytable, and use a clear screen commmand for the terminal


# Main Menu
![image](https://github.com/user-attachments/assets/ae3f530b-6260-4a8c-a772-69e86d8f6fa6)

# Pickup Query Example
![image](https://github.com/user-attachments/assets/65c592ee-ffbe-497a-88c0-b57e6d450bc3)

