import requests
import os

# update process

username = 'AntonderDenker'
repository = 'guess_the_correlation_game'
asset_name = 'guess_the_correlation.exe'

# Make a GET request to the GitHub API to fetch the latest release
url = f'https://api.github.com/repos/{username}/{repository}/releases/latest'
response = requests.get(url)

# Parse the JSON response
release = response.json()

# Get the download URL of the release asset
filename = "guess_the_correlation.exe"
if 'assets' in release:
    download_url = None
    for asset in release['assets']:
        if asset['name'] == asset_name:
            download_url = asset['browser_download_url']
            break

    if download_url is None:
        print(f'Error: Failed to find asset "{asset_name}" in the latest release.')
    else:
        print(f'Download URL: {download_url}')
        response = requests.get(download_url)
        updated_executable_content = response.content
        if os.path.isfile(filename):
            with open('temp_executable.exe', 'wb') as f:
                f.write(updated_executable_content)

            os.replace('temp_executable.exe', filename)
        else:
            with open(filename, "wb") as f:
                f.write(updated_executable_content)

else:
    print("Error: Failed to fetch assets from the latest release")