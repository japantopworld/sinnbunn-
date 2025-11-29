from flask import Flask, render_template, request
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json

app = Flask(__name__)

# Googleスプレッドシート認証
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

# credentials.json がある場合はファイルから、ない場合は環境変数から読み込む
if os.path.exists("credentials.json"):
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
else:
    creds_json = os.environ.get("GOOGLE_CREDENTIALS")
    creds_dict = json.loads(creds_json)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

client = gspread.authorize(creds)
sheet = client.open("新聞配達顧客管理").sheet1

@app.route("/")
def index():
    customers = sheet.get_all_records()
    return render_template("index.html", customers=customers)

@app.route("/deliver/<int:row>", methods=["POST"])
def deliver(row):
    sheet.update_cell(row+2, 3, "配達済み")
    customers = sheet.get_all_records()
    return render_template("index.html", customers=customers)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
