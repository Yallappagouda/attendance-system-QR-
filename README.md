# Django QR Code Attendance System

This is a Django-based web application for managing attendance using QR codes. Staff can create attendance sessions, generate QR codes, and students can mark their attendance by scanning the QR code with their mobile devices.

---

## Features

- **Staff dashboard** to create and manage attendance sessions
- **QR code generation** for each session (students scan to mark attendance)
- **Student login & attendance marking**
- **Attendance records** for staff to review

---

## Project Structure

```
qrcode_attendance/
├── attendance/            # Main app for attendance logic
│   ├── migrations/
│   ├── templates/
│   ├── ...
├── qrcode_attendance/     # Project settings and URLs
├── db.sqlite3             # SQLite database (auto-created)
├── media/                 # Uploaded QR codes
├── static/                # Static files
├── manage.py              # Django management script
├── .gitignore
└── README.md
```

---

## Getting Started

### 1. **Clone the repository**

```bash
git clone https://github.com/YOUR-USERNAME/qrcode_attendance.git
cd qrcode_attendance
```

### 2. **Create a virtual environment & activate**

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. **Install dependencies**

```bash
pip install -r requirements.txt
```

If `requirements.txt` is missing, install dependencies manually:
```bash
pip install django qrcode pillow
```

### 4. **Apply migrations**

```bash
python manage.py migrate
```

### 5. **Create a superuser (for staff login)**

```bash
python manage.py createsuperuser
```
Follow the prompts to set up your admin account.

### 6. **Run the development server**

```bash
python manage.py runserver 0.0.0.0:8000
```

### 7. **Access the site**

- On your laptop: [http://127.0.0.1:8000/](http://127.0.0.1:8000/) or [http://localhost:8000/](http://localhost:8000/)
- On your mobile (same WiFi): `http://<your-laptop-ip>:8000/`

---

## Usage

1. Log in as staff and create a session.
2. The system generates a QR code for the session.
3. Students scan the QR code using their mobile device and log in.
4. Students mark their attendance for the session.

---

## Notes

- Ensure your laptop and students' mobiles are on the **same WiFi network**.
- The QR code must contain your laptop's **local IP address** (not `localhost`).
- Update `ALLOWED_HOSTS` in `settings.py` to include your IP.
- If your IP changes, update the code and regenerate QR codes.

---

## License

MIT License

---

## Author

[Yallappagouda](https://github.com/Yallappagouda)



This requirements.txt covers Django 5.2, QR code generation, and image handling.
If you use other packages (like django-crispy-forms, djangorestframework, etc.), add them as needed.
Install with:
Code
pip install -r requirements.txt