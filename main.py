import os 
import json 
import base64
import requests 
import shutil 
from flask import Flask,render_template,url_for,redirect,jsonify,request 
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
from xml.dom import minidom
# Create the URDF structure u
user = os.listdir("/home/")[0] 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'
app.config['COMPONENTS_FOLDER'] = 'static/Robotics_parts'
user = os.listdir("/home/")[0] # Getting the user data 
Robot_part_file = {}
mem_child_joint = {} # get the mem child joint data 
project_files_list = {} #Get project list update in the system data to show in the front-end website 
list_proj_files = {} # Get the list project files data of the function 
removed_list = {} 

path_backup_status_local = "/home/"+str(user)+"/urdf_creator_template/static/Back_up_file_status/"
path_uploaded ="/home/"+str(user)+"/urdf_creator_template/static/Robotics_parts/" 
path_urdf_gen = "/home/"+str(user)+"/urdf_creator_template/static/urdf/"
project_path = "/home/"+str(user)+"/urdf_creator_template/"

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

def Re_rec():
        #Project file with project name data  
        try:
           
                project_list = open(project_path+"project_list_data.json",'r')
                proj_load = json.loads(project_list.read())
                for rtj in list(proj_load):
                          project_files_list[rtj] = proj_load[rtj] # Load the current project file data 
                for rtj in list(proj_load):
                    for ir in list(proj_load.get(rtj)):
                           print(ir,proj_load.get(rtj).get(ir))
                           #if datas.get(rtj).get(ir) not in current_list:  
                           if rtj not in list(list_proj_files):    
                               list_proj_files[rtj] = [proj_load.get(rtj).get(ir)]
                               if list_proj_files[rtj] != []:
                                    if proj_load.get(rtj).get(ir) not in list_proj_files[rtj]:
                                        list_proj_files[rtj].append(proj_load.get(rtj).get(ir))
                           if rtj in list(list_proj_files):
                                if list_proj_files[rtj] != []:             
                                     if proj_load.get(rtj).get(ir) not in list_proj_files[rtj]:
                                        list_proj_files[rtj].append(proj_load.get(rtj).get(ir))                          

        except:
            print("Error reading the file in the project list")


Re_rec()

def Write_project_list(project_files):
        try:
             proj_files = json.dumps(project_files) 
             write_proj = open(project_path+"project_list_data.json",'w')
             write_proj.write(proj_files) # Get the project files list data
        except:
             
             print("Project files list data")          

# Get the project list file of the data in json data list
@app.route("/create_urdf/<account_payload>",methods=['GET','POST']) # Add arguement of email and data of the project here 
def  index(account_payload):
     form = UploadFileForm()
     if form.validate_on_submit():
            file = form.file.data # First grab the file
            valid_file_type = ['zip'] #get the zip file dat from the back end 
            file_type = file.filename.split(".")[1]
            decoded_bytes = base64.b64decode(account_payload)
            decoded_string = decoded_bytes.decode("utf-8")
            print(decoded_string)
            emaildata = json.loads(decoded_string).get('email')            
            project_name = json.loads(decoded_string).get('project_name')
            print("Account_payload_record ",emaildata,project_name,file.filename.split(".")[0]) # Get the account payload data 
            
            if project_files_list == {} :
                       project_files_list[emaildata] = {project_name:file.filename.split(".")[0]} # Store the file name data in the list of dictionary for each project dynamically 
                       print(project_files_list) # Get the project files list data
                       Write_project_list(project_files_list) # Get the project files list 
            
            if project_files_list != {}:
                  # Check if the email dat exist inside the list of the project   
                  if emaildata in list(project_files_list):     
                         #currrent_project = project_files_list[emaildata] # Get the current project list data  
                         #currrent_project[project_name] = file.filename.split(".")[0]
                      try:   
                         recorded_proj = open(project_path+"project_list_data.json",'r')
                         current_project = json.loads(recorded_proj.read())
                         print("Current project update ",current_project) # Get the current project update 
                         current_project[emaildata][project_name] = file.filename.split(".")[0]
                         project_files_list[emaildata] = current_project[emaildata]  #Append the data of the current project file into the project list       
                         print("Current project files ",project_files_list) 
                         Write_project_list(project_files_list) # Get the project files list     
                      except:
                          print("Project files list")       
                  if emaildata not in list(project_files_list):
                         recorded_proj = open(project_path+"project_list_data.json",'r')
                         current_project = json.loads(recorded_proj.read())
                         current_project[emaildata] = {project_name:file.filename}
                         project_files_list[emaildata]  = current_project[emaildata] # Add the project linst the list incase the email not exist in the storation data 
                         print("Update new user project ",project_files_list)  
                         Write_project_list(project_files_list)
                         
            try:
               
               if file_type in valid_file_type:
                       file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['COMPONENTS_FOLDER'],secure_filename(file.filename))) # Then save the file  
                                 
            except:
                print("Remove project list data not found record")
            Re_rec()
     return render_template("index.html",form=form,component_profile=account_payload) 
@app.route("/project_files")
def project_record_upload():
         #print("Project files list ",project_files_list)
         #Re_rec()
         return jsonify(project_files_list)

@app.route("/project_data_files")
def project_files_rec_upload():
          return jsonify(list_proj_files)
@app.route("/Account_user_parts",methods=['GET','POST']) # Get the post request from the front end data 
def user_project_parts():
         input_part_dat = request.get_json(force=True) # get the parts 
         email = input_part_dat.get('email') 
         return jsonify(list_proj_files.get(email))
@app.route("/remove_project",methods=['GET','POST'])
def Remove_projects():
         remove_files = request.get_json(force=True) 
         #get the email and project name and directory name of the user data 
         #get the project_name 
         #Get directory of the project to remove data 
         #Structure of the file in json 
         email = remove_files.get('email')
         project_name = remove_files.get('project_name') # Get the project name data to clear the right info
         project_dir = remove_files.get('project_dir') 
         struct_remove = {email:[project_name,project_dir]}
         print(struct_remove)
         #os.remove(path_uploaded+project_dir+".zip") #
         if project_dir != '': 
               shutil.rmtree(path_urdf_gen+project_dir, ignore_errors=True)
               try:
                   project_list = open(project_path+"project_list_data.json",'r')
                   proj_load = json.loads(project_list.read())
                   list_proj_files[email].remove(project_dir)
                   print(list_proj_files)
                   del proj_load[email][project_name] 
                   project_files_list[email] =  proj_load[email]
                   print(project_files_list)
                   Write_project_list(project_files_list)

               except:
                   print("project file not in the list of the project index")             
         #Re_rec()        
         return jsonify(struct_remove) 
# Request the robot file from the project name 
@app.route("/robot_file_name",methods=['GET','POST'])
def Robots_file():
         input_robot_file = request.get_json() 
         email_project = input_robot_file.get('email') # Get the email from the front-end 
         project_names = input_robot_file.get('project_name') # Get the project name data
         project_dir = input_robot_file.get('project_dir') # Get the project dir data 

         try: 
            robot_files = os.listdir("/home/"+user+"/urdf_creator_template/static/urdf/"+str(project_dir)+"/meshes/") # Real path is static/Robots_parts use this as a real path data 
            robot_files_data = {'email':email_project,project_names:{project_dir:{'project_files':robot_files}}}
         except:
             print("Error no project directoy found")
         return jsonify(robot_files_data) 
@app.route("/model_color",methods=['GET','POST'])
def current_model_color():
           #fetch the link from the front-end data 
           input_color_model = request.get_json() # Getting the color json model of the selected model 
           '''
           {
            "colorhex": "#d20404",
            "email": "kornbot380@hotmail.com",
            "partname": "Body.stl",
            "project_name": "Atlete"
           }

           '''
           email_data = input_color_model.get('email') # get the email output data 
           part_name = input_color_model.get('partname') 
           project_name = input_color_model.get('project_name')
           colorhex = input_color_model.get('colorhex')
           #Check if the email user is exist inside the database of the current profile 
           #Data consist of email project_name part name and hex color to transfer into the new link                                                       
           #redirect the url to the current model selected 
           #redirect("http://0.0.0.0:5890/model_color/"+email_data+"/"+project_name+"/"+part_name+"/"+colorhex)  # redirect the link to the color and model part to create the current link and configure the current model in the link   
           
           return jsonify(input_color_model) #   

#Add the arguement in here to run the function of the colorized model data 
@app.route("/model_colors/<dataredirect>",methods=['GET','POST'])
def colorized_model(dataredirect):   
            #decode jwt here from the arguement added into the link 
            print(dataredirect)
            
            return render_template("model_color.html",data_direct=dataredirect) # add all arguments into the url link system 

@app.route("/robot_parts",methods=['GET','POST'])
def Robotics_parts():
        input_robot = request.get_json()
        email_data = input_robot.get('email') 
        project_name = input_robot.get('project_name')
        #using project_name directory of the urdf in the static as the base of the main project that will contain the meshes file and urdf directory inside 
        #project dir on server use /var/www/roboreactor/static/urdf
        #project zip on server user /var/www/roboreactor/static/urdf/ 
        
        #robot_files = os.listdir("/home/"+user+"/urdf_creator_template/static/urdf/T12/meshes/") # Real path is static/Robots_parts use this as a real path data      
        
        #robot_project_dir = os.listdir("/home/"+user+"/urdf_creator_template/static/urdf/")  #Share list of the file of the robot parts in the system 
        print("Robot part back_end request",input_robot) 
        #Inside the project name will contain the project name and file name that uploaded into the directory and updated data 
        #robot_files = os.listdir("/home/"+user+"/urdf_creator_template/static/urdf/T12/meshes/") # Real path is static/Robots_parts use this as a real path data      
        try:
             robot_project_dir = os.listdir("/home/"+user+"/urdf_creator_template/static/urdf/")  #Share list of the file of the robot parts in the system 
             Robot_dir = {email_data:{project_name:robot_project_dir}} # Get the project directory
        except:
            print("Error project not found") 
  
        return jsonify(Robot_dir)
#Get all the joint function on the system to 
def joint_function(robot,jointnames,joint_type,jointorigin_xyz,jointorigin_rpy,jointparent,jointchild,jointaxis,jointlimit_lower,jointlimit_upper,jointlimit_effort,jointlimit_velocity):
       joint_name = ET.SubElement(robot, "joint")  
       joint_name.set('name',jointnames)
       joint_name.set('type',joint_type)
       joint_origin = ET.SubElement(joint_name,'oringin') 
       joint_origin.set('xyz',jointorigin_xyz)
       joint_origin.set('rpy',jointorigin_rpy)
       joint_parent = ET.SubElement(joint_name,'parent')
       joint_parent.set('link',jointparent)
       joint_child = ET.SubElement(joint_name,'child')
       joint_child.set('link',jointchild) 
       joint_axis = ET.SubElement(joint_name,'axis')
       joint_axis.set('xyz',jointaxis)
       joint_limit = ET.SubElement(joint_name,'limit')
       joint_limit.set("lower",jointlimit_lower)
       joint_limit.set("upper",jointlimit_upper)
       joint_limit.set("effort",jointlimit_effort)
       joint_limit.set("velocity",jointlimit_velocity)

                
#for joint_struct in datajoint:
def joint_generator(robot,joint_part,joint_struct): 
       try:
              print(joint_struct) # Getting the joint struct in the data joint 
              data_joint = joint_part.get(joint_struct) 
              print(data_joint) # Get the joint data 
               
              joint_names = data_joint.get('name') # Get the joint name         
              jointypes = data_joint.get('type')  # Get the joint type  
              joint_origin = data_joint.get('origin')
              joint_origin_xyz = joint_origin.get('xyz')
              jx = joint_origin_xyz.get('x') 
              jy = joint_origin_xyz.get('y')
              jz = joint_origin_xyz.get('z')
              joint_origin_rpy = joint_origin.get('rpy')
              j_r = joint_origin_rpy.get('r')
              j_p = joint_origin_rpy.get('p')
              j_y = joint_origin_rpy.get('y')  
              parent_joint = data_joint.get('parent') # Parent joint   
              child_joint = data_joint.get('child') # Child joint 
              axis_joint = data_joint.get('axis').get('xyz') # axis joint 
              x_axis = axis_joint[0]
              y_axis = axis_joint[1]
              z_axis = axis_joint[2]
              limit_joint = data_joint.get('axis').get('limit') # limit joint data 
              lower_limit = limit_joint.get('lower') 
              upper_limit = limit_joint.get('upper')
              effort_limit = limit_joint.get('effort')
              velocity_limit = limit_joint.get('velocity') 
              joint_org_assem_xyz = str(jx)+" "+str(jy)+" "+str(jz)
              joint_org_assem_rpy = str(j_r)+" "+str(j_p)+" "+str(j_y)
              jointaxis= str(x_axis)+" "+str(y_axis)+" "+str(z_axis) 
              print(jointaxis,lower_limit,upper_limit,effort_limit,velocity_limit,joint_org_assem_xyz,joint_org_assem_rpy)
              joint_function(robot,joint_names,jointypes,joint_org_assem_xyz,joint_org_assem_rpy,parent_joint,child_joint,jointaxis,str(lower_limit),str(upper_limit),str(effort_limit),str(velocity_limit))
       except:
            print(joint_struct)
def URDF_generator(json_front_end):
           print("Start generating URDF ....")
           
           data_com = json_front_end
           email = list(data_com)[0]
           project_name = list(data_com.get(email))[0]
           project_dir = list(data_com.get(email).get(project_name))[0] 
           # Get the email joint and data list 
           link_part = data_com.get(email).get(project_name).get(project_dir).get('link')
           joint_part = data_com.get(email).get(project_name).get(project_dir).get('joint')
           datalist = list(link_part) # link part 
           datajoint = list(joint_part) # joint part 
           robot = ET.Element("robot")
           robot.set('name',project_name)
           for joint_struct in datajoint:
              print(joint_struct) # Getting the joint struct in the data joint 
              data_joint = joint_part.get(joint_struct) 
              print(joint_struct,data_joint.get('child')) # Get the joint data 
              mem_child_joint[data_joint.get('child')] = joint_struct # Generate the memdata of the child joint 
              #Get all the joint function on the system to 
           for part_struct in datalist:
                    print(part_struct,link_part.get(part_struct)) # Getting the link part 
                    data_parts = link_part.get(part_struct) 
                    #Inertial data 
                    #Origin data input  
                    print(list(data_parts.get('inertial')))
                    origin_data = data_parts.get('inertial').get('origin') # Get the origin data 
                    print("******************_Origin position_"+part_struct+"_***********************************")
                    print(origin_data)
                    x = origin_data.get('xyz').get('x')
                    y = origin_data.get('xyz').get('y')
                    z = origin_data.get('xyz').get('z') 
                    print('xyz',x,y,z)
                    r = origin_data.get('rpy').get('r') 
                    p = origin_data.get('rpy').get('p')
                    y = origin_data.get('rpy').get('y') 
                    print('rpy',r,p,y)
                    mass = data_parts.get('inertial').get('mass')
                    Mass = mass.get('value')
                    print("mass",Mass)
                    inertia = data_parts.get('inertial').get('inertia')
                    ixx = inertia.get('ixx_dat')
                    ixy = inertia.get('ixy_dat')
                    ixz = inertia.get('ixz_dat') 
                    iyy = inertia.get('iyy_dat') 
                    iyz = inertia.get('iyz_dat') 
                    izz = inertia.get('izz_dat')
                    print("inertia",ixx,ixy,ixz,iyy,iyz,izz)
                    #Collision data 
                    print("*****************_Collision data_"+part_struct+"_******************************************")
                    collision_data = data_parts.get('collision')
                    print(list(collision_data))
                    geometry = data_parts.get('collision').get('geometry')
                    print(geometry)
                    print(list(geometry))
                    file_name = geometry.get('mesh').get('filename')
                    print(file_name) 
                    origin_collision = geometry = data_parts.get('collision').get('origin')
                    print(origin_collision)
                    x0 = origin_collision.get('xyz').get('x')
                    y0 = origin_collision.get('xyz').get('y')
                    z0 = origin_collision.get('xyz').get('z') 
                    print('xyz',x0,y0,z0) 
                    r0 = origin_collision.get('rpy').get('r')
                    p0 = origin_collision.get('rpy').get('p')
                    y0 = origin_collision.get('rpy').get('y') 
                    print('rpy',r0,p0,y0)
                    #visual 
                    print("****************_Visual_data_"+part_struct+"_******************************")
                    visual_data = data_parts.get('visual')  # Visual _data 
                    print(visual_data)
                    print(list(visual_data))
                    print(" Visual origin")
                    visual_origin = visual_data.get('origin')
                    xv = visual_origin.get('xyz').get('x')
                    yv = visual_origin.get('xyz').get('y')
                    zv = visual_origin.get('xyz').get('z') 
                    print('xyz',xv,yv,zv)
                    rv = visual_origin.get('rpy').get('r') 
                    pv = visual_origin.get('rpy').get('p')
                    yv = visual_origin.get('rpy').get('y') 
                    print('rpy',rv,pv,yv)
                    print("Visual_color")
                    color_data = visual_data.get('color')
                    color_rgba = color_data.get('rgba')
                    colorvis = color_rgba.split(" ")
                    print(int(colorvis[0])/100,int(colorvis[1])/100,int(colorvis[2])/100,int(colorvis[3])) # Get the color data 
                    print("Visual_geometry")
                    visual_geo = visual_data.get('geometry') 
                    print(visual_geo)
                    print(list(visual_geo))
                    geometry_v = visual_geo.get('mesh').get('file_name')
                    print(geometry_v)

                    #Link part dat structure 
                    link = ET.SubElement(robot, "link")  
                    link.set('name',part_struct)  # using the list(link_parts)[i] data run in the loop 
                    inertial = ET.SubElement(link,'inertial') 
                    origin = ET.SubElement(inertial,'origin') 
                    origin.set('xyz',str(x)+" "+str(y)+" "+str(z))   # Change every number type of the data into the string 
                    origin.set('rpy',str(r)+" "+str(p)+" "+str(y))
                    mass = ET.SubElement(inertial,'mass') 
                    mass.set('value',str(Mass))
                    inertia = ET.SubElement(inertial,'inertia') 
                    #for the set data can be running in the loop to generate the raw data to the xml tree data 
                    #inertia data input 
                    inertia.set('ixx',str(ixx)) 
                    inertia.set('ixy',str(ixy))
                    inertia.set('ixz',str(ixz))
                    inertia.set('iyy',str(iyy))
                    inertia.set('iyz',str(iyz))
                    inertia.set('izz',str(izz))
                    #Visual element
         
                    visual = ET.SubElement(link,'visual') 
                    #Origin in visual 
                    origin2 = ET.SubElement(visual,'origin') 
                    origin2.set('xyz',str(x0)+" "+str(y0)+" "+str(z0))
                    origin2.set('rpy',str(r0)+" "+str(p0)+" "+str(y0))
                    geometry = ET.SubElement(visual,'geometry') 
                    mesh = ET.SubElement(geometry,'mesh')
                    mesh.set('filename',file_name)  # Load the body into the mesh data 
                    material = ET.SubElement(visual,'material')
                    material.set('name','')
                    color = ET.SubElement(material,'color') 
                    color_edit = color_rgba.split(" ")
                    color.set('rgba',str(int(color_edit[0])/100)+" "+str(int(color_edit[1])/100)+" "+str(int(color_edit[2])/100)+" "+"1")
                    collision = ET.SubElement(link,'collision')
                    origin3 = ET.SubElement(collision,'origin')
                    origin3.set('xyz',str(xv)+" "+str(yv)+" "+str(zv))
                    origin3.set('rpy',str(rv)+" "+str(pv)+" "+str(yv)) 
                    geometry2 = ET.SubElement(collision,'geometry')
                    mesh2 = ET.SubElement(geometry2,'mesh')
                    mesh2.set('filename',geometry_v)
                    joint_generator(mem_child_joint.get(part_struct))
           #Joint part structure case here ...
           tree = ET.ElementTree(robot)
           # Write the XML to a file
           xml_str = ET.tostring(robot)
           reparsed = minidom.parseString(xml_str)
           with open("first_generate.URDF", "w") as f:
                 f.write(reparsed.toprettyxml(indent="  "))
                          
@app.route("/generate_urdf_converter",methods=['GET','POST'])
def urdf_converter():
         structure_codes = request.get_json()
         email = list(structure_codes)[0]   # Get the raw email data from the list
         project_name = list(structure_codes.get(email))[0]
         project_dir = list(structure_codes.get(email).get(project_name))[0]
         link_part = structure_codes.get(email).get(project_name).get(project_dir).get('link')
         joint_part = structure_codes.get(email).get(project_name).get(project_dir).get('joint')
         datalist = list(link_part) # link part 
         datajoint = list(joint_part) # joint part
         print(datalist,datajoint) #Generate the files of the joint and the link  into the urdf data 
         robot = ET.Element("robot")
         robot.set('name',project_name)
         for joint_struct in datajoint:
              print(joint_struct) # Getting the joint struct in the data joint 
              data_joint = joint_part.get(joint_struct) 
              print(joint_struct,data_joint.get('child')) # Get the joint data 
              mem_child_joint[data_joint.get('child')] = joint_struct # Generate the memdata of the child joint 
         def joint_function(jointnames,joint_type,jointorigin_xyz,jointorigin_rpy,jointparent,jointchild,jointaxis,jointlimit_lower,jointlimit_upper,jointlimit_effort,jointlimit_velocity):
                   joint_name = ET.SubElement(robot, "joint")  
                   joint_name.set('name',jointnames)
                   joint_name.set('type',joint_type)
                   joint_origin = ET.SubElement(joint_name,'origin') 
                   joint_origin.set('xyz',jointorigin_xyz)
                   joint_origin.set('rpy',jointorigin_rpy)
                   joint_parent = ET.SubElement(joint_name,'parent')
                   joint_parent.set('link',jointparent)
                   joint_child = ET.SubElement(joint_name,'child')
                   joint_child.set('link',jointchild) 
                   joint_axis = ET.SubElement(joint_name,'axis')
                   joint_axis.set('xyz',jointaxis)
                   joint_limit = ET.SubElement(joint_name,'limit')
                   joint_limit.set("lower",jointlimit_lower)
                   joint_limit.set("upper",jointlimit_upper)
                   joint_limit.set("effort",jointlimit_effort)
                   joint_limit.set("velocity",jointlimit_velocity)
         #for joint_struct in datajoint:
         def joint_generator(joint_struct): 
          try:
              print(joint_struct) # Getting the joint struct in the data joint 
              data_joint = joint_part.get(joint_struct) 
              print(data_joint) # Get the joint data 
               
              joint_names = data_joint.get('name') # Get the joint name         
              jointypes = data_joint.get('type')  # Get the joint type  
              joint_origin = data_joint.get('origin')
              joint_origin_xyz = joint_origin.get('xyz')
              jx = joint_origin_xyz.get('x') 
              jy = joint_origin_xyz.get('y')
              jz = joint_origin_xyz.get('z')
              joint_origin_rpy = joint_origin.get('rpy')
              j_r = joint_origin_rpy.get('r')
              j_p = joint_origin_rpy.get('p')
              j_y = joint_origin_rpy.get('y')  
              parent_joint = data_joint.get('parent') # Parent joint   
              child_joint = data_joint.get('child') # Child joint 
              axis_joint = data_joint.get('axis').get('xyz') # axis joint 
              x_axis = axis_joint[0]
              y_axis = axis_joint[1]
              z_axis = axis_joint[2]
              limit_joint = data_joint.get('axis').get('limit') # limit joint data 
              lower_limit = limit_joint.get('lower') 
              upper_limit = limit_joint.get('upper')
              effort_limit = limit_joint.get('effort')
              velocity_limit = limit_joint.get('velocity') 
              joint_org_assem_xyz = str(jx)+" "+str(jy)+" "+str(jz)
              joint_org_assem_rpy = str(j_r)+" "+str(j_p)+" "+str(j_y)
              jointaxis= str(x_axis)+" "+str(y_axis)+" "+str(z_axis) 
              print(jointaxis,lower_limit,upper_limit,effort_limit,velocity_limit,joint_org_assem_xyz,joint_org_assem_rpy)
              joint_function(joint_names,jointypes,joint_org_assem_xyz,joint_org_assem_rpy,parent_joint,child_joint,jointaxis,str(lower_limit),str(upper_limit),str(effort_limit),str(velocity_limit))
          except:
            print(joint_struct)      
         for part_struct in datalist:
                print(part_struct,link_part.get(part_struct)) # Getting the link part 
                data_parts = link_part.get(part_struct) 
                #Inertial data 
                #Origin data input  
                print(list(data_parts.get('inertial')))
                origin_data = data_parts.get('inertial').get('origin') # Get the origin data 
                print("******************_Origin position_"+part_struct+"_***********************************")
                print(origin_data)
                x = origin_data.get('xyz').get('x')
                y = origin_data.get('xyz').get('y')
                z = origin_data.get('xyz').get('z') 
                print('xyz',x,y,z)
                r = origin_data.get('rpy').get('r') 
                p = origin_data.get('rpy').get('p')
                y = origin_data.get('rpy').get('y') 
                print('rpy',r,p,y)
                mass = data_parts.get('inertial').get('mass')
                Mass = mass.get('value')
                print("mass",Mass)
                inertia = data_parts.get('inertial').get('inertia')
                ixx = inertia.get('ixx_dat')
                ixy = inertia.get('ixy_dat')
                ixz = inertia.get('ixz_dat') 
                iyy = inertia.get('iyy_dat') 
                iyz = inertia.get('iyz_dat') 
                izz = inertia.get('izz_dat')
                print("inertia",ixx,ixy,ixz,iyy,iyz,izz)
                #Collision data 
                print("*****************_Collision data_"+part_struct+"_******************************************")
                collision_data = data_parts.get('collision')
                print(list(collision_data))
                geometry = data_parts.get('collision').get('geometry')
                print(geometry)
                print(list(geometry))
                file_name = geometry.get('mesh').get('filename')
                print(file_name) 
                origin_collision = geometry = data_parts.get('collision').get('origin')
                print(origin_collision)
                x0 = origin_collision.get('xyz').get('x')
                y0 = origin_collision.get('xyz').get('y')
                z0 = origin_collision.get('xyz').get('z') 
                print('xyz',x0,y0,z0) 
                r0 = origin_collision.get('rpy').get('r')
                p0 = origin_collision.get('rpy').get('p')
                y0 = origin_collision.get('rpy').get('y') 
                print('rpy',r0,p0,y0)
                #visual 
                print("****************_Visual_data_"+part_struct+"_******************************")
                visual_data = data_parts.get('visual')  # Visual _data 
                print(visual_data)
                print(list(visual_data))
                print(" Visual origin")
                visual_origin = visual_data.get('origin')
                xv = visual_origin.get('xyz').get('x')
                yv = visual_origin.get('xyz').get('y')
                zv = visual_origin.get('xyz').get('z') 
                print('xyz',xv,yv,zv)
                rv = visual_origin.get('rpy').get('r') 
                pv = visual_origin.get('rpy').get('p')
                yv = visual_origin.get('rpy').get('y') 
                print('rpy',rv,pv,yv)
                print("Visual_color")
                color_data = visual_data.get('color')
                color_rgba = color_data.get('rgba')
                colorvis = color_rgba.split(" ")
                print(int(colorvis[0])/100,int(colorvis[1])/100,int(colorvis[2])/100,int(colorvis[3])) # Get the color data 
                print("Visual_geometry")
                visual_geo = visual_data.get('geometry') 
                print(visual_geo)
                print(list(visual_geo))
                geometry_v = visual_geo.get('mesh').get('file_name')
                print(geometry_v)
                #Link part dat structure 
                link = ET.SubElement(robot, "link")  
                link.set('name',part_struct)  # using the list(link_parts)[i] data run in the loop 
                inertial = ET.SubElement(link,'inertial') 
                origin = ET.SubElement(inertial,'origin') 
                origin.set('xyz',str(x)+" "+str(y)+" "+str(z))   # Change every number type of the data into the string 
                origin.set('rpy',str(r)+" "+str(p)+" "+str(y))
                mass = ET.SubElement(inertial,'mass') 
                mass.set('value',str(Mass))
                inertia = ET.SubElement(inertial,'inertia') 
                #for the set data can be running in the loop to generate the raw data to the xml tree data 
                #inertia data input 
                inertia.set('ixx',str(ixx)) 
                inertia.set('ixy',str(ixy))
                inertia.set('ixz',str(ixz))
                inertia.set('iyy',str(iyy))
                inertia.set('iyz',str(iyz))
                inertia.set('izz',str(izz))
                #Visual element
                visual = ET.SubElement(link,'visual') 
                #Origin in visual 
                origin2 = ET.SubElement(visual,'origin') 
                origin2.set('xyz',str(x0)+" "+str(y0)+" "+str(z0))
                origin2.set('rpy',str(r0)+" "+str(p0)+" "+str(y0))
                geometry = ET.SubElement(visual,'geometry') 
                mesh = ET.SubElement(geometry,'mesh')
                mesh.set('filename',file_name)  # Load the body into the mesh data 
                material = ET.SubElement(visual,'material')
                material.set('name','')
                color = ET.SubElement(material,'color') 
                color_edit = color_rgba.split(" ")
                color.set('rgba',str(int(color_edit[0])/100)+" "+str(int(color_edit[1])/100)+" "+str(int(color_edit[2])/100)+" "+"1")
                collision = ET.SubElement(link,'collision')
                origin3 = ET.SubElement(collision,'origin')
                origin3.set('xyz',str(xv)+" "+str(yv)+" "+str(zv))
                origin3.set('rpy',str(rv)+" "+str(pv)+" "+str(yv)) 
                geometry2 = ET.SubElement(collision,'geometry')
                mesh2 = ET.SubElement(geometry2,'mesh')
                mesh2.set('filename',geometry_v)
                joint_generator(mem_child_joint.get(part_struct))
         #Joint part structure case here ...
         tree = ET.ElementTree(robot)
         # Write the XML to a file
         xml_str = ET.tostring(robot)
         reparsed = minidom.parseString(xml_str)
         #Generate the urdf file data into the list 
         with open(path_urdf_gen+project_dir+"/urdf/"+project_dir+".URDF", "w") as f:  
                 f.write(reparsed.toprettyxml(indent="  "))
         return jsonify(structure_codes) # Get the return structure code          
if __name__=="__main__":

        app.run(debug=True,threaded=True,host="0.0.0.0",port=5890)
   
