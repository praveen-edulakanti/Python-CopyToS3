# Praveen Edulakanti
# Joomla(Akeeba Plugin) taken backup to server location after that Copying Backup Files of entire website and db to S3 Bucket.

import datetime
import boto3
import os
import os.path

# Create an S3 client
S3 = boto3.client('s3')
BUCKET_NAME = 'praveen-websitedb-backups'

domains_list = { "0" : {
  "domain_name": "domain.com",
  "bucket_obj": "DomainName"  
},
"1" : {
  "domain_name": "domain1.com",
  "bucket_obj": "DomainName1"  
},
"2" : {
  "domain_name": "domain2.com",
  "bucket_obj": "DomainName2"  
},
"3" : {
  "domain_name": "domain3.com",
  "bucket_obj": "DomainName3"  
}


  
}

date_object = datetime.date.today()
dt_string = date_object.strftime("%Y%m%d")
#print("Todays Backup Date:", dt_string)
extSql = "sql" 
extZip = "zip"
for k,v in domains_list.items():
    domain_Sqlfilename = v['domain_name'] + "-" + dt_string +"." + extSql
    domain_Zipfilename = v['domain_name'] + "-" + dt_string +"." + extZip 
   
    SOURCE_FILENAME = '/var/www/vhosts/{0}/administrator/components/com_akeeba/backup/{1}'
    SourceFullPath = SOURCE_FILENAME.format(v['domain_name'], domain_Sqlfilename) #Sql Files
    SourceZipFullPath = SOURCE_FILENAME.format(v['domain_name'], domain_Zipfilename) #Complete backup Files and folders in zip

    #print(SourceFullPath)
    KeyStr = v['bucket_obj'] + "/" + domain_Sqlfilename
    KeyStrZip = v['bucket_obj'] + "/" + domain_Zipfilename
    #print(KeyStr)
    if os.path.isfile(SourceFullPath) and os.access(SourceFullPath, os.R_OK):
    #print "File exists and is readable"
     S3.upload_file(SourceFullPath, BUCKET_NAME, Key = KeyStr)
    if os.path.isfile(SourceZipFullPath) and os.access(SourceZipFullPath, os.R_OK):
    #print "File exists and is readable"
     S3.upload_file(SourceZipFullPath, BUCKET_NAME, Key = KeyStrZip)
