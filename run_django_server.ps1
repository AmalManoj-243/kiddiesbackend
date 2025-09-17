# PowerShell script to activate env and run Django server
cd "C:\Users\sulab\Desktop\reactnative\amalkiddies-master (1)"
& "C:\Users\sulab\Desktop\reactnative\amalkiddies-master (1)\booksenvv\Scripts\Activate.ps1"
& "C:\Users\sulab\Desktop\reactnative\amalkiddies-master (1)\booksenvv\Scripts\python.exe" manage.py runserver 0.0.0.0:8000
