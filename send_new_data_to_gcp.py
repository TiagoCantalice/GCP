import os
from google.cloud import storage
import datetime 

bucket_name = 'imagescantalicebucket'

list_files_gcp = []

client = storage.Client()

#Creating a list of blobs of gcp bucket
for blob in client.list_blobs(bucket_name):
    list_files_gcp.append(blob.name)

#files in folder
list_files_folder = os.listdir('files')

def new_files_in_folder(files_folder, files_cloud):
    return [blob for blob in list(set(files_folder+files_cloud)) if blob in files_folder and blob not in files_cloud]

print('files in folder: ', list_files_folder)
print('files in gcp:', list_files_gcp)

files_only_in_folder = new_files_in_folder(list_files_folder, list_files_gcp)
print('list of files only in folder:', files_only_in_folder)


print('Number of files to upload: {}\n'.format(len(files_only_in_folder)))


#Uploading files to gcp...
f = open('log_upload_files_gcp.txt', 'a+')

datenow = datetime.datetime.now() 
f.write('{} beginning of upload: {}\n'.format('#'*20, datenow))
f.write('------> {} files to upload\n'.format(len(files_only_in_folder)))
for idx, fl in enumerate(files_only_in_folder): 
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(fl)
    blob.upload_from_filename('files/'+fl)
    print('{} - {}'.format(idx, fl))
    f.write('{} - {}\n'.format(idx, fl))
f.close()
print('{} Upload finalizado!\n'.format('-'*10))
