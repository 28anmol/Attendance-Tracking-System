import time as t
from tkinter import *
from PIL import ImageTk, Image
import cv2
import face_recognition as fr
import numpy as np
import pickle
import mediapipe as mp
from datetime import date, datetime, time
import os



def exit():
    #"dummy function"
    pass


root = Tk()
root.title('AUTOLOGGER_ROBOTICS LABORATORY')
root.geometry('800x415')  #pixels
root.resizable(0,0)     #root.resizable(False, False) #basically height and width are false.
root.configure(background = '#42f5e6')
#root.protocol('WM_DELETE_WINDOW', exit)     #callback function. When u click [x] it executes exit function.

aspectratio = 1280.0/720.0

backbutton = ''
homeclick = ''
returnwindow = ''


image1 = Image.open("robopic.jpeg")     #   betterquality_robopic.jpeg
image1 = ImageTk.PhotoImage(image1.resize((250,250)))

image3 = Image.open("homebutton.jpg")   #   new_home_button.jpg
image3 = ImageTk.PhotoImage(image3.resize((35,35)))

settingphoto = PhotoImage(file = "settingslogo.png")    #   settings_logo.png
settingphotoimage = settingphoto.subsample(30,30)

loginphoto = PhotoImage(file = "loginlogo.png") #   loginslogo.png
loginphotoimage = loginphoto.subsample(8,8)

nextphoto = PhotoImage(file = "nextlogo.png")   #   nextlogo2.png
nextphotoimage = nextphoto.subsample(15,15)         

backphoto = PhotoImage(file = "backlogo.png")   #   backlogo.png
backphotoimage = backphoto.subsample(18,18)

createphoto = PhotoImage(file = "createuser.png")   #   create_user.png
createphotoimage = createphoto.subsample(6,6)

deletephoto = PhotoImage(file = "deleteuser.png")   #   delete_user.png
deletephotoimage = deletephoto.subsample(6,6)

otherphoto = PhotoImage(file = "autologgerparameters.png")  #   autologger_param.png
otherphotoimage = otherphoto.subsample(6,6)

adminphoto = PhotoImage(file = "adminloginlogo.png")    #   admin_login_logo.png
adminphotoimage = adminphoto.subsample(8,8)

clickphoto = PhotoImage(file = "cameraphoto.png")   #   Take_camera_photo.png
clickphotoimage = clickphoto.subsample(12,12)

aboutphoto = PhotoImage(file = "AboutUs.png")   #   AboutUs.png
aboutphotoimage = aboutphoto.subsample(8,8)

saveuserphoto = PhotoImage(file = "savefile.png")   #   savefile.png
saveuserphotoimage = saveuserphoto.subsample(12,12)

deleteuserphoto = PhotoImage(file = "deletefile.png")   #   deletefile.png
deleteuserphotoimage = deleteuserphoto.subsample(12,12)

activelogin = PhotoImage(file = "activelogins.png") #   active_logins.png
activeloginphotoimage = activelogin.subsample(8,8)

confirmlogin = PhotoImage(file = "loginconfirm.png")    #   login_confirm.png
confirmloginphotoimage = confirmlogin.subsample(8,8)

yespicsave = PhotoImage(file = "yesicon.png")   #   yesicon.png
yespicphotoimage = yespicsave.subsample(9,9)

nopicsave = PhotoImage(file = "noicon.png") #   noicon.png
nopicphotoimage = nopicsave.subsample(9,9)

archivesave = PhotoImage(file = "archive.png")  #   archive.png
archivephotoimage = archivesave.subsample(6,6)


loginmodetup = ['single','multiple']

labeltext1 = 'Features of Autonomous Attendance Logger'
feature0 = '1. Runs on 3 AI models: Face Detection, Face Recognition & Gesture Recognition.\n'
feature1 = '2. Login gesture: Thumbs Up.\n'                
feature2 = '3. Logout gesture: Thumbs Down.\n'
feature3 = '4. Gesture control works only when hand is inside the box.\n'
feature4 = '5. The gesture box turns green when hand is present inside else remains red.\n'
feature5 = '6. Login/Logout is successful only when the face is recognised and correct gesture is detected.\n'
feature6 = '7. Face recognition works for only one person at a time; not with a mask.\n'
labelauthor = 'Authors and Contributors'
labelauthorstr1 = 'This project is a work of bachelor thesis done by:\n'
labelname = 'Herr Anmol Singh\n'
labelstudyprogram = 'Mechatronic Systems Engineering(B.Sc.)\n'
labelfaculty = 'Faculty of Technology & Bionics\n'
labelthesissupervisor = 'Herr Prof. Dr. Ronny Hartanto(Technische Informatik)\n'
labelcosupervisor = 'Herr Prof. Dr. Matthias Krauledat(Informatik)\n'
labelguidance = 'Herr Mamen Thomas Chembakasseril(Mechanical Engineering, M.Sc.)\n'
labelplace = 'Robotics Laboratory, Rhine Waal University of Applied Sciences,Germany.\n'

global login_logout_flag
login_logout_flag = 0
global flag1
flag1 = -1
global flag2
flag2 = -1
global flag3
flag3 = -1
global flag5
flag5 = -1
global flag6
flag6 = -1
global projecttextfield2
global project_name
global username
username = ''
global userid
userid = ''
global userdefaultproject
userdefaultproject = ''
global confirm_login_logout_flag
confirm_login_logout_flag = 0
global face_login_logout_flag
face_login_logout_flag = 0
global projectstr
projectstr = ''
global default_project
default_project = ''


width = 640
height = 480

labopentime = time(hour = 6, minute = 0, second = 0, microsecond = 000000)

timedetails_fileexists = os.path.exists('autologger_timedetails.txt')
tempfile_fileexists =   os.path.exists('autologger_tempfile.txt')
logfile_fileexists =   os.path.exists('autologger_logfile.txt')

#Format: logintype,loginlogoutminduration,officehrval1(hr),officehrval2(min) - This is a default value.
if timedetails_fileexists == False:
    with open('autologger_timedetails.txt', 'w') as file:
            file.write(f'multiple,15,18,30')

if tempfile_fileexists == False:
    with open('autologger_tempfile.txt', 'w') as file:
        pass

if logfile_fileexists == False:
    with open('autologger_logfile.txt', 'w') as file:
        pass


#Load mediapipe frameworks
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

mp_face_detection = mp.solutions.face_detection


def facerecognitionfun(results,wid,hei):
    previousarea = 0
    y1, x2, y2, x1 = None, None, None, None

    if results.detections:
        for idx, detection in enumerate(results.detections):  
            xmin,ymin,width,height = detection.location_data.relative_bounding_box.xmin,detection.location_data.relative_bounding_box.ymin,detection.location_data.relative_bounding_box.width,detection.location_data.relative_bounding_box.height

            facearea = abs(width*height)

            if facearea>previousarea:
                previousarea = facearea
                y1, x2, y2, x1 = int(ymin * hei/4), (int(xmin * wid/4) + int(width * wid/4)), (int(ymin * hei/4) + int(height * hei/4)), int(xmin * wid/4)
    return y1, x2, y2, x1



def handgesturecontrol(imageframe):
        imgframe = cv2.cvtColor(imageframe, cv2.COLOR_BGR2RGB)
        results = hands.process(imgframe)

        if results.multi_hand_landmarks:

            hand_landmarks = results.multi_hand_landmarks[0]

            mp_drawing.draw_landmarks(imageframe,hand_landmarks, mp_hands.HAND_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color = (255,0,0), thickness =  2, circle_radius = 4),
                                    mp_drawing.DrawingSpec(color = (200,0,0), thickness =  2, circle_radius = 2))
            x0 = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x * width
            y0 = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * height
            y4 = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y * height

            y_arr = []
            for item in hand_landmarks.landmark:
                y_arr.append(item.y * height)
            y_arr.pop(4)
            y_numbers = np.array(y_arr)

            return y_numbers ,x0, y0, y4
        return None, None, None, None



def delete_item_button(mymenu):  #Remove particular entries from userdetails and faceencodings fil

    itemtodelete = mymenu.get()
    idno = itemtodelete.split(',')[0].strip('\n').strip(' ')

    user_file_exists_flag = os.path.exists('autologger_userdetails.txt')
    encode_file_exists_flag = os.path.exists('autologger_faceencodings.txt')

    if user_file_exists_flag and encode_file_exists_flag:
        with open('autologger_userdetails.txt','r') as file1:
            users = file1.readlines()
        with open('autologger_faceencodings.txt','rb') as file2:
            enclist = pickle.load(file2)


    with open('autologger_userdetails.txt','w') as file1:
        for line in users:
            if itemtodelete in line:
                file1.write('')
            else:
                file1.write(line)


    for idx,line in enumerate(enclist):
        if idno == line[0]:
            enclist.pop(idx)

    with open('autologger_faceencodings.txt','wb') as file2:
        pickle.dump(enclist,file2)
            

    delete_user_label.destroy()
    delete_button.destroy()
    archive_button.destroy()
    userlist.destroy()
    dropmenu.destroy()
    window4()



#Remove particular entries from userdetails and faceencodings and paste the same in archive file.
def archive_item_button(mymenu):

    itemtoarchive = mymenu.get()
    idno = itemtoarchive.split(',')[0].strip('\n').strip(' ')

    archive_file_exists_flag = os.path.exists('autologger_archive.txt')

    user_file_exists_flag = os.path.exists('autologger_userdetails.txt')
    encode_file_exists_flag = os.path.exists('autologger_faceencodings.txt')

    if user_file_exists_flag and encode_file_exists_flag:
        with open('autologger_userdetails.txt','r') as file1:
            users = file1.readlines()
        with open('autologger_faceencodings.txt','rb') as file2:
            enclist = pickle.load(file2)


    tobestored = []


    with open('autologger_userdetails.txt','w') as file1:
        for line in users:
            if itemtoarchive in line:
                tobestored.append(list(line))
                file1.write('')
            else:
                file1.write(line)

    for idx,line in enumerate(enclist):
        if idno == line[0]:
            tobestored[0].append(enclist.pop(idx))


    with open('autologger_faceencodings.txt','wb') as file2:
        pickle.dump(enclist,file2)

    locallist = []

    if archive_file_exists_flag:
        with open('autologger_archive.txt','rb') as filereading:
            locallist = pickle.load(filereading)
    
        with open('autologger_archive.txt','wb') as file3:
            locallist.append(tobestored)
            pickle.dump(locallist,file3)

    elif archive_file_exists_flag == False:
            with open('autologger_archive.txt','wb') as file3:
                pickle.dump(tobestored,file3)


    delete_user_label.destroy()
    delete_button.destroy()
    archive_button.destroy()
    userlist.destroy()
    dropmenu.destroy()
    window4()



def confirm_login(): 

    with open('autologger_timedetails.txt', 'r') as timefile:
        loclist = timefile.read()
    
    loginmode = loclist.split(',')[0].strip('\n').strip(' ')

    global confirm_login_logout_flag
    confirm_login_logout_flag = 1
    global login_logout_flag
    global face_login_logout_flag

    global projectstr
    global default_project
    projectstr = projecttextfield2.get()
    global currenttime
    global currentdate
    global flag1
    global flag2
    global flag3
    global flag5
    global flag6
    global project_name

    if login_logout_flag == 1 and face_login_logout_flag == 1:          #LOGIN

        if confirm_login_logout_flag == 1:

            if flag1 == 0 and flag2 == 1:

                if projectstr != '' and loginmode == 'single':
                    projecttextfield2.delete(0,END)
                    currentdate = datetime.now().date()
                    currenttime = datetime.now().time()
                    with open('autologger_tempfile.txt', 'a') as f:
                        f.write(f'{currentdate}: LOGIN, {name}, {currenttime}, {projectstr}\n')
                    with open('autologger_logfile.txt', 'a') as file:
                        file.write(f'{currentdate}: LOGIN, {name}, {currenttime}, {projectstr}\n')
                    login_logout_flag = 0
                    face_login_logout_flag = 0  
                elif projectstr != '' and loginmode == 'multiple':
                    currentdate = datetime.now().date()
                    currenttime = datetime.now().time()
                    projecttextfield2.delete(0,END)
                    with open('autologger_tempfile.txt', 'a') as f:
                        f.write(f'{currentdate}: LOGIN, {name}, {currenttime}, {projectstr}\n')
                    with open('autologger_logfile.txt', 'a') as file:
                        file.write(f'{currentdate}: LOGIN, {name}, {currenttime}, {projectstr}\n')
                    login_logout_flag = 0
                    face_login_logout_flag = 0
                elif projectstr == '' and loginmode == 'single':
                    currentdate = datetime.now().date()
                    currenttime = datetime.now().time()
                    projecttextfield2.delete(0,END)
                    with open('autologger_tempfile.txt', 'a') as f:
                        f.write(f'{currentdate}: LOGIN, {name}, {currenttime}, {default_project}\n')
                    with open('autologger_logfile.txt', 'a') as file:
                        file.write(f'{currentdate}: LOGIN, {name}, {currenttime}, {default_project}\n')
                    login_logout_flag = 0
                    face_login_logout_flag = 0
                elif projectstr == '' and loginmode == 'multiple':
                    currentdate = datetime.now().date()
                    currenttime = datetime.now().time()
                    projecttextfield2.delete(0,END)
                    with open('autologger_tempfile.txt', 'a') as f:
                        f.write(f'{currentdate}: LOGIN, {name}, {currenttime}, {default_project}\n')
                    with open('autologger_logfile.txt', 'a') as file:
                        file.write(f'{currentdate}: LOGIN, {name}, {currenttime}, {default_project}\n')
                    login_logout_flag = 0
                    face_login_logout_flag = 0
                else:
                    pass

    elif login_logout_flag == 2 and face_login_logout_flag == 1:        #LOGOUT

        if confirm_login_logout_flag == 1:

            if flag3 == 1 and flag5 == 0 and flag6 == 1:

                if projectstr != '' and loginmode == 'single':
                    currentdate = datetime.now().date()
                    currenttime = datetime.now().time()
                    projecttextfield2.delete(0,END)
                    with open('autologger_tempfile.txt', 'r') as f:
                        lineslist = f.readlines()
                    with open('autologger_tempfile.txt','w') as ff:
                        for line in lineslist:
                            if f'{currentdate}: LOGIN, {name},' in line.strip('\n'):
                                ff.write(f'{currentdate}: {name}\n')                           
                            else:
                                ff.write(line)
                    with open('autologger_logfile.txt', 'a') as fff:
                        fff.write(f'{currentdate}: LOGOUT, {name}, {currenttime}, {project_name}\n')
                    login_logout_flag = 0
                    face_login_logout_flag = 0

                elif projectstr != '' and loginmode == 'multiple':
                    currentdate = datetime.now().date()
                    currenttime = datetime.now().time()
                    projecttextfield2.delete(0,END)
                    with open('autologger_tempfile.txt', 'r') as f:
                        lineslist = f.readlines()

                    with open('autologger_tempfile.txt','w') as ff:
                        for line in lineslist:
                            if f'{currentdate}: LOGIN, {name},' in line.strip('\n'):
                                ff.write('')
                            else:
                                ff.write(line)

                    with open('autologger_logfile.txt', 'a') as fff:
                        fff.write(f'{currentdate}: LOGOUT, {name}, {currenttime}, {project_name}\n')
                    login_logout_flag = 0
                    face_login_logout_flag = 0

                elif projectstr == '' and loginmode == 'single':
                    currentdate = datetime.now().date()
                    currenttime = datetime.now().time()
                    projecttextfield2.delete(0,END)
                    with open('autologger_tempfile.txt', 'r') as f:
                        lineslist = f.readlines()
                    with open('autologger_tempfile.txt','w') as ff:
                        for line in lineslist:
                            if f'{currentdate}: LOGIN, {name},' in line.strip('\n'):
                                ff.write(f'{currentdate}: {name}\n')                           
                            else:
                                ff.write(line)
                    with open('autologger_logfile.txt', 'a') as fff:
                        fff.write(f'{currentdate}: LOGOUT, {name}, {currenttime}, {project_name}\n')
                    login_logout_flag = 0
                    face_login_logout_flag = 0

                elif projectstr == '' and loginmode == 'multiple':
                    currentdate = datetime.now().date()
                    currenttime = datetime.now().time()
                    projecttextfield2.delete(0,END)
                    with open('autologger_tempfile.txt', 'r') as f:
                        lineslist = f.readlines()

                    with open('autologger_tempfile.txt','w') as ff:
                        for line in lineslist:
                            if f'{currentdate}: LOGIN, {name},' in line.strip('\n'):
                                ff.write('')
                            else:
                                ff.write(line)

                    with open('autologger_logfile.txt', 'a') as fff:
                        fff.write(f'{currentdate}: LOGOUT, {name}, {currenttime}, {project_name}\n')
                    login_logout_flag = 0
                    face_login_logout_flag = 0

                else:
                    pass

    projectlabel2.destroy()
    projecttextfield2.destroy()
    confirmbutton.destroy()
    video.destroy()
    cap.release()
    cv2.destroyAllWindows()
    window1(image1)


def home():

    if backhomereturnbutton == 'window2':
        login_button.destroy()
        system_preferences_button.destroy()
        aboutus_button.destroy()
        active_login_button.destroy()
        window1(image1)

    elif backhomereturnbutton == 'window3':
        projectlabel2.destroy()
        projecttextfield2.destroy()
        confirmbutton.destroy()
        video.destroy()
        cap.release()
        cv2.destroyAllWindows()
        window1(image1)

    elif backhomereturnbutton == 'window4':
        create_user_button.destroy()
        delete_user_button.destroy()
        autologger_parameters_button.destroy()
        labelsetting.destroy()
        window1(image1)

    elif backhomereturnbutton == 'window5':
        global username
        username = ''
        global userid
        userid = ''
        global userdefaultproject
        userdefaultproject = ''
        facepicture.destroy()
        facepicturelabel.destroy()
        projecttextfield.destroy()
        projectlabel.destroy()
        matriculationtextfield.destroy()
        matriculationlabel.destroy()
        nametextfield.destroy()
        namelabel.destroy()
        user_label.destroy()
        emptylabel.destroy()
        save_button.destroy()
        window1(image1)

    elif backhomereturnbutton == 'window6':
        delete_user_label.destroy()
        delete_button.destroy()
        archive_button.destroy()
        userlist.destroy()
        dropmenu.destroy()
        window1(image1)

    elif backhomereturnbutton == 'window7':
        change_setting_label.destroy()
        logindur_label.destroy()
        officehr_label.destroy()
        loginmode_label.destroy()
        save_button2.destroy()
        emptylabel2.destroy()
        logintypespin.destroy()
        logindurspin.destroy()
        officehrspin.destroy()
        officeminspin.destroy()
        logindurtext.destroy()
        officehourtext.destroy()
        officeminutetext.destroy()  
        window1(image1)

    elif backhomereturnbutton == 'window8':
        if username != '' and userid != '' and userdefaultproject != '':
            username = ''
            userid = ''
            userdefaultproject = ''

        videolabel2.destroy()
        clickpic.destroy()
        cap2.release()
        cv2.destroyAllWindows()
        window1(image1)

    elif backhomereturnbutton == 'admin_password_window':
        passwordwidget.destroy()
        password_textfield.destroy()
        admin_login_button.destroy()
        window1(image1)

    elif backhomereturnbutton == 'about_software':
        heading1.destroy()
        text1.destroy()
        text2.destroy()
        heading2.destroy()
        window1(image1)
    
    elif backhomereturnbutton == 'active_users_window':
        active_users_label.destroy()
        active_users_listbox.destroy()
        scrollbar_listbox.destroy()
        window1(image1)
    
    elif backhomereturnbutton == 'window9':
        if username != '' and userid != '' and userdefaultproject != '':
            username = ''
            userid = ''
            userdefaultproject = ''
        surelabel.destroy()
        yesbutton.destroy()
        nobutton.destroy()
        labelpic.destroy()
        window1(image1)
        


def back():         #To go one page back

    if backhomereturnbutton == 'window2':
        login_button.destroy()
        system_preferences_button.destroy()
        aboutus_button.destroy()
        active_login_button.destroy()
        window1(image1)

    elif backhomereturnbutton == 'window3':
        projectlabel2.destroy()
        projecttextfield2.destroy()
        confirmbutton.destroy()
        video.destroy()
        cap.release()
        cv2.destroyAllWindows()
        window2()

    elif backhomereturnbutton == 'window4':
        create_user_button.destroy()
        delete_user_button.destroy()
        autologger_parameters_button.destroy()
        labelsetting.destroy()
        admin_password_window()

    elif backhomereturnbutton == 'window5':
        global username
        username = ''
        global userid
        userid = ''
        global userdefaultproject
        userdefaultproject = ''
        facepicture.destroy()
        facepicturelabel.destroy()
        projecttextfield.destroy()
        projectlabel.destroy()
        matriculationtextfield.destroy()
        matriculationlabel.destroy()
        nametextfield.destroy()
        namelabel.destroy()
        user_label.destroy()
        emptylabel.destroy()
        save_button.destroy()
        window4()

    elif backhomereturnbutton == 'window6':
        delete_user_label.destroy()
        delete_button.destroy()
        archive_button.destroy()
        userlist.destroy()
        dropmenu.destroy()
        window4()

    elif backhomereturnbutton == 'window7':
        change_setting_label.destroy()
        logindur_label.destroy()
        officehr_label.destroy()
        loginmode_label.destroy()
        save_button2.destroy()
        emptylabel2.destroy()
        logintypespin.destroy()
        logindurspin.destroy()
        officehrspin.destroy()
        officeminspin.destroy()
        logindurtext.destroy()
        officehourtext.destroy()
        officeminutetext.destroy()  
        window4()

    elif backhomereturnbutton == 'window8':
        videolabel2.destroy()
        clickpic.destroy()
        cap2.release()
        cv2.destroyAllWindows()
        window5()

    elif backhomereturnbutton == 'admin_password_window':
        passwordwidget.destroy()
        password_textfield.destroy()
        admin_login_button.destroy()
        window2()

    elif backhomereturnbutton == 'about_software':
        heading1.destroy()
        text1.destroy()
        text2.destroy()
        heading2.destroy()
        window2()

    elif backhomereturnbutton == 'active_users_window':
        active_users_label.destroy()
        active_users_listbox.destroy()
        scrollbar_listbox.destroy()
        window2()

    elif backhomereturnbutton == 'window9':
        surelabel.destroy()
        yesbutton.destroy()
        nobutton.destroy()
        labelpic.destroy()
        window8()



def yes(encodingimage):
    #Save format: matriculatioon nr, name, faceencodings in a list of lists.
    surelabel.destroy()
    yesbutton.destroy()
    nobutton.destroy()
    labelpic.destroy()

    global encode
    encode = fr.face_encodings(encodingimage)
    
    window5(encode)


def no():
    surelabel.destroy()
    yesbutton.destroy()
    nobutton.destroy()
    labelpic.destroy()
    window8()



def window9(imagefrencoding):
    videolabel2.destroy()
    clickpic.destroy()
    cap2.release()
    cv2.destroyAllWindows()

    global backhomereturnbutton
    backhomereturnbutton = 'window9'

    global surelabel
    surelabel = Label(root,text='Are you sure to save encodings for this picture?',font=('Arial',25),bg='#42f5e6')
    surelabel.pack()

    cvimage3 = cv2.cvtColor(imagefrencoding,cv2.COLOR_BGR2RGB)
    cvimage3 = cv2.resize(cvimage3,(300,300))
    img345 = Image.fromarray(cvimage3)

    imgtk3 = ImageTk.PhotoImage(image=img345)

    global labelpic
    labelpic = Label(root, image=imgtk3)
    labelpic.photo = imgtk3
    labelpic.pack()

    global yesbutton
    yesbutton = Button(root,command = lambda: yes(imagefrencoding),bg='#42f5e6', highlightbackground='black', image = yespicphotoimage, compound = LEFT,background='white')
    yesbutton.place(x = 519,y = 350)

    global nobutton
    nobutton = Button(root,command = no,bg='#42f5e6', highlightbackground='black', image = nopicphotoimage, compound = LEFT,background='white')
    nobutton.place(x = 225,y = 350)
    root.update()



def window8():

    global backhomereturnbutton
    backhomereturnbutton = 'window8'

    facepicture.destroy()
    facepicturelabel.destroy()
    projecttextfield.destroy()
    projectlabel.destroy()
    matriculationtextfield.destroy()
    matriculationlabel.destroy()
    nametextfield.destroy()
    namelabel.destroy()
    user_label.destroy()
    emptylabel.destroy()
    save_button.destroy()

    global clickpic
    clickpic = Button(root, text='Click Pic',command = lambda: window9(displayimg), font=('Arial',15),bg='#42f5e6', highlightbackground='black', image = clickphotoimage, compound = LEFT,background='white')
    clickpic.place(x = 620,y = 360)

    global videolabel2
    videolabel2 = Label(root)
    videolabel2.pack()

    global cap2
    cap2 = cv2.VideoCapture(0)
    width = cap2.get(3)
    height = cap2.get(4)

    t.sleep(1)

    with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection:

        while cap2.isOpened():
            ret,frame2 = cap2.read()
            
            frame2 = cv2.resize(frame2,(0,0),None,fx = 0.25,fy = 0.25)        #320,180
            img = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
            
            blazeface_location_results = face_detection.process(img)

            y1, x2, y2, x1 = facerecognitionfun(blazeface_location_results,width,height)
            livefeedlocation = [(y1,x2,y2,x1)]


            if livefeedlocation:
                y1,x2,y2,x1 = livefeedlocation[0]

                global newy1
                global newx2
                global newy2
                global newx1
                

                global fixedwidth
                global fixedheight
                global midpointx
                global midpointy

                fixedwidth = 100
                fixedheight = 100

                midpointx = (x1+x2)/2
                midpointy = (y1+y2)/2

                newy1,newx2,newy2,newx1 = int(midpointy - fixedheight/2),int(midpointx + fixedwidth/2),int(midpointy + fixedheight/2),int(midpointx - fixedwidth/2)

                displayimg = frame2[newy1:newy2,newx1:newx2]
                
                cv2.line(img,(x1,y1),(x1+5,y1),(255,255,0),2)
                cv2.line(img,(x1,y1),(x1,y1+5),(255,255,0),2)
                cv2.line(img,(x2,y1),(x2,y1+5),(255,255,0),2)
                cv2.line(img,(x2,y1),(x2-5,y1),(255,255,0),2)
                cv2.line(img,(x2,y2),(x2,y2-5),(255,255,0),2)
                cv2.line(img,(x2,y2),(x2-5,y2),(255,255,0),2)
                cv2.line(img,(x1,y2),(x1+5,y2),(255,255,0),2)
                cv2.line(img,(x1,y2),(x1,y2-5),(255,255,0),2)

                cvimage2 = cv2.resize(img, (int(aspectratio*350),350))
                img2 = Image.fromarray(cvimage2)
                imgtk2 = ImageTk.PhotoImage(image=img2)
                videolabel2.config(image = imgtk2)
                root.update()
            else:
                cvimage2 = cv2.resize(img, (int(aspectratio*350),350))
                img2 = Image.fromarray(cvimage2)
                imgtk2 = ImageTk.PhotoImage(image=img2)
                videolabel2.config(image = imgtk2)
                root.update()



def save_autologger_parameters(logtype,dura,office1,office2):

    logintypeval = logtype
    logindurval = dura
    officehrval1 = office1
    officehrval2 = office2
    

    #Format: logintype,loginduration,officehrval1(hr),officehrval2(min)
    with open('autologger_timedetails.txt', 'w') as file:
        file.write(f'{logintypeval},{logindurval},{officehrval1},{officehrval2}')
    
    with open('autologger_tempfile.txt', 'r') as f:
        lineslist = f.readlines()
    
    with open('autologger_tempfile.txt','w') as ff:
        for line in lineslist:
            if f'LOGIN' in line.strip('\n'):
                ff.write(line)                          
            else:
                ff.write('')
    
    

    change_setting_label.destroy()
    logindur_label.destroy()
    officehr_label.destroy()
    loginmode_label.destroy()
    save_button2.destroy()
    emptylabel2.destroy()
    logintypespin.destroy()
    logindurspin.destroy()
    officehrspin.destroy()
    officeminspin.destroy()
    logindurtext.destroy()
    officehourtext.destroy()
    officeminutetext.destroy()  
    window4()



def window7():        #Autologger_Parameters_window

    with open('autologger_timedetails.txt','r') as afile:
        listlocal = afile.read()
    
    val1 = listlocal.split(',')[0].strip('\n').strip(' ')
    val2 = int(listlocal.split(',')[1].strip('\n').strip(' '))
    val3 = int(listlocal.split(',')[2].strip('\n').strip(' '))
    val4 = int(listlocal.split(',')[3].strip('\n').strip(' '))

    my_var1 = StringVar()
    my_var2 = IntVar()
    my_var3 = IntVar()
    my_var4 = IntVar()

    global backhomereturnbutton
    backhomereturnbutton = 'window7'

    create_user_button.destroy()
    delete_user_button.destroy()
    autologger_parameters_button.destroy()
    labelsetting.destroy()

    global change_setting_label
    change_setting_label = Label(root, text='Change autologger settings',font=('Arial',30),bg='#42f5e6')
    change_setting_label.grid(row = 0, column = 2,sticky = E, columnspan = 2)

    global emptylabel2
    emptylabel2 = Label(root,bg='#42f5e6',width = 1)
    emptylabel2.grid(row = 1,column = 0)

    global logindur_label
    logindur_label = Label(root, text='Select login/logout duration: ',font=('Arial',25),bg='#42f5e6')
    logindur_label.grid(row = 2,column = 2, sticky = W)

    global officehr_label
    officehr_label = Label(root, text='Select office hours: ',font=('Arial',25),bg='#42f5e6')
    officehr_label.grid(row = 3,column = 2, sticky = W)

    global loginmode_label
    loginmode_label = Label(root, text='Select login mode: ',font=('Arial',25),bg='#42f5e6')
    loginmode_label.grid(row = 4,column = 2, sticky = W)

    global logintypespin
    logintypespin = Spinbox(root,values = loginmodetup,textvariable = my_var1,font=('Arial',15)) 
    logintypespin.grid(row = 4, column = 3,sticky = W)
    my_var1.set(val1)

    global logindurspin
    logindurspin = Spinbox(root,from_ = 5, to = 60, increment= 5,width = 5,textvariable = my_var2,font=('Arial',15))
    logindurspin.grid(row = 2, column = 3, sticky = W)
    my_var2.set(val2)

    global logindurtext 
    logindurtext = Label(root,text='min',font=('Arial',14),bg='#42f5e6')
    logindurtext.grid(row = 2, column = 3, sticky = W,padx = 80)

    global officehrspin
    officehrspin = Spinbox(root,from_= 6,to = 23, width = 5,textvariable = my_var3,font=('Arial',15))
    officehrspin.grid(row = 3, column = 3, sticky = W)
    my_var3.set(val3)

    global officehourtext 
    officehourtext = Label(root,text='hours',font=('Arial',14),bg='#42f5e6')
    officehourtext.grid(row = 3, column = 3, sticky = W,padx = 80)

    global officeminspin
    officeminspin = Spinbox(root,from_= 0, to = 59, width = 5,textvariable = my_var4,font=('Arial',15))
    officeminspin.grid(row = 3, column = 4, sticky = W)
    my_var4.set(val4)

    global officeminutetext 
    officeminutetext = Label(root,text='min',font=('Arial',14),bg='#42f5e6')
    officeminutetext.grid(row = 3, column = 4, sticky = W,padx = 80)

    global save_button2
    save_button2 = Button(root, text = 'Save', command = lambda: save_autologger_parameters(logintypespin.get(),logindurspin.get(),officehrspin.get(),officeminspin.get()), 
                          font = ('Arial',15),borderwidth=3,highlightbackground='black', image = saveuserphotoimage, compound = LEFT,background='white')
    save_button2.place(x = 660,y = 350)



def window6():      #Delete_User_window

    deletefilelist = []
    with open('autologger_userdetails.txt','r') as deletefile:
        deletefilelist = deletefile.read().splitlines()
    
    global backhomereturnbutton
    backhomereturnbutton = 'window6'

    global mymenu
    mymenu = StringVar()        #StringVar is treated globally.
    mymenu.set('----- Select Name -----')

    deletefilelist.insert(0,'----- Select Name -----')

    create_user_button.destroy()
    delete_user_button.destroy()
    autologger_parameters_button.destroy()
    labelsetting.destroy()

    global delete_user_label
    delete_user_label = Label(root, text='Select the user to delete/archive from the database',font=('Arial',22),bg='#42f5e6')
    delete_user_label.pack(side='top')

    global delete_button
    delete_button = Button(root, text = 'Delete',command = lambda: delete_item_button(mymenu), font = ('Arial',15),borderwidth=3,highlightbackground='black', image = deleteuserphotoimage, compound = LEFT,background='white')
    delete_button.place(x=650,y=350)

    global archive_button
    archive_button = Button(root, text = 'Archive',command = lambda: archive_item_button(mymenu), font = ('Arial',15),borderwidth=3,highlightbackground='black', image = archivephotoimage, compound = LEFT,background='white')
    archive_button.place(x=490,y=350)

    global userlist
    userlist = Label(root, text='Active User Database: ',font=('Arial',25),bg='#42f5e6')
    userlist.place(x = 100,y = 220)

    global dropmenu
    dropmenu = OptionMenu(root,mymenu,*deletefilelist)
    dropmenu.place(x = 440,y = 228,width = 350)



def createuser_save_button(encodeface):

    global username
    global userid
    global userdefaultproject


    checkflag1 = -1
    checkflag2 = -1
    readencodefacelist = []

    user_file_exists_flag = os.path.exists('autologger_userdetails.txt')
    encode_file_exists_flag = os.path.exists('autologger_faceencodings.txt')

    if user_file_exists_flag and encode_file_exists_flag:

        with open('autologger_userdetails.txt','r') as f:
            readuserlist = f.readlines()
            for line in readuserlist:
                if userid in line:
                    checkflag1 = 1
                    break
                else:
                    checkflag1 = 0

        with open('autologger_faceencodings.txt','rb') as fileread:
            readencodefacelist = pickle.load(fileread)
            for idx in range(len(readencodefacelist)):
                if userid == readencodefacelist[idx][0]:
                    checkflag2 = 1
                    break
                else: 
                    checkflag2 = 0


    if (user_file_exists_flag == False and encode_file_exists_flag == False) or (readencodefacelist == [] and readuserlist == []):
        checkflag1 = 0
        checkflag2 = 0


    if username != '' and userid != '' and userdefaultproject != '' and encodeface != None:   

        if checkflag1 == 0 and checkflag2 == 0:

            nametextfield.delete(0,END)
            matriculationtextfield.delete(0,END)
            projecttextfield.delete(0, END)

            with open('autologger_userdetails.txt','a') as file1:
                file1.write(f'{userid}, {username}, {userdefaultproject}\n')
            with open('autologger_faceencodings.txt','wb') as file2:
                readencodefacelist.append([userid, username, encodeface[0]])
                pickle.dump(readencodefacelist, file2)

            
            username = ''
            userid = ''
            userdefaultproject = ''
            
            facepicture.destroy()
            facepicturelabel.destroy()
            projecttextfield.destroy()
            projectlabel.destroy()
            matriculationtextfield.destroy()
            matriculationlabel.destroy()
            nametextfield.destroy()
            namelabel.destroy()
            user_label.destroy()
            emptylabel.destroy()
            save_button.destroy()
            window4()
        
        if checkflag1 == 1 and checkflag2 == 1:     #when userdetails exist already

            username = ''
            userid = ''
            userdefaultproject = ''

            nametextfield.delete(0,END)
            matriculationtextfield.delete(0,END)
            projecttextfield.delete(0, END)
            

def window5(encodeface=None):          #Create_User_window      #Default arguement is None.

    global username
    global userid
    global userdefaultproject


    global backhomereturnbutton
    backhomereturnbutton = 'window5'

    create_user_button.destroy()
    delete_user_button.destroy()
    autologger_parameters_button.destroy()
    labelsetting.destroy()
        
    my_str1 = StringVar()
    my_str2 = StringVar()
    my_str3 = StringVar()

    global user_label
    user_label = Label(root, text='Fill in for registering a new user',font=('Arial',30),bg='#42f5e6')
    user_label.grid(row = 0, column = 1, sticky = W, columnspan = 2)

    global emptylabel
    emptylabel = Label(root,bg='#42f5e6',width = 5)
    emptylabel.grid(row = 1, column = 0)

    global namelabel
    namelabel = Label(root, text='NAME: ',font=('Arial',25),bg='#42f5e6')
    namelabel.grid(row = 2, column = 1, sticky = W)

    global nametextfield
    nametextfield = Entry(root, width=35, borderwidth = 2, bg="white", fg = "black", textvariable = my_str1)
    nametextfield.grid(row = 2, column = 2, sticky = W)

    global matriculationlabel
    matriculationlabel = Label(root, text='MAT NR.: ', font=('Arial',25),bg='#42f5e6')
    matriculationlabel.grid(row = 3, column = 1, sticky = W)

    global matriculationtextfield
    matriculationtextfield = Entry(root, width=35, borderwidth = 2, bg="white", fg = "black", textvariable = my_str2)
    matriculationtextfield.grid(row = 3, column = 2, sticky = W)

    global projectlabel
    projectlabel = Label(root, text='PROJECT: ', font=('Arial',25),bg='#42f5e6')
    projectlabel.grid(row = 4, column = 1, sticky = W)

    global projecttextfield
    projecttextfield = Entry(root, width=35, borderwidth = 2, bg="white", fg = "black", textvariable = my_str3)
    projecttextfield.grid(row = 4, column = 2, sticky = W)

    global facepicturelabel
    facepicturelabel = Label(root, text='FACE PICTURE:  ', font=('Arial',25),bg='#42f5e6')
    facepicturelabel.grid(row = 5, column = 1, sticky = W)

    global facepicture
    facepicture = Button(root, text='Snap Picture',command = window8, font=('Arial',15),bg='#42f5e6', highlightbackground='black', image = clickphotoimage, compound = LEFT,background='white',state = 'disabled')
    facepicture.grid(row = 5, column = 2, sticky = W)

    global save_button
    save_button = Button(root, text = 'Save',command = lambda: createuser_save_button(encodeface), font = ('Arial',15),borderwidth=3,highlightbackground='black', image = saveuserphotoimage, compound = LEFT,background='white')
    save_button.place(x = 660, y = 350)


    def enablebutton(*kwargs):
        global username
        global userid
        global userdefaultproject

        if my_str1.get() != '' and my_str2.get() != ''  and my_str3.get() != '':
            username = my_str1.get()
            userid = my_str2.get()
            userdefaultproject = my_str3.get()
            facepicture.config(state = 'normal')
        else:
            facepicture.config(state = 'disabled')

    my_str3.trace('w', enablebutton)            #lambda func to pass arg to callback func- triggered by an event.       One observer for 3 fields is fine.

    if username != '' and userid != '' and userdefaultproject != '':
        my_str1.set(username)
        my_str2.set(userid)
        my_str3.set(userdefaultproject)



def window4():          #System_preferences_window

    global backhomereturnbutton
    backhomereturnbutton = 'window4'

    global backbutton
    backbutton = 'window4'

    global homeclick
    homeclick = 'window4'

    passwordwidget.destroy()
    password_textfield.destroy()
    admin_login_button.destroy()

    global create_user_button
    create_user_button = Button(root, text='Create User', font=('Arial',15),command = window5,bg='#42f5e6', highlightbackground='black', image = createphotoimage, compound = LEFT,background='white')
    create_user_button.place(x = 315, y = 60)

    global delete_user_button
    delete_user_button = Button(root, text='Delete User', font=('Arial',15),command = window6,bg='#42f5e6', highlightbackground='black', image = deletephotoimage, compound = LEFT,background='white')
    delete_user_button.place(x = 315, y = 180)

    global autologger_parameters_button
    autologger_parameters_button = Button(root, text='Autologger Parameters', font=('Arial',15),command = window7,bg='#42f5e6', highlightbackground='black', image = otherphotoimage, compound = LEFT,background='white')
    autologger_parameters_button.place(x = 280, y = 300)

    global labelsetting
    labelsetting = Label(root, text='System Preferences',font=('Arial',25),bg='#42f5e6')
    labelsetting.pack()


def active_users_window():

    login_button.destroy()
    system_preferences_button.destroy()
    aboutus_button.destroy()
    active_login_button.destroy()

    global backhomereturnbutton
    backhomereturnbutton = 'active_users_window'

    global active_users_label
    active_users_label = Label(root, text= 'Active Users in Robotics Laboratory',font=('Arial',25),bg='#42f5e6')
    active_users_label.pack()

    global scrollbar_listbox
    scrollbar_listbox = Scrollbar(root, orient = VERTICAL)
    scrollbar_listbox.place(x = 770,y = 40,height = 320)        #side = RIGHT, fill = BOTH

    global active_users_listbox
    active_users_listbox = Listbox(root,width = 70,height = 15,font=('Arial',13),yscrollcommand=scrollbar_listbox.set)
    active_users_listbox.place(x = 50, y = 40)


    with open('autologger_tempfile.txt','r') as f:
        datum = str(datetime.now().date())
        stat = "LOGIN"
        for line in f:
            if datum in line and stat in line:
                active_users_listbox.insert(END, str(line))

    scrollbar_listbox.config(command = active_users_listbox.yview)


def window3():          #Login_Page_Window      #Read about image and stuff. #default is 25 to 30fps. Need some kind of confirm button. Gesture,login and project satisfied then only press confirm. 

    with open('autologger_timedetails.txt', 'r') as timefile:
        loclist = timefile.read()
    
    loginmode = loclist.split(',')[0].strip('\n').strip(' ')
    loginmindur = int(loclist.split(',')[1].strip('\n').strip(' ')) * 60
    office1 = int(loclist.split(',')[2].strip('\n').strip(' '))
    office2 = int(loclist.split(',')[3].strip('\n').strip(' '))
    officehours = time(hour = office1, minute = office2, second = 0, microsecond = 000000)  

    with open('autologger_tempfile.txt','r') as f:
        readlist = f.readlines()


    with open('autologger_tempfile.txt','r+') as file:    #logout and clear file two different operations
        todays_date = datetime.now().date()


    #logging out after booting up for old dates.
        for line in file:
            if 'LOGIN' in line:

                datelog = line.split(',')[0].split(':')[0]
                logstatus = line.split(',')[0].split(':')[1].strip()
                namelog = line.split(',')[1].strip()
                projectnameauto = line.split(',')[3].strip('\n').strip()

                if datelog in line and logstatus in line: #login: 2022-06-01: LOGIN, ANMOLSINGH, 15:23:53.118805
                    if str(datelog) != str(todays_date) and str(logstatus) == 'LOGIN':
                        with open('autologger_logfile.txt','a') as secondfile:
                            secondfile.write(f'{datelog}: LOGOUT, {namelog}, {officehours}, {projectnameauto}\n')


    #Clearing the tempfile for old dates.
    with open('autologger_tempfile.txt','w') as ff:

        for line in readlist:
            datelog = line.split(',')[0].split(':')[0]

            if datelog != str(datetime.now().date()):
                ff.write('')           
            else:
                ff.write(line)

    
    #Load the facedatabase and encodedfacesdatabase files
    with open('autologger_faceencodings.txt', 'rb') as f:
        encodelistknownfaces = pickle.load(f)
    

    new_encodeface_list = []
    for item in range(len(encodelistknownfaces)):
        new_encodeface_list.append(encodelistknownfaces[item][2])
    
    global backhomereturnbutton
    backhomereturnbutton = 'window3'

    login_button.destroy()
    system_preferences_button.destroy()
    aboutus_button.destroy()
    active_login_button.destroy()

    global projectlabel2
    projectlabel2 = Label(root, text='PROJECT: ', font=('Arial',20),bg='#42f5e6')
    projectlabel2.place(x = 130,y = 363)

    global confirmbutton
    confirmbutton = Button(root, text='Confirm',command = confirm_login,font=('Arial',15), bg='#42f5e6',borderwidth=0,highlightbackground='black', image = confirmloginphotoimage, compound = RIGHT,background='white')
    confirmbutton.place(x = 648,y = 364)

    global projecttextfield2
    projecttextfield2 = Entry(root, width=35, borderwidth = 2, bg="white", fg = "black", state = 'disabled')
    projecttextfield2.place(x = 270,y = 370)

    global video
    video = Label(root)
    video.pack()

    global cap
    cap = cv2.VideoCapture(0)
    wid = cap.get(3)
    hei = cap.get(4)

    previoustime = t.time()     #Not zero
    global hands
    global projectstr
    global confirm_login_logout_flag
    global login_logout_flag
    global face_login_logout_flag
    global flag1
    global flag2
    global flag3
    global flag5
    global flag6
    global project_name
    y1, x2, y2, x1 = None, None, None, None
    counterframe = 0
    livefeedencoding = []
    global name
    name  = ''
    person_confirmed = False
    original_name = ''

    with mp_hands.Hands(model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence = 0.5)  as hands, mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection:

        while True:
            
            success, imageframe = cap.read()
            imageframe = cv2.flip(imageframe,1)

            #FPS calculation
            currenttimefps = t.time()
            fps = 1/(currenttimefps - previoustime)
            previoustime = currenttimefps

            resizedimg = cv2.resize(imageframe,(0,0),None, fx = 0.25, fy = 0.25)    #Resizes from 1280,720 to 320,180.     #Removes the lag all the way
            recoloredimg = cv2.cvtColor(resizedimg, cv2.COLOR_BGR2RGB)

            recoloredimg.flags.writeable = False
            blazeface_location_results = face_detection.process(recoloredimg)

            y1, x2, y2, x1 = facerecognitionfun(blazeface_location_results,wid,hei)
            livefeedlocation = [(y1,x2,y2,x1)]

            
            if x1 is None:
                name = ''
                person_confirmed = False

 
            cv2.putText(imageframe,f'FPS: {(fps)}',(10,40),cv2.FONT_HERSHEY_COMPLEX,0.6,(255,0,0),2)
            cv2.putText(imageframe,'Place any hand in the box!',(65,420),fontFace= cv2.FONT_HERSHEY_SIMPLEX,fontScale=0.6,color=(200,0,0),thickness = 2)
            cv2.putText(imageframe,'Hand gesture-control works, when wrist is inside the box',(10,20),fontFace= cv2.FONT_HERSHEY_SIMPLEX,fontScale=0.6,color=(200,0,0),thickness = 2)
            cv2.putText(imageframe,'Thumbs up: LOGIN!',(10,60),fontFace= cv2.FONT_HERSHEY_SIMPLEX,fontScale=0.6,color=(200,0,0),thickness = 2)
            cv2.putText(imageframe,'Thumbs down: LOGOUT!',(10,80),fontFace= cv2.FONT_HERSHEY_SIMPLEX,fontScale=0.6,color=(200,0,0),thickness = 2)

            cv2.line(imageframe,(100,200),(115,200),(0,0,255),3)
            cv2.line(imageframe,(100,200),(100,215),(0,0,255),3)
            cv2.line(imageframe,(300,200),(300,215),(0,0,255),3)
            cv2.line(imageframe,(300,200),(285,200),(0,0,255),3)
            cv2.line(imageframe,(100,400),(100,385),(0,0,255),3)
            cv2.line(imageframe,(100,400),(115,400),(0,0,255),3)
            cv2.line(imageframe,(300,400),(285,400),(0,0,255),3)
            cv2.line(imageframe,(300,400),(300,385),(0,0,255),3)
            
            if x1 and counterframe == 0 and (not person_confirmed):

                livefeedencoding = fr.face_encodings(recoloredimg,livefeedlocation)[0]   
                matches = fr.compare_faces(new_encodeface_list, livefeedencoding, tolerance = 0.5)     #Returns a list of true and false against all the encodings; one closest is true. /0.7 or 0.75
                facedistance = fr.face_distance(new_encodeface_list,livefeedencoding) #Returns a list of face distances against the whole of database. smallest one is true.
                matchindex = np.argmin(facedistance)        #Returns the index of the element of the database which is true for the picture.

                if matches[matchindex]:
                    name = encodelistknownfaces[matchindex][1].upper()
                    face_login_logout_flag = 1
                    original_name = encodelistknownfaces[matchindex][1]      
                    
                elif not matches[matchindex]:
                    name = 'Unknown'
                    
                counterframe +=1

            elif x1 and counterframe > 0 and counterframe < 3:

                matches = fr.compare_faces(new_encodeface_list, livefeedencoding, tolerance = 0.5)     #Returns a list of true and false against all the encodings; one closest is true. /0.7 or 0.75
                facedistance = fr.face_distance(new_encodeface_list,livefeedencoding) #Returns a list of face distances against the whole of database. smallest one is true.
                matchindex = np.argmin(facedistance)        #Returns the index of the element of the database which is true for the picture.

                if matches[matchindex]:
                    a_name = encodelistknownfaces[matchindex][1].upper()
                    original_name = encodelistknownfaces[matchindex][1]

                    if a_name == name:
                        person_confirmed = True
                    else:
                        counterframe = 0
                        name = ''

                elif not matches[matchindex]:
                    name = 'Unknown'
                    person_confirmed = True

                counterframe += 1

            elif x1 and (counterframe == 3 or person_confirmed):

                counterframe = 0

                if name == 'Unknown':
                    
                    person_confirmed = False

                    cv2.line(imageframe,(100,200),(115,200),(0,0,255),3)
                    cv2.line(imageframe,(100,200),(100,215),(0,0,255),3)
                    cv2.line(imageframe,(300,200),(300,215),(0,0,255),3)
                    cv2.line(imageframe,(300,200),(285,200),(0,0,255),3)
                    cv2.line(imageframe,(100,400),(100,385),(0,0,255),3)
                    cv2.line(imageframe,(100,400),(115,400),(0,0,255),3)
                    cv2.line(imageframe,(300,400),(285,400),(0,0,255),3)
                    cv2.line(imageframe,(300,400),(300,385),(0,0,255),3)

                    y1,x2,y2,x1 = livefeedlocation[0]

                    y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
                    cv2.rectangle(imageframe,(x1,y1),(x2,y2),(0,0,255),3)
                    cv2.putText(imageframe,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),2)
                    cv2.putText(imageframe,'Identity Mismatch!',(int(x1-20),int(y1-40)),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2)
                    cv2.putText(imageframe,'Unauthorized Robotics Lab Personnel',(int(x1-103),int(y1-20)),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2)


                else:
                    y1,x2,y2,x1 = livefeedlocation[0]
                    y_numbers, x0, y0, y4 = handgesturecontrol(imageframe)

                    y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4

                    cv2.rectangle(imageframe,(x1,y1),(x2,y2),(0,255,0),3)
                    cv2.putText(imageframe,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),2)
                    cv2.putText(imageframe,'Identity Verified',(int(x1+25),int(y1-40)),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),2)
                    cv2.putText(imageframe,'Authorized Robotics Lab Personnel',(int(x1-45),int(y1-20)),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),2)

                    with open('autologger_userdetails.txt', 'r') as readmefile:
                        global default_project
                        for item in readmefile:
                            if original_name in item:
                                default_project = item.split(',')[2].strip('\n').strip(' ')

                    if y0 != None:
                        if y0 < 400 and y0 > 200 and x0 > 100 and x0 < 300:

                            cv2.line(imageframe,(100,200),(115,200),(0,255,0),3)
                            cv2.line(imageframe,(100,200),(100,215),(0,255,0),3)
                            cv2.line(imageframe,(300,200),(300,215),(0,255,0),3)
                            cv2.line(imageframe,(300,200),(285,200),(0,255,0),3)
                            cv2.line(imageframe,(100,400),(100,385),(0,255,0),3)
                            cv2.line(imageframe,(100,400),(115,400),(0,255,0),3)
                            cv2.line(imageframe,(300,400),(285,400),(0,255,0),3)
                            cv2.line(imageframe,(300,400),(300,385),(0,255,0),3)

                            # Code block to log in the lab on any day
                            if (np.all(y_numbers>y4)):
                                
                                login_logout_flag = 1
                                cv2.putText(imageframe,"Login Gesture Detected",(20,300),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,0),2)

                                search_name = str(name)
                                search_date = str(datetime.now().date())
                                search_log_status = 'LOGIN'

                                with open('autologger_tempfile.txt', 'r') as f:
                                    flag1 = 0
                                    flag2 = 0

                                    if f:

                                        for line in f:
                                            word = line.split(':')[1].strip('\n').strip(' ').split(',')[0].strip('\n').strip(' ')
                                            if ((search_date in line and search_name in line and search_log_status in line) or (search_name == word)):
                                                flag1 = 1
                                                break

                                    if flag1 == 0:
                                        if (datetime.now().time() > labopentime and datetime.now().time() < officehours):
                                            flag2 = 1

                                        if flag2 == 1:
                                            projecttextfield2.config(state = 'normal')
                                            cv2.putText(imageframe,"Login Successful!",(200,460),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,0),2)
                                            currentdate = datetime.now().date()
                                            currenttime = datetime.now().time()
                                        elif flag2 == 0:
                                            cv2.putText(imageframe,"Lab is closed! Can't Login!",(200,460),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,0),2)

                                    elif flag1 == 1:
                                        pass

                                
                            # Code block to log out of the lab on any day.
                            elif (np.all(y_numbers<y4)):
                                login_logout_flag = 2
                                cv2.putText(imageframe,"Logout Gesture Detected",(20,300),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)
                                search_name = str(name)
                                search_date = str(datetime.now().date())
                                search_log_statusone = 'LOGIN'


                                with open('autologger_tempfile.txt', 'r') as f:
                                    flag3 = 0
                                    flag5 = 0
                                    flag6 = 0

                                    for line in f:
                                        if search_date in line and search_name in line and search_log_statusone in line:
                                            flag3 = 1
                                            user_login_time = datetime.strptime(line.split(',')[2].strip('\n').strip(' ').split('.')[0], '%H:%M:%S').time()
                                            final_time = datetime.combine(date.today(), user_login_time)
                                            project_name = line.split(',')[3].strip('\n').strip(' ')
                                            break

                                    if flag3 == 0:
                                        cv2.putText(imageframe,"Please Login First!",(200,460),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)

                                    elif flag3 == 1:

                                            if (datetime.now().time() > officehours):
                                                flag5 = 1

                                            if flag5 == 0:
                                                
                                                global logouttime, timediff
                                                logouttime = datetime.now()
                                                timediff = logouttime - final_time
                                                if timediff.seconds > loginmindur:
                                                    flag6 = 1
                                                
                                                if flag6 == 1:

                                                    if loginmode == 'single':

                                                        cv2.putText(imageframe,"Logout Successful!",(200,460),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)
                                                        currentdate = datetime.now().date()
                                                        currenttime = datetime.now().time()

                                                    elif loginmode == 'multiple':
                                                        cv2.putText(imageframe,"Logout Successful!",(200,460),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)
                                                        currentdate = datetime.now().date()
                                                        currenttime = datetime.now().time()
            
                                                    else:
                                                        pass
    
                                                elif flag6 == 0:
                                                    cv2.putText(imageframe,"Can't Logout right now!",(200,460),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,0,255),2)
 

            cvimage = cv2.cvtColor(imageframe,cv2.COLOR_BGR2RGBA)        #alpha channel for png - numpy array this image
            cvimage = cv2.resize(cvimage, (int(aspectratio*350),350))
            img = Image.fromarray(cvimage)
            imgtk = ImageTk.PhotoImage(image=img)
            video.config(image = imgtk)
            root.update()



def about_software():

    login_button.destroy()
    system_preferences_button.destroy()
    aboutus_button.destroy()
    active_login_button.destroy()

    global backhomereturnbutton
    backhomereturnbutton = 'about_software'

    global heading1
    heading1 = Label(root, text = labeltext1, font = ('Arial',18),bg='#42f5e6')
    heading1.pack()

    global text1
    text1 = Text(root, font = ('Arial',11), height = 8,bg='#ffff80')
    text1.insert(INSERT,feature0)
    text1.insert(INSERT,feature1)
    text1.insert(INSERT,feature2)
    text1.insert(INSERT,feature3)
    text1.insert(INSERT,feature4)
    text1.insert(INSERT,feature5)
    text1.insert(INSERT,feature6)
    text1.pack()

    global heading2
    heading2 = Label(root, text = labelauthor, font = ('Arial',20),bg='#42f5e6')
    heading2.pack()

    global text2
    text2 = Text(root, font = ('Arial',11), height = 8, width = 70,bg='#ffff80')
    text2.insert(INSERT,labelauthorstr1)
    text2.insert(INSERT,'Name: '+labelname)
    text2.insert(INSERT,'Study Program: '+labelstudyprogram)
    text2.insert(INSERT,'Faculty: '+labelfaculty)
    text2.insert(INSERT,'Thesis Supervisor: '+labelthesissupervisor)
    text2.insert(INSERT,'Thesis Co-supervisor: '+labelcosupervisor)
    text2.insert(INSERT,'Guided By: '+labelguidance)
    text2.insert(INSERT,'Place: '+labelplace)
    text2.pack()



def admin_verification():
    password = '05eg025'
    user_pass = str(password_textfield.get())
    if user_pass == password:
        password_textfield.delete(0, END)
        window4()
    else:
        password_textfield.delete(0, END)



def admin_password_window():

    login_button.destroy()
    system_preferences_button.destroy()
    aboutus_button.destroy()
    active_login_button.destroy()

    global backhomereturnbutton
    backhomereturnbutton = 'admin_password_window'

    global passwordwidget
    passwordwidget = Label(root, text='Please Enter Admin Password',font=('Arial',20),bg='#42f5e6')
    passwordwidget.pack()

    global password_textfield
    password_textfield = Entry(root, width=30, borderwidth = 2, bg="white", fg = "black", show ='*')
    password_textfield.place(x = 170,y = 220)

    global admin_login_button
    admin_login_button = Button(root, text='Admin Login', font=('Arial',15),command=admin_verification, bg='#42f5e6', highlightbackground='black', image = adminphotoimage, compound = LEFT,background='white')
    admin_login_button.place(x = 460,y = 205)



def window2():          #Main_Utilities_Window

    with open('autologger_timedetails.txt', 'r') as timefile:
        loclist = timefile.read()
    
    office1 = int(loclist.split(',')[2].strip('\n').strip(' '))
    office2 = int(loclist.split(',')[3].strip('\n').strip(' '))
    officehours = time(hour = office1, minute = office2, second = 0, microsecond = 000000)  

    with open('autologger_tempfile.txt','r') as f:
        readlist = f.readlines()


    with open('autologger_tempfile.txt','r+') as file:    #logout and clear file two different operations
        todays_date = datetime.now().date()
        momentstime = datetime.now().time()


    #logging out after booting up for old dates.
        for line in file:
            if 'LOGIN' in line:

                datelog = line.split(',')[0].split(':')[0]
                logstatus = line.split(',')[0].split(':')[1].strip()
                namelog = line.split(',')[1].strip()
                projectnameauto = line.split(',')[3].strip('\n').strip()

                if datelog in line and logstatus in line: #login: 2022-06-01: LOGIN, ANMOLSINGH, 15:23:53.118805, Autologger
                    if str(datelog) != str(todays_date) and str(logstatus) == 'LOGIN':
                        with open('autologger_logfile.txt','a') as secondfile:
                            secondfile.write(f'{datelog}: LOGOUT, {namelog}, {officehours}, {projectnameauto}\n')


    #Clearing the tempfile for old dates.
    with open('autologger_tempfile.txt','w') as ff:

        for line in readlist:
            datelog = line.split(',')[0].split(':')[0]

            if datelog != str(datetime.now().date()):
                ff.write('')           
            else:
                ff.write(line)


    label0.destroy()
    label1.destroy()
    button1.destroy()
    labeltext.destroy()  

    global backhomereturnbutton
    backhomereturnbutton = 'window2'

    global login_button 
    login_button = Button(root, text = 'User Login/Logout', font = ('Arial',15), command = window3,borderwidth=3,highlightbackground='black', image = loginphotoimage, compound = LEFT, background = 'white')
    login_button.place(x = 290,y = 100)

    global system_preferences_button
    system_preferences_button  = Button(root, text = 'System Preferences', font = ('Arial',15), command = admin_password_window, borderwidth = 3, highlightbackground='black', image = settingphotoimage, compound = LEFT, background = 'white')
    system_preferences_button.place(x = 280,y = 200)

    global aboutus_button
    aboutus_button = Button(root, text = 'About Autonomous Attendance Logger', font = ('Arial',15),command = about_software,borderwidth=3,highlightbackground='black', image = aboutphotoimage, compound = LEFT,background='white')
    aboutus_button.place(x = 200,y = 305)

    global active_login_button
    active_login_button = Button(root, text = 'Active Users',command = active_users_window,font = ('Arial',15),borderwidth=3,highlightbackground='black', image = activeloginphotoimage, compound = LEFT,background='white')
    active_login_button.place(x = 320,y = 10)


def window1(img):           #Welcome_Page_Window

    global backhomereturnbutton
    backhomereturnbutton = 'window1'

    global label0
    label0 = Label(root, image=img, bg = '#42f5e6')
    label0.pack()

    global label1
    label1 = Label(root, text='WELCOME TO ROBOTICS LABORATORY', font=('Arial',25),bg='#42f5e6')
    label1.pack()

    global labeltext 
    labeltext = Label(root, text='Hi, this is your autonomous attendance logger', font=('Arial',20),bg='#42f5e6')
    labeltext.place(x=110,y= 310)

    global button1
    button1 = Button(root, text='Next', font=('Arial',15),command=window2, bg='#42f5e6',borderwidth=0,highlightbackground='black', image = nextphotoimage, compound = RIGHT,background='white')
    button1.place(x = 690,y = 372)

home_button = Button(root, image = image3, command = home, bg='#42f5e6',
                    highlightbackground='black',highlightthickness=1, fg = 'black', background='#42f5e6')
home_button.place(x = 0,y = 0)


button2 = Button(root, text='Back', font=('Arial',15),command = back,bg='#42f5e6', highlightbackground='black', image = backphotoimage, compound = LEFT,background='white')
button2.place(x = 4,y = 370)

if __name__ == '__main__':
    window1(image1)
    root.mainloop()
