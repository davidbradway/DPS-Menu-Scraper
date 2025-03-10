# Post Events to a Google Calendar via the API

## Setting Up a New Project with Google API Libraries
1. **Create a Project**:
   - Go to the [Google Cloud Console](https://support.google.com/googleapi/answer/6251787?hl=en).
   - Click on the project dropdown and select "New Project."
   - Enter a project name and, optionally, edit the project ID. Click "Create."

2. **Enable APIs**:
   - In the Cloud Console, navigate to **"APIs & Services" > "Library."**
   - Search for the API you want to use and click **"Enable."**
   - Our project uses the Google Calendar API

3. **Set Up Billing (if required)**:
   - Some APIs require billing to be enabled.
   - Go to **"Billing"** in the Cloud Console and link a billing account to your project.

## Configuring Credentials
1. **Choose the Right Credential Type**:
   - Our project uses an **OAuth 2.0 Client ID** for accessing user data with their consent.
   - Create a Desktop app OAuth client ID.

2. **Create Credentials**:
   - Navigate to **"APIs & Services" > "Credentials"** in the Cloud Console.
   - Click **"Create Credentials"** and select the appropriate type (OAuth Client ID).

3. **Set Up OAuth Consent Screen**:
   - Navigate to **"OAuth consent screen"** in the Cloud Console.
   - Fill in the required details, such as:
     - **App Name**
     - **Support Email**
     - **Authorized Domains**
   - Add the required scopes for the APIs you plan to use.

4. **Download Credentials**:
   - For OAuth, download the JSON file containing your credentials using the down arrow icon under the Clients menu for your project.
   - Rename the downloaded file `credentials.json` and move it to the root of the repository.
   - *Keep this file secure.* Do not add it to the repository or push it.

5. **Integrate Credentials in Your Application
   - The Python script `gcal.py` loads the credentials the first time it is run
   - The credentials are used in web authentication flow via a website to download a token and save it to a JSON file. Make sure this file is in the same working directory.
   - Then on subsequent runs, until the token expires, the saved `token.json` file is loaded.