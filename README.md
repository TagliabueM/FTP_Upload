# FTP Upload

## Description

This is a program to upload files from a local to a remote directory using the FTP protocol

## Output Example

### Success

```txt
    18/01/2023 11:05:56 INFO     File: path\\file
    18/01/2023 11:05:56 INFO 	 File size (B): 121
    18/01/2023 11:05:56 INFO 	 IP Address: 192.168.10.50
    18/01/2023 11:05:56 INFO 	 User: UserTest
    18/01/2023 11:05:56 INFO 	 Directory: /Upload/Dir 
    18/01/2023 11:05:56 TRACE 	 uploading file via FTP protocol ...
    18/01/2023 11:05:56 TRACE 	 File Uploaded Successfully in 0:00:00.016794!
```

### Failure

```txt
    10/03/2023 09:38:34 ERROR 	 Something must be wrong, there are 0 new backups!
    10/03/2023 09:38:34 ERROR 	 Last backup on date 2023-03-07 13:25:09.505993
    10/03/2023 09:38:34 TRACE 	 Email sent to email@domain.com
```
