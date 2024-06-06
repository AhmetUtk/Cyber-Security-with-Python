import cv2
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
kamera = cv2.VideoCapture(0)


save_photo = False
photo_counter = 0

# "fotolar" klasörünü oluştur
fotolar = "fotolar"
os.makedirs(f"{fotolar}", exist_ok=True)

while True:
    _, goruntu = kamera.read()
    cv2.imshow("Orjinal", goruntu)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break
    elif key == ord("s"):
        save_photo = True

    if save_photo:
        photo_filename = os.path.join("fotolar", f"captured_photo_{photo_counter}.jpg")
        cv2.imwrite(photo_filename, goruntu)
        print(f"Fotoğraf kaydedildi: {photo_filename}")
        save_photo = False
        photo_counter += 1

# E-posta ayarları
email_address = ""  # Gönderici e-posta adresi
email_password = ""      # Gönderici e-posta şifresi
recipient_email = ""  # Alıcı e-posta adresi

# E-posta oluştur
email_subject = "Yakalanan Fotoğraflar"
email_body = "Yakalanan fotoğraflar ektedir."

email = MIMEMultipart()
email['From'] = email_address
email['To'] = recipient_email
email['Subject'] = email_subject
email.attach(MIMEText(email_body, 'plain'))

# "fotolar" klasöründeki tüm fotoğrafları e-postaya ekleyin
photo_folder = "fotolar"
photo_files = [f for f in os.listdir(photo_folder) if os.path.isfile(os.path.join(photo_folder, f))]

for photo_filename in photo_files:
    photo_path = os.path.join(photo_folder, photo_filename)
    attachment = open(photo_path, "rb")
    image = MIMEImage(attachment.read())
    attachment.close()

    image.add_header('Content-Disposition', f'attachment; filename = {photo_filename}')
    email.attach(image)

# E-postayı gönder
try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_address, email_password)
    text = email.as_string()
    server.sendmail(email_address, recipient_email, text)
    server.quit()
    print("E-posta gönderildi!")
except Exception as e:
    print(f"E-posta gönderilirken bir hata oluştu: (str){e}")
kamera.release()
cv2.destroyAllWindows()