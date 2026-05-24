📘 CampusBridge

A Role-Based Mental Health Support and Counseling Platform built with Django

🚀 Overview

CampusBridge is a full-stack web application designed to provide anonymous mental health support, counseling appointment scheduling, and secure messaging between students and counselors.

It enables students to submit support requests anonymously, book counseling sessions, and communicate securely with counselors through a structured system.

🎯 Key Features

🧑‍🎓 User Roles
Student
Counselor
Staff

🧠 Anonymous Support System
Anonymous profile generation (ANON-ID)
Support request submission with file attachments
Track submitted requests (status-based view)
Edit and delete support requests

📅 Appointment System
Counselor availability slot generation
Appointment booking system
Approval / rejection workflow
Automatic notification system
Slot management dashboard for counselors

💬 Messaging System
Anonymous chat between students and counselors
Conversation-based architecture
File/media sharing in chat
Secure role-based access control

⚡ Slot Management
Auto generation of weekly counseling slots
Prevents double booking
Counselor-controlled scheduling system

📂 Media Support
File upload in support requests
File sharing in chat messages
Secure media storage using Django FileField
🏗️ Project Architecture

Core Apps
accounts → User authentication & role management
support → Anonymous support request system
appointments → Counseling scheduling system
messaging → Secure chat system
CampusBridge (core) → Project configuration & routing

🧩 Models Overview
User (Custom AbstractUser)
AnonymousProfile
SupportRequest
CounselorAvailability
Appointment
Conversation
Message
Notification

⚙️ Tech Stack
Backend: Django 5.x
Database: SQLite (development)
Frontend: HTML, CSS, Bootstrap
Media Handling: Django FileField


