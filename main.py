import pw_generator,datetime
from tkinter import *
import tkinter.ttk as ttk 
from ttkthemes import ThemedStyle
class Interface():
    def __init__(self, master, title, screen_width, screen_height):
        
        # initializes foundation of window
        self.gui = master
        self.title = self.gui.title(title)
        self.screen_width = int(screen_width)
        self.screen_height = int(screen_height)
        #self.size = self.gui.geometry(str(self.screen_width) + "x" + str(self.screen_height))
        
        # Password Manager Interface
        self.password_gen = Password_save(self.gui)
        self.create_password_button = Button(self.gui, text="generate Password", command=self.password_gen.generate_pw_window)
        self.create_password_button.grid(column=0,row=0)
        
        

    def update_content(self):
        # Password related stuff
        self.gui.after(1000, self.update_content)
        
        
        
class Password_save():
    
    def __init__(self,master):
        self.gui = master
        
        self.pw_li = Listbox(self.gui)
        self.password_list = self.loadPwList(load_content("pw_save.txt"))
        self.pw_li.grid(column=2,row=0,columnspan=3, rowspan=3,sticky=E)
        self.updatePwList()
        
        self.configure_pw_button = Button(self.gui, text="configure",command=self.managePw)
        self.configure_pw_button.grid(column=2,row=4,sticky=W)
        
        self.delete_pw_button = Button(self.gui,text="delete",command=self.deletePw)
        self.delete_pw_button.grid(column=3,row=4,sticky=E)
        

    #updates the Password List in the Interface by reading every key from the loadPwList()
    def updatePwList(self):
        self.password_list = self.loadPwList(load_content("pw_save.txt"))
        li = load_content("pw_save.txt")
        print("LIST",li)
        self.pw_li.delete(0,'end')
        for key in self.password_list:
            self.pw_li.insert(END,key)   

    # reads the pw_save.txt and puts the alias name as key and the pw as value in a dict
    def loadPwList(self,input):
        dict = {}
        list = [x for x in input.split("\n") if x != ""]
        print("DICTR LISTR",list)
        
        for item in list:
            name = item.split(":")[0] 
            pw = item.split(":")[1]

            dict[name] = pw 
        print("DICT",dict)    
        return dict   
    
    def managePw(self):
        selected = self.pw_li.get(self.pw_li.curselection())
        self.password_list = self.loadPwList(load_content("pw_save.txt"))
        
        self.configure_tab = Toplevel()
        self.configure_tab.geometry("300x100")
        focusWindow(self.configure_tab)
        frame = Frame(self.configure_tab)
        frame.pack()
        to_be_edited_name = None

        
        # Gets password from selected alias name in list
        show_pw_label = Label(frame,text="Password: ")
        show_pw_label.grid(column = 0, row=2)
        for key in self.password_list:
            if key == selected:
                self.show_pw = Text(frame,width=20,height=1)
                self.show_pw.grid(column = 1, row=2)
                self.show_pw.insert(END,self.password_list[key])
                to_be_edited_name = key

        edit_alias_label  = Label(frame,text="Alias Name: ")
        edit_alias_label.grid(column = 0, row=1)
        self.edit_alias = Text(frame, width=20,height=1)
        self.edit_alias.grid(column = 1, row=1)
        self.edit_alias.insert(END,to_be_edited_name)

        
        self.save_pw_button = Button(self.configure_tab, text="Save",command= lambda: self.overridePw(to_be_edited_name))
        self.save_pw_button.pack(pady= 10)

        
               
    def overridePw(self,program_name):
        self.password_list = self.loadPwList(load_content("pw_save.txt"))
        content = [x for x in load_content("pw_save.txt").split("\n") if x != ""]
        password = self.show_pw.get("1.0",END).replace("\n","")
        alias_name = self.edit_alias.get("1.0",END).replace("\n","")

        output = ''

        for line in content:

            if program_name in line:
                if alias_name == program_name:
                    output +=  "\n" + alias_name + ":" + password + "\n"
                else:
                    if alias_name in self.password_list:
                        popUpWindow(alias_name + " already exists in password list")
                        output += line + "\n"
                    else:
                        output +=  "\n" + alias_name + ":" + password + "\n" 
            else:
                output += line + "\n"
        f = open("pw_save.txt","w")
        f.write(output)
        f.close()
        self.updatePwList()
        close_window(self.configure_tab)

    def deletePw(self):
        content = [x for x in load_content("pw_save.txt").split("\n") if x != ""]
        selected = self.pw_li.get(self.pw_li.curselection())
        output = ''

        for line in content:
            if selected not in line:
                output += line + "\n"

        f = open("pw_save.txt","w")
        f.write(output)
        f.close()
        print("OUTUT",output)
        self.updatePwList()

    # Calls process() of pw_generator.py and generates a password
    def generatePassword(self):
        
        try:
            self.pw_length =  int(self.pw_length_entry.get())    
        except:
            self.generated_pw_label.delete("1.0", END)
            self.generated_pw_label.insert(END,"Invalid password length")
            return
        self.custom_words = self.custom_words_entry.get()
            
        # calls pw_generator.py and starts the generating process
        pw = pw_generator.PasswordSettings(self.pw_length,self.custom_words)
        generated_pw = pw.process()
        
        # Deletes old password and replaces it with new generated
        self.generated_pw_label.delete("1.0", END)
        self.generated_pw_label.insert(END,generated_pw)
        
        return generated_pw
    
    # Create Window to save password and add properties
    def generate_pw_window(self):
        window_width = 382
        window_height = 300
        
        # Set up base window for password process
        gen_window = Toplevel()
        focusWindow(gen_window)
        gen_window.geometry(str(window_width) + "x" + str(window_height))


        # Set up programm, where password is used 
        programm_name_label = Label(gen_window,text="Alias Name: ")
        programm_name_label.grid(column=0,row=1,sticky=W,pady = 20)
        self.programm_name_entry = Entry(gen_window)
        self.programm_name_entry.grid(column=1,row=1,sticky=E)
        
        # Set up length entry for password
        pw_length_label = Label(gen_window,text="Length of password: ")
        pw_length_label.grid(column=0,row=2,sticky=W,pady = 20)
        self.pw_length_entry = Entry(gen_window)
        self.pw_length_entry.grid(column=1,row=2,sticky=E)
        
        # Allows to type in custom words in your pw (seperate words by comma)
        custom_words_label = Label(gen_window,text="Type in custom words to be in your password\nseperated by comma: ")
        custom_words_label.grid(column=0,row=3,sticky=W,pady = 20)
        self.custom_words_entry = Entry(gen_window)
        self.custom_words_entry.grid(column=1,row=3,sticky=E)
        
        # Starts generating process of password
        
        self.save_pw_button = Button(gen_window, text="Save password",command=self.savePW)
        self.save_pw_button.grid(column=1,row=6,sticky=E)
        
        generate_pw_button = Button(gen_window, text="Generate password",command=self.generatePassword)
        generate_pw_button.grid(column=0,row=6,sticky=W,pady=20)
        
        self.generated_pw_label = Text(gen_window,height=1,width=47)
        self.generated_pw_label.grid(column=0,row=5,columnspan=2)
        self.generated_pw_label.insert(END,"")
        
    def savePW(self):
        program_name = self.programm_name_entry.get()
        pw = self.generated_pw_label.get(1.0,END)
        
        popup = Toplevel()
        popup.focus_set()
        popup.grab_set()
        popup.geometry("200x50")
        popup.resizable(0,0)
        
        
        if program_name != "":
            if len(pw) <= 1:
                popup_message = Label(popup,text="ERROR: NO PASSWORD GENERATED")
                popup_message.pack()  
            else:
                self.updatePwList()
                if program_name not in self.password_list:
                    save_content = program_name + ":" + pw
                    pw_generator.save(save_content)
                    popup_message = Label(popup,text="saved")
                    popup_message.pack()
                    self.updatePwList()
                else:
                    popup_message = Label(popup,text="PROGRAM NAME ALREADY USED")  
                    popup_message.pack()    
                
        
        else:
            popup_message = Label(popup,text="ERROR: ALL FIELDS ARE REQUIRED")  
            popup_message.pack()


def popUpWindow(input_txt):
    popup = Toplevel()
    focusWindow(popup)
    popup.geometry("200x50")
    popup.resizable(0,0)
    popup_text = Label(popup, text=input_txt)
    popup_text.pack()

                 
def load_content(filename):
    try:
        content = ''
        f = open(filename,"r")
        for line in f:
            content += line 
        return content
        
    except:
        print("ERROR: COULD NOT LOAD FILE CONTENT")
        return "ERROR: COULD NOT LOAD FILE CONTENT"    
        
def focusWindow(window):
    window.focus_set()
    window.resizable(0,0)
    window.grab_set()

def close_window(window):
        window.destroy()   

def main():
    root = Tk()
    main_gui = Interface(root,"pySave PW Manager",300,600)
    root.after(1000,main_gui.update_content)
    root.mainloop() 


if __name__ == "__main__":
    main()