import os
import requests

# Azure AD and Microsoft Graph API
client_id = "your_client_id"
client_secret = "your_client_secret"
tenant_id = "your_tenant_id"

username = "your_username"
password = "your_password"
scope = "offline_access Files.Read Files.Read.All Sites.Read.All"


def get_access_token(username, password):
    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    token_data = {
        'grant_type': 'password',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': scope,
        'username': username,
        'password': password
    }
    token_response = requests.post(token_url, data=token_data)
    token_response.raise_for_status()
    return token_response.json()['access_token']


def find_folder_id(access_token, folder_name, parent_id='root'):
    drive_url = f"https://graph.microsoft.com/v1.0/me/drive/items/{parent_id}/children"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(drive_url, headers=headers)

    if response.status_code == 200:
        items = response.json().get('value', [])
        for item in items:
            if item['name'] == folder_name and 'folder' in item:
                return item['id']
            elif 'folder' in item:
                folder_id = find_folder_id(access_token, folder_name, item['id'])
                if folder_id:
                    return folder_id
    else:
        print(f"Error: {response.status_code}, {response.text}")
    return None


def download_items(access_token, folder_id, local_path="."):
    drive_url = f"https://graph.microsoft.com/v1.0/me/drive/items/{folder_id}/children"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    print("downloadurl", drive_url)
    response = requests.get(drive_url, headers=headers)

    if response.status_code == 200:
        items = response.json().get('value', [])
        for item in items:
            item_name = item['name']
            item_path = os.path.join(local_path, item_name)
            if 'file' in item:
                download_url = f"https://graph.microsoft.com/v1.0/me/drive/items/{item['id']}/content"
                download_response = requests.get(download_url, headers=headers)
                print("download_url:",download_url)
                if download_response.status_code == 200:
                    os.makedirs(os.path.dirname(item_path), exist_ok=True)
                    with open(item_path, 'wb') as f:
                        f.write(download_response.content)
                    print(f"File downloaded: {item_path}")
                else:
                    print(f"Download failed for file: {item_path}, Status Code: {download_response.status_code}")
            elif 'folder' in item:
                os.makedirs(item_path, exist_ok=True)
                print(f"Entering folder: {item_path}")
                download_items(access_token, folder_id=item['id'], local_path=item_path)
    else:
        print(f"Error: {response.status_code}, {response.text}")


def main():
    access_token = get_access_token(username, password)
    folder_name = input("Please enter the name of the folder you want to download: ")
    folder_id = find_folder_id(access_token, folder_name)

    if folder_id:
        print(f"Found folder ID: {folder_id}")
        download_items(access_token, folder_id)
    else:
        print(f"Folder '{folder_name}' not found.")


if __name__ == "__main__":
    main()
