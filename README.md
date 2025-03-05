# DS Chat: Secure and Usable Messaging Platform

## Project Overview
**DS Chat** is a secure end-to-end messaging platform designed for undergraduate students in the School of Computer Science at the University of Sydney. The platform allows students to share academic experiences, seek help, and access a knowledge repository of useful learning materials. The project is divided into two main parts: **Security** and **Usability**.

### Security Part
The security component focuses on implementing a secure messaging system that ensures confidentiality, integrity, and authentication. Key features include:
- **Secure Password Storage**: Passwords are securely stored on the server using hashing techniques to prevent offline pre-computation attacks.
- **Certificate Verification**: Users verify the server's certificate during login, ensuring secure communication.
- **Secure Password Transmission**: Passwords are transmitted securely using encryption protocols.
- **End-to-End Encryption**: Messages are encrypted such that even the server cannot read or modify the content, ensuring privacy and authenticity.

### Usability Part
The usability component expands the messaging platform into a comprehensive support system for students. Key features include:
- **User Roles**: Different roles such as students, alumni, and administrative staff are supported.
- **Knowledge Repository**: A shared space for students to upload and access learning materials.
- **Admin Functionality**: Admins can manage users and content, including deleting posts or muting users.
- **User-Specific Features**: Custom functionalities based on user needs, such as course guides or academic advice.

## Demo
[Demo Vedio](Demo/functionality_demo.mov)

## Key Features
- **Secure Messaging**: End-to-end encrypted communication between users.
- **User Authentication**: Secure login with password hashing and certificate verification.
- **Knowledge Sharing**: A repository for students to share and access academic resources.
- **Admin Controls**: Ability to manage users and content, ensuring a safe and organized environment.
- **User-Centric Design**: Features tailored to the needs of students, alumni, and staff.

## Technical Details
- **Programming Language**: Python (for backend security features)
- **Frameworks**: HTML, CSS, JavaScript (for frontend usability)
- **Security Protocols**: Encryption, hashing, and certificate-based authentication.
- **User Roles**: Students, Alumni, Administrative Staff.

## How It Works
1. **Login**: Users log in securely, verifying the server's certificate and transmitting their password securely.
2. **Messaging**: Users can send encrypted messages to each other, ensuring privacy.
3. **Knowledge Repository**: Students can upload and access learning materials, organized by categories.
4. **Admin Controls**: Admins can manage users and content, ensuring the platform remains useful and safe.

## Project Phases
1. **Security Implementation**: Focus on secure password storage, certificate verification, and end-to-end encryption.
2. **Usability Design**: Conduct user investigations, design navigation, and create prototypes for the website.
3. **Evaluation and Iteration**: Perform usability tests, gather feedback, and iterate on the design.
4. **Final Implementation**: Develop the high-fidelity prototype and integrate security features.

## Acknowledgments
This project was developed as part of the INFO2222 course, focusing on both security and usability in web-based applications. The goal is to create a platform that is not only secure but also user-friendly and tailored to the needs of its users.
