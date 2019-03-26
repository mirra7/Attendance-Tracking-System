SET log_file=%cd%\logfile.txt
call C:\Users\Mirra\Anaconda3\Scripts\activate.bat
activate tensorflow
python Cap_Login.py  > %log_file%