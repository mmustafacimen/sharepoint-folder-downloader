# SharePoint Folder Downloader

Download an entire SharePoint / OneDrive folder using the Microsoft Graph API.
---

## Features

- Microsoft Graph API integration
- Automatic OAuth2 access token retrieval
- Recursive folder search
- Recursive folder download
- Downloads all files inside the selected folder

---

## Requirements

Python 3.8+

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Before running the script, update the following variables in the code:

Required values:

* CLIENT_ID – Azure application client ID
* CLIENT_SECRET – Azure application client secret
* TENANT_ID – Azure tenant ID
* USERNAME – Microsoft account username
* PASSWORD – Microsoft account password

These credentials must belong to an Azure AD application with the required permissions.

Required Microsoft Graph permissions:

```
Files.Read
Files.Read.All
Sites.Read.All
```

## Usage

Run the script:


```
python sharepoint_folder_downloader.py
```

The script will ask for the folder name:

```
Please enter the name of the folder you want to download:
```

After entering the folder name, the script will:

1. Search for the folder in your drive
2. Retrieve its folder ID
3. Download all files and subfolders recursively

Downloaded files will be saved in the current directory.

## Project Structure

```
sharepoint-folder-downloader
│
├── sharepoint_folder_downloader.py
├── requirements.txt
└── README.md
```

## Notes

* The script downloads files using the Microsoft Graph API.
* The folder search is recursive, meaning the script scans subfolders as well.
* Make sure your Azure AD application has the required API permissions.

  * `Files.Read`
  * `Files.Read.All`
  * `Sites.Read.All`

## Security Warning

Never publish real credentials in a public repository.

Always remove or replace sensitive information before uploading to GitHub.
