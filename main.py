# from os import open, listdir, stat
from sys import exit
from ftplib import FTP
from smtplib import SMTP
from os import listdir, stat
from time import perf_counter
from os import path as ospath
from datetime import datetime
from email.message import EmailMessage



def search_newest_file(path):
    filelist = []

    for file in listdir(path):
        filetime = datetime.fromtimestamp(ospath.getctime(path + file))
        if filetime.date() == datetime.now().date():
            if file.endswith('.txt'):
                filelist.append(path + file)
    
    return [filelist, filetime]


def create_email(mail_from, mail_to, mail_subject, mail_body):
    msg = EmailMessage()
    msg.set_content(mail_body)

    msg['From'] = f'{mail_from}'
    msg['To'] = f"{mail_to}"
    msg['Subject'] = f"{mail_subject}"

    return msg


def send_email(sender, password, msg):
    send = SMTP(
        host='SMTP SERVER', 
        port=587, 
        local_hostname='localhost'
    )
    send.starttls()
    send.login(sender, password)
    send.send_message(msg)
    send.quit()


def open_ftp_connection(host, port, usr, pwd, up_dir, path, filename):
    with FTP() as ftp:
        ftp.connect(
            host, 
            port
        )
        ftp.login(
            usr, 
            pwd
        )
        ftp.cwd(up_dir)

        start = perf_counter()
        fp = open(filename, 'rb')
        ftp.storbinary('STOR %s' % ospath.basename(filename), fp, 102400)
        fp.close()
        end = perf_counter()

        output = ''.join([
            '{} INFO \t IP Address: {} \n'.format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), host),
            '{} INFO \t User: {} \n'.format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), usr),
            '{} INFO \t Directory: {} \n'.format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), up_dir),
            '{} TRACE \t uploading file via FTP protocol ... \n'.format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")),
            '{} TRACE \t File Uploaded Successfully in {}! \n'.format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), str(end-start)),
            '\n\n'
        ])

    return output



""" 
    FTP UPLOAD EXAMPLE
    IP:  192.168.10.50:21
    Usr: UserTest
    Pwd: passwordTest
    Source Folder:      D:/Source/Folder/
    Destination Folder: /Dest/Folder/


    OUTPUT LOG EXAMPLE
    18/01/2023 11:05:56 INFO 	 File: path\\file 
    18/01/2023 11:05:56 INFO 	 File size (B): 121 
    18/01/2023 11:05:56 INFO 	 IP Address: 192.168.10.50
    18/01/2023 11:05:56 INFO 	 User: UserTest
    18/01/2023 11:05:56 INFO 	 Directory: /Upload/Dir 
    18/01/2023 11:05:56 TRACE 	 uploading file via FTP protocol ... 
    18/01/2023 11:05:56 TRACE 	 File Uploaded Successfully in 0:00:00.016794! 
"""
def main():
    # Get Newest and Largest File
    with open('ftp_log.log', 'a') as wr:
        path = 'PATH TO FILES'
        output = ''

        filelist = search_newest_file(path)

        if len(filelist[0]) == 0:
            output = ''.join([
                '{} ERROR \t Something must be wrong, there are 0 new backups! \n'.format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")), 
                '{} ERROR \t Last backup on date {} \n'.format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), filelist[1]),
                '{} TRACE \t Email sent to <EMAIL WHO RECIEVE> \n'.format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")),
                '\n\n'
            ])
            error = 'CLIENT | ERROR TYPE'
            send_email('EMAIL WHO SENDS', 'PASSWORD', create_email('EMAIL WHO SENDS', 'EMAIL WHO RECIEVE', error, output))
            wr.write(output)
            exit()

        filename = max(filelist[0], key=lambda x: stat(x).st_size)

        # Start the FTP Process
        connection_status = open_ftp_connection(
            'DESTINATION IP ADDRESS',
            'PORT (as an int)',
            'FTP USER',
            'FTP PASSWORD',
            'FTP DESTINATION PATH',
            filename
        )

        output = "".join([
            '{} INFO \t File: {} \n'.format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), filename),
            '{} INFO \t File size (B): {} \n'.format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), stat(filename).st_size),
            connection_status
        ])

        wr.write(output)




if __name__ == '__main__':
    main()