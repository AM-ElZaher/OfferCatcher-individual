import schedule
import time
import smtplib, ssl
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import datetime


def job():
    # Get Product Price by Xpath
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.get("https://egypt.souq.com/eg-en/realme-rma207-watch-s-smart-watch-with-blood-oxygen-level-sensor-black-132227539/i/")
    element_text = driver.find_element_by_xpath(
        '//*[@id="content-body"]/div/header/div[2]/div[2]/div[3]/div/section/div/div/div[1]/h3').text
    # remove vat txt
    # noVat = element_text.replace('(Inclusive of VAT)', '')
    # remove EGP txt
    noEGP = element_text.replace('EGP', '')
    # remove any spaces
    remSpace = noEGP.replace(' ', '')
    remFasla = noEGP.replace(',', '')
    driver.quit()

    # remove everything after (.) so it will be valid price
    a_string = remFasla
    split_string = a_string.split(".", 1)
    finalTEXT = split_string[0]
    print(finalTEXT)

    # compare scrapped price with target price
    if int(finalTEXT) < 700:
        print("SALE!!")
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        fromaddr = "Sender@gmail.com"
        toaddr = "Reciver@gmail.com"
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Realme RMA207 Watch Price Changed!!!!"
        body = "Item: " + "\n" "Realme RMA207 Watch " + " Has Been Reduced to: " + finalTEXT + " On Souq Egypt" + "\n" + "https://egypt.souq.com/eg-en/realme-rma207-watch-s-smart-watch-with-blood-oxygen-level-sensor-black-132227539/i/"
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(fromaddr, "PASSWORD")
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
        print("Mail Sent")
        timeNow = datetime.datetime.now().__str__()
        logfile = open('log.txt', 'a')
        logfile.write('\n' + 'Last run: ' + ' ' + timeNow)
        logfile.close()


    else:
        print("Not Yet")
        timeNow = datetime.datetime.now().__str__()
        logfile = open('log.txt', 'a')
        logfile.write('\n' + 'Last run: ' + ' ' + timeNow)
        logfile.close()



#schedule.every(30).seconds.do(job)
schedule.every(15).minutes.do(job)
# schedule.every().hour.do(job)
# schedule.every().day.at("01:59").do(job)



while 1:
    schedule.run_pending()
    time.sleep(1)

