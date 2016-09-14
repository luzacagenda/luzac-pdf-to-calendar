# Luzac PDF to Google Calendar
Convert PDF to Google Calendar.


#### Install & Usage

Requirements
- Unix system
- Python 2.7

```
git clone https://github.com/lesander/luzac-pdf-to-calendar.git
cd luzac-pdf-to-calendar/
pip install --upgrade pdfminer
pip install --upgrade google-api-python-client
```

Create a new project at [console.developers.google.com](https://console.developers.google.com).
Select `web server (node.js)` as platform, set `http://localhost:8080` as allowed Javascript origin,
and add `http://localhost:8080/` (note the `/` at the end!) to the authorized redirect URI's.

When finished, download the `client_secret.json` and place it in the `luzac-pdf-to-calendar` folder.

For the first time, run `python googleoauth.py` and give consent to your application.

Download the latest Luzac Rooster PDF to the `luzac-pdf-to-calendar` folder.
Note the page number your schedule is on and run:
```
python ./main.py <my-page> <my-pdf>
```
Replace `<my-page>` with for example `20` and `<my-pdf>` with for example `luzac-rooster.pdf`.
