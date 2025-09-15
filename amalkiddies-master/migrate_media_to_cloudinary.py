import os
import cloudinary
import cloudinary.uploader

# TODO: Replace with your actual Cloudinary credentials
cloudinary.config(
    cloud_name = 'djc3qirsl',
    api_key = '757284145337785',
    api_secret = 'Bd49Uo_soLIHibq1r5o3QOf5T60'
)

# Folders to migrate
folders = ['media/movies', 'media/tickets']

for folder in folders:
    for root, dirs, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            # Only upload image files
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif', '.avif')):
                print(f'Uploading {file_path}...')
                result = cloudinary.uploader.upload(file_path, folder=folder+'/')
                print(f'Uploaded: {result["secure_url"]}')
            else:
                print(f'Skipping unsupported file: {file_path}')

print('Migration complete!')
