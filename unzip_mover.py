import os 
import json 
import threading
import shutil
import zipfile
from itertools import count # Count the loop iteration of the data inside the list of directory to unzip and move the directory file 
user = os.listdir("/home/")[0]
path_upload_server = "/var/www/"+str(user)+"/static/Robotics_parts/"
path_backup_status_server = "/var/www/"+str(user)+"/static/Back_up_file_status/"
path_backup_status_local = "/home/"+str(user)+"/urdf_creator_template/static/Back_up_file_status/"
path_uploaded ="/home/"+str(user)+"/urdf_creator_template/static/Robotics_parts/" 
path_urdf_gen = "/home/"+str(user)+"/urdf_creator_template/static/urdf/"
valid_file = ['zip']
meshes_check = ['meshes']
check_file = [] # Check the existing directory extracted in the list 
check_exten = [] #Check file extension
check_valid_file = {} # Checking the valid file 
#list_files = os.listdir(path_uploaded) # Check path uploaded 
#check the file in the loop and directory
#check_if_dir = os.path.isdir(path_uploaded)
#print(check_if_dir)
#def Extract_unzip():
for i in count(0): 
  list_files = os.listdir(path_uploaded) # Check path uploaded
  try: 
   for files in list_files:  
     if files.split(".")[0] not in os.listdir(path_urdf_gen): 
          #if files not in os.listdir(path_urdf_gen):       
          #Check the file extension  
          if check_exten != []: 
                     check_exten.clear() 
          files_length = files.split(".")
          if len(files_length) == 2:
               if files_length[1] in valid_file:
                    file_extracted = os.listdir(path_urdf_gen)
                    if files not in file_extracted:         
                       if files.split(".")[0] not in file_extracted: 
                          
                          with zipfile.ZipFile(path_uploaded+files, 'r') as zip_ref:
                                        zip_ref.extractall(path_uploaded)
                                        #check_file.append(files)  # append te file name that not exist in unzip file 
                          check_direct = os.path.isdir(path_uploaded+"/"+files_length[0]) # Runing the the data of the current directory of the file                                             
                          if check_direct == True:
                                    print("Checking the mesh file insider the directory")                 
                                    list_dir_meshes = os.listdir(path_uploaded+"/"+files_length[0])
                                    if list_dir_meshes[0] in meshes_check:
                                                list_files_inside = os.listdir(path_uploaded+"/"+files_length[0]+"/"+list_dir_meshes[0])               
                                                print(list_files_inside)
                                                #check if all are contain stl file  
                                                for file_exten in list_files_inside:
                                                         if file_exten.split(".")[1] == 'stl':
                                                               check_exten.append(file_exten.split(".")[1])
                                                if len(list_files_inside)  == len(check_exten):
                                                                 shutil.move(path_uploaded+files.split(".")[0],path_urdf_gen)                                                                                     
                                                                 check_valid_file[files] = "Valid_file_extracted"
                                                                 #Write json files for the file status on the system node and check valid file system
                                                                 #File_inserver mode    
                                                                 #files_status  = open(path_backup_status_server+"Backup_file_status.json",'w')
                                                                 #files_status.write(check_valid_file)  # Send the values
                                                                 files_status  = open(path_backup_status_local+"Backup_file_status.json",'w')
                                                                 files_status.write(json.dumps(check_valid_file))  # Send the values 
                                                                 print(check_valid_file)
                                                                 
                                                                 print("Writing the URDF file into the uploaded directory to path ",path_uploaded+files.split(".")[0]+"/urdf") 
                                                                 os.mkdir(path_urdf_gen+files.split(".")[0]+"/urdf",0o777)
                                                                 os.remove(path_uploaded+files) 
                                                if len(list_files_inside) != len(check_exten):
                                                           if len(check_exten) != 0: 
                                                                 check_valid_file[files] = "Has trouble shooting with "+str(len(list_files_inside)-len(check_exten))+" file extention inside"
                                                                 #Write json files for the file status on the system node and check valid file system
                                                                 #File_inserver mode    
                                                                 #files_status  = open(path_backup_status_server+"Backup_file_status.json",'w')
                                                                 #files_status.write(check_valid_file)  # Send the values
                                                                 files_status  = open(path_backup_status_local+"Backup_file_status.json",'w')
                                                                 files_status.write(json.dumps(check_valid_file))  # Send the values 
                                                                 print(check_valid_file," removing file from path "+path_uploaded+files+","+path_uploaded+files.split(".")[0])   
                                                                 os.remove(path_uploaded+files)
                                                                 shutil.rmtree(path_uploaded+files.split(".")[0], ignore_errors=True) 
                                                           if len(check_exten) == 0: 
                                                                 check_valid_file[files] = "Has no file extension match found"
                                                                 #Write json files for the file status on the system node and check valid file system
                                                                 #File_inserver mode    
                                                                 #files_status  = open(path_backup_status_server+"Backup_file_status.json",'w')
                                                                 #files_status.write(check_valid_file)  # Send the values
                                                                 files_status  = open(path_backup_status_local+"Backup_file_status.json",'w')
                                                                 files_status.write(json.dumps(check_valid_file))  # Send the values 
                                                                 print(check_valid_file," removing file from path "+path_uploaded+files+","+path_uploaded+files.split(".")[0])   
                                                                 os.remove(path_uploaded+files)
                                                                 shutil.rmtree(path_uploaded+files.split(".")[0], ignore_errors=True)         
                                                                                                                                     
  except:                                                        
                                          
       print("File is already exist!")                                                            
  
