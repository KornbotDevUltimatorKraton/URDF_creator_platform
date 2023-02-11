import json
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
from xml.dom import minidom
# Create the URDF structure using ElementTree
# Running the link in the loop to automate the link and joint generator and configure the matching part of the data 
mem_child_joint = {} # mem the child in joint position 
# Load the json and running the loop structure of the data from the json front-end to generate the back-end URDF inside the project directory file 
#Get this data from the fetcher in front-end command request 
#project_name_dir = "Joint_link_create_1_leg.json" # Get the project name dir data 
project_name_dir = "joint_fixed_test_2.json"
data_partss = open(project_name_dir,'r') #Get the total project name  
data_com = json.loads(data_partss.read()) # Get the json data parts load the json function into 
#Get the project name data of the model urdf
email = list(data_com)[0]   # Get the raw email data from the list
project_name = list(data_com.get(email))[0]
project_dir = list(data_com.get(email).get(project_name))[0]
# Get the 
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

#for joint_struct in datajoint:

#Joint part structure case here ...
tree = ET.ElementTree(robot)
# Write the XML to a file
xml_str = ET.tostring(robot)
reparsed = minidom.parseString(xml_str)
#Generate the urdf file data into the list 
with open(project_name_dir.split(".")[0]+".URDF", "w") as f:  
    f.write(reparsed.toprettyxml(indent="  "))


