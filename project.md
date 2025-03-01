# Project Attendance System / Dochazkovy system

This project is based on two applications:

## 1. Employee Application

**Functionality:**
- Check-in
- Check-out
- Other actions (further details needed)

**Features:**
- Utilizes a camera hardware driver to capture the employee's face.
- Calculates a facial vector from the captured image.
- Compares the calculated vector with vectors stored in the database for verification.
- Employee verification through facial vector and PIN code.
- Mode selection upon successful verification.
- Tracks employee work status (present or absent).
- Upon employee confirmation, sets status to 'at work' and starts tracking time in the database.
- Database models can be extended with various other functions and methods.

## 2. Dashboard / Overview

**Users:**
- Company Owner
- Director
- HR Manager

**Access:**
- Administrative panel

**Data Access:**
- Employee count
- Real-time status of employees (at work, on business trip, on sick leave)
- Statistics
- Hour reports
- Sending informational emails

This improved formatting uses Markdown headings, lists, and bold text to structure the information in `project.md` for better readability.
