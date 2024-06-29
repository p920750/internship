from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
import tkinter.simpledialog as sd
import mysql.connector as mysql


mycon=mysql.connect(host="localhost",user="root",password="root",database="library")
if mycon.is_connected():
    print("success")
cur=mycon.cursor()


root=Tk()
root.title("Library Management System")
root.iconbitmap('./icond.ico')
root.geometry("1000x500+400+100")
root.resizable(False,False)
backimage = PhotoImage(file="welcomim.png") 
Label(root,text='Library Management System',font=("Bookman old style",20,"bold","italic","underline"),bg="orange",fg="white").pack(side=TOP,fill=X)

bkid=StringVar()
bkname=StringVar()
author=StringVar()
status=StringVar()
cardid=StringVar()
v1=IntVar()


def clear():
    bkid.set('')
    bkname.set('')
    author.set('')
    e1.focus_set()

def sel():
    if v1.get() == 0:
        status.set("Available")
    else:
        status.set("Issued")
   
    
def save():
    global status,cardid,bkid,bkname,author,cur,mycon

    if bkid.get()=='' or bkname.get()=='' or author.get()=='':
        msgbox.showinfo("message","Please enter the details")
    elif status.get()=='Issued':
        msgbox.showinfo("message","Please enter available books only")
    else:
        cardid.set("N/A")
        s="insert into bookentry values(%s,'%s','%s','%s','%s')" %(bkid.get(),bkname.get(),author.get(),status.get(),cardid.get())
        cur.execute(s)
        mycon.commit()
        msgbox.showinfo("message","Record saved")
        tree.insert('','end',values=(bkid.get(),bkname.get(),author.get(),status.get(),cardid.get()))
        clear()

def display():
    tree.delete(*tree.get_children())
    s="Select * from bookentry"
    cur.execute(s)
    data=cur.fetchall()
    for i in data:
        print(i)
        tree.insert('','end',values=i)

def issuer_card():
	Cid = sd.askstring('Issuer Card ID', 'What is the Issuer\'s Card ID?\t\t\t')

	if not Cid:
		msgbox.showerror('Issuer ID cannot be zero!', 'Can\'t keep Issuer ID empty, it must have a value')
	else:
		return Cid

def update_record():
    def update():
        if status.get()=='Issued':
            cardid.set(issuer_card())
        else:
            cardid.set('N/A')
        s="update bookentry set bkname='%s',author_name='%s',status='%s',cardid='%s' where bkid=%s" %(bkname.get(),author.get(),status.get(),cardid.get(),bkid.get())
        cur.execute(s)
        mycon.commit()
        clear()
        edit.destroy()
        e1.config(state='normal')
        b2.config(state='normal')
        display()
        msgbox.showinfo('Done', 'The record updated successfully')
    if not tree.selection():
        msgbox.showerror('Error!', 'Please select an item from the database')
        msgbox.showinfo("message",'click display button')
        return
    current_item = tree.focus()
    values = tree.item(current_item)
    selection = values["values"]
    s="Select * from bookentry where bkid=%s" %(selection[0],)
    cur.execute(s)
    data=cur.fetchone()
    if len(data)>0:
        bkid.set(data[0])
        bkname.set(data[1])
        author.set(data[2])
        status.set(data[3])
    e1.config(state='disabled')
    b2.config(state='disabled')    
    edit = Button(lt_frame, text='Update Record', font=("Bookman old style",12,"bold"),width=27,fg="#cc6600", command=update)
    edit.place(x=75, y=370)


def delete():
    if not tree.selection():
        msgbox.showerror('Error!', 'Please select an item from the database')
        return
    current_item = tree.focus()
    values = tree.item(current_item)
    selection = values["values"]
    a="delete from bookentry where bkid=%s" %(selection[0],)
    cur.execute(a)
    mycon.commit()
    tree.delete(current_item)
    msgbox.showinfo('Done', 'The record you wanted deleted was successfully deleted.')





lt_frame=Frame(root,bg="light blue",relief="solid").place(x=0,y=35,width=400,height=500)
rt_frame=Frame(root,bg="#ffbb33").place(x=400,y=35,width=600,height=400)             
btm_frame=Frame(root,bg="orange").place(x=400,y=435,width=600,height=65)

backimage1 = PhotoImage(file="welcomim.png") 
Label(lt_frame,image=backimage1 ).place(width=400, height=500,x=0,y=35)  
Label(lt_frame,text="Book ID: ",font=("Bookman old style",18,"bold"),fg="white", bg="orange").place(x=50,y=50)
e1=Entry(lt_frame,width=25,text=bkid,font=("Bookman old style",14,"bold"),bg="light yellow")
e1.place(x=30,y=90)
Label(lt_frame,text="Book Name: ",font=("Bookman old style",18,"bold"),fg="white",bg="orange").place(x=50,y=130)
Entry(lt_frame,width=25,text=bkname,font=("Bookman old style",14,"bold"),bg="light yellow").place(x=30,y=170)
Label(lt_frame,text="Author Name: ",font=("Bookman old style",18,"bold"),fg="white",bg="orange").place(x=50,y=210)
Entry(lt_frame,width=25,text=author,font=("Bookman old style",14,"bold"),bg="light yellow").place(x=30,y=250)
Label(lt_frame,text="Book status: ",font=("Bookman old style",18,"bold"),fg="white",bg="orange").place(x=50,y=290)



r1= Radiobutton(lt_frame, text="Available",variable=v1, value=0, command=sel).place(x=120, y= 340)
r2= Radiobutton(lt_frame, text="Issued",variable= v1, value=1,command=sel ).place(x=250, y= 340)

Button(lt_frame,text="Submit",font=("Bookman old style",12,"bold"),fg="#cc6600",width=10, command=save).place(x=75,y=370)
b2=Button(lt_frame,text="Clear",font=("Bookman old style",12,"bold"),fg="#cc6600",width=10, command=clear)
b2.place(x=250,y=370)

Label(rt_frame,text="Book Inventory",font=("Times New Roman",14,"bold"),bg="#ffbb33",fg="white").pack(side=TOP)

tree = ttk.Treeview(rt_frame, selectmode=BROWSE,columns=('ID', 'Name', 'Author', 'Status', 'Issuer Card ID'))
tree.heading('ID', text='Book ID', anchor=CENTER)
tree.heading('Name', text='Book Name', anchor=CENTER)
tree.heading('Author', text='Author', anchor=CENTER)
tree.heading('Status', text='Status of the Book', anchor=CENTER)
tree.heading('Issuer Card ID', text='Card ID of the Issuer', anchor=CENTER)
tree.column('#0', width=0, stretch=NO)
tree.column('#1', width=50, stretch=NO)
tree.column('#2', width=70, stretch=NO)
tree.column('#3', width=150, stretch=NO)
tree.column('#4', width=105, stretch=NO)
tree.column('#5', width=132, stretch=NO)
tree.place(y=65, x=400, height=370, width=600)

Button(btm_frame,text="Display",font=("Bookman old style",12,"bold"),width=10,fg="#cc6600", command=display).place(x=410,y=440)
Button(btm_frame,text="Delete Record",font=("Bookman old style",12,"bold"),width=10,fg="#cc6600", command= delete).place(x=640,y=440)
Button(btm_frame,text="Update Record",font=("Bookman old style",12,"bold"),width=10,fg="#cc6600",command=update_record).place(x=870,y=440)


root.mainloop()
