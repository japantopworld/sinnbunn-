from flask import Flask, render_template, request
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
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