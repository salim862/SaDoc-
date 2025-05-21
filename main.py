from flet import *
import mysql.connector

# اتصال بقاعدة البيانات
conn = mysql.connector.connect(
    host="mysql-197363-0.cloudclusters.net",
    user="admin",
    password="mhBWz8Wm",
    database="sal13",
    port=10003
)
cursor = conn.cursor()

def main(page: Page):
    page.title = 'SADhealth'
    page.scroll = 'auto'
    page.window.top = 1
    page.window.left = 960
    page.window.width = 340
    page.window.height = 740
    page.bgcolor = 'white'
    page.theme_mode = ThemeMode.LIGHT
    image_path = "C:/Users/salim/Desktop/project/doctor/assets/home.gif"
    page.add(
    Column(
        [
            Image(src=image_path, height=400),
        ],
        horizontal_alignment="center"
          )
            )

    def ensure_connection():
        if not conn.is_connected():
            try:
                conn.reconnect(attempts=3, delay=2)
            except mysql.connector.Error as err:
                page.dialog = AlertDialog(title=Text("Error"), content=Text(f"Error reconnecting to the database: {err}"))
                page.dialog.open = True
                page.update()
                return False
        return True

    def login_action(e):
        if not ensure_connection():
            return
        dokey = dokey_field.value
        query = "SELECT * FROM sikness_info WHERE dokey = %s"
        cursor.execute(query, (dokey,))
        result = cursor.fetchone()
        if result:
            cursor.execute("SELECT firstname, lastname, sickness, temperature FROM sikness_info WHERE dokey = %s", (dokey,))
            record = cursor.fetchone()
            if record:
                firstname, lastname, sickness, temperature = record
                show_patient_info(page, firstname, lastname, sickness, temperature, dokey)
            else:
                page.dialog = AlertDialog(title=Text("Error"), content=Text("No matching records found."))
                page.dialog.open = True
                page.update()
        else:
            page.dialog = AlertDialog(title=Text("Error"), content=Text("Invalid dokey."))
            page.dialog.open = True
            page.update()

    def show_patient_info(page, firstname, lastname, sickness, temperature, dokey):
        def send(e):
            if not ensure_connection():
                return
            appoi = appo_field.value.upper()
            improvment = impr_field.value
            try:
                if appoi == "YES":
                    date = date_field.value
                    time = time_field.value
                    cursor.execute("UPDATE sikness_info SET appointment = %s, date = %s, time = %s, improvment = %s WHERE dokey = %s", (appoi, date, time, improvment, dokey))
                else:
                    cursor.execute("UPDATE sikness_info SET appointment = 'NO', date = '2024-12-31', time = '00:00:00', improvment = %s WHERE dokey = %s", (improvment, dokey,))
                conn.commit()
                page.dialog = AlertDialog(title=Text("Success"), content=Text("Information was sent."))
                page.dialog.open = True
                page.update()
            except mysql.connector.Error as err:
                page.dialog = AlertDialog(title=Text("Information was not sent."), content=Text(f"Error: {err}"))
                page.dialog.open = True
                page.update()

        appo_field = TextField(label="Schedule an appointment with your patient?", width=300, prefix_icon=Icons.EVENT)
        date_field = TextField(label="YYYY-MM-DD", width=300, prefix_icon=Icons.CALENDAR_MONTH)
        time_field = TextField(label="HH:MM:SS", width=300, prefix_icon=Icons.LOCK_CLOCK)
        impr_field = TextField(label="Your thoughts", width=300, prefix_icon=Icons.NOTE)

        page.controls.clear()
        page.add(
            Column([
                Image(src="home.gif", width=280),
                Text(f"Patient: {firstname} {lastname}", size=18),
                Text(f"Sickness type: {sickness}", size=18),
                Text(f"Temperature: {temperature}", size=18),
                appo_field,
                date_field,
                time_field,
                impr_field,
                ElevatedButton(text="Send", on_click=send, width=290, style=ButtonStyle(bgcolor='blue', color='white'))
            ], alignment=MainAxisAlignment.CENTER, horizontal_alignment=CrossAxisAlignment.CENTER, spacing=20)
        )
        page.update()

    dokey_field = TextField(label='Enter your key', prefix_icon=Icons.PERSON, rtl=True, height=38)
    login_button = ElevatedButton(text="Login", width=290, style=ButtonStyle(bgcolor='blue', color='white'), on_click=login_action)

    page.add(
        Column([
            Text("Patient Management System", size=20, font_family="IBM Plex Sans Arabic", color='black'),
            dokey_field,
            login_button
        ], alignment=MainAxisAlignment.CENTER, horizontal_alignment=CrossAxisAlignment.CENTER, spacing=20)
    )
    page.update()

app(main)

