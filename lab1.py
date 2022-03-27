from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter import filedialog
import pickle
import vocabularylib as vl

root=Tk()
vocabulary = []

#==================================INPUT FRAME===========================================================================
space0 = Label(root,text='\n')
inputFrame=Frame(root,bg='grey',bd=5)
inputText=Text(inputFrame,height=15,width=130,wrap=WORD)
createVocabularyButton=Button(inputFrame,text='Create vocabulary from text',width=55,height=2,bg='green')
orLabel=Label(inputFrame,text=' Or',width=35,height=2,bg='grey',fg='white')
openVocabularyButton=Button(inputFrame,text='Open vocabulary from file',width=55,height=2,bg='blue')

#==================================VOCABULARY FRAME======================================================================
space1 = Label(root,text='\n')
vocabularyFrame=Frame(root,bg='grey',bd=5)
vocabularyTree=ttk.Treeview(vocabularyFrame, columns=("Lemma", "Part of speech", "Endings"), selectmode='browse', height=11)
vocabularyTree.heading('Lemma', text="Lemma", anchor=W)
vocabularyTree.heading('Part of speech', text="Part of speech", anchor=W)
vocabularyTree.heading('Endings', text="Endings", anchor=W)
vocabularyTree.column('#0', stretch=NO, minwidth=0, width=0)
vocabularyTree.column('#1', stretch=NO, minwidth=347, width=347)
vocabularyTree.column('#2', stretch=NO, minwidth=347, width=347)
vocabularyTree.column('#3', stretch=NO, minwidth=347, width=347)
saveButton=Button(vocabularyFrame,text='Save vocabulary to file',width=55,height=2,bg='green')
orLabel2=Label(vocabularyFrame,text=' Or',width=35,height=2,bg='grey',fg='white')
clearButton=Button(vocabularyFrame,text='Clear vocabulary',width=55,height=2,bg='red')

#==================================ADDING, EDITING, DELETING FRAME======================================================================
space2=Label(root,text='\n')
addingFrame=Frame(root,bg='grey',bd=5)
lemmaAddingLabel=Label(addingFrame,text=' Lemma: ',width=10,height=2,bg='grey',fg='white')
lemmaAddingEntry=Entry(addingFrame,width=23)
posAddingLabel=Label(addingFrame,text=' Part of speech: ',width=14,height=2,bg='grey',fg='white')
posAddingEntry=Entry(addingFrame,width=23)
endingsAddingLabel=Label(addingFrame,text=' Endings: ',width=10,height=2,bg='grey',fg='white')
endingsAddingEntry=Entry(addingFrame,width=23)
space21=Label(addingFrame,text='          ', bg='grey')
addButton=Button(addingFrame,text='Add',width=5,height=2,bg='green')
editButton=Button(addingFrame,text='Edit selected',width=11,height=2,bg='green')
formsButton=Button(addingFrame,text='Create all forms of selected',width=22,height=2,bg='green')
deleteButton=Button(addingFrame,text='Delete selected',width=14,height=2,bg='red')

#==================================FUNCTIONS================================================================================
rows = 0

def showVocabulary():
	global rows
	rows = 0
	vocabularyTree.delete(*vocabularyTree.get_children())
	for lexeme in vocabulary:
		vocabularyTree.insert('', 'end', values=(lexeme.lemma, lexeme.part_of_speech, lexeme.endings), iid=rows)
		rows += 1

def createVocabulary():
	global vocabulary
	vocabulary = vl.create_vocabulary_from_text(inputText.get('1.0', END))
	vocabulary.sort()
	showVocabulary()
	
def openVocabulary():
	global vocabulary
	file_path = filedialog.askopenfilename()
	if file_path != "":
		f = open(file_path, 'rb')
		vocabulary = pickle.load(f)
		f.close()
		showVocabulary()
	
def saveVocabulary():
	file_path = filedialog.asksaveasfilename()
	if file_path != "":
		f = open(file_path, 'wb')
		pickle.dump(vocabulary, f)
		f.close()
		
def clearVocabulary():
	global rows, vocabulary
	rows = 0
	vocabulary = []
	vocabularyTree.delete(*vocabularyTree.get_children())

def addVocabulary():
	if lemmaAddingEntry.get() != "" and posAddingEntry.get() != "":
		vocabulary.append(vl.Lexeme(lemmaAddingEntry.get(), posAddingEntry.get(), endingsAddingEntry.get()))
		vocabulary.sort()
		showVocabulary()

def editVocabulary():
	if vocabularyTree.selection() != () and lemmaAddingEntry.get() != "" and posAddingEntry.get() != "":
		vocabulary[int(vocabularyTree.selection()[0])] = vl.Lexeme(lemmaAddingEntry.get(), posAddingEntry.get(), endingsAddingEntry.get())
		vocabulary.sort()
		showVocabulary()
	
def deleteVocabulary():
	if vocabularyTree.selection() != ():
		del vocabulary[int(vocabularyTree.selection()[0])]
		vocabulary.sort()
		showVocabulary()
	
def formsVocabulary():
	if vocabularyTree.selection() != ():
		messagebox.showinfo("Forms", vl.create_forms(vocabulary[int(vocabularyTree.selection()[0])]))
	
def vocabularyTreeClick(event):
	item = vocabularyTree.identify('item',event.x,event.y)
	if item:
		lemmaAddingEntry.delete(0,END)
		posAddingEntry.delete(0,END)
		endingsAddingEntry.delete(0,END)
		lemmaAddingEntry.insert(0, vocabularyTree.item(item,"values")[0])
		posAddingEntry.insert(0, vocabularyTree.item(item,"values")[1])
		endingsAddingEntry.insert(0, vocabularyTree.item(item,"values")[2])

createVocabularyButton.config(command=createVocabulary)
openVocabularyButton.config(command=openVocabulary)
saveButton.config(command=saveVocabulary)
clearButton.config(command=clearVocabulary)
addButton.config(command=addVocabulary)
editButton.config(command=editVocabulary)
deleteButton.config(command=deleteVocabulary)
formsButton.config(command=formsVocabulary)
vocabularyTree.bind("<Button-1>", vocabularyTreeClick)

#==================================PACKING UI ELEMENTS======================================================================
space0.pack()
inputFrame.pack()
inputText.pack()
createVocabularyButton.pack(side='left')
orLabel.pack(side='left')
openVocabularyButton.pack(side='right')
space1.pack()
vocabularyFrame.pack()
vocabularyTree.pack()
saveButton.pack(side='left')
orLabel2.pack(side='left')
clearButton.pack(side='right')
space2.pack()
addingFrame.pack()
lemmaAddingLabel.pack(side='left')
lemmaAddingEntry.pack(side='left')
posAddingLabel.pack(side='left')
posAddingEntry.pack(side='left')
endingsAddingLabel.pack(side='left')
endingsAddingEntry.pack(side='left')
space21.pack(side='left')
addButton.pack(side='left')
editButton.pack(side='left')
formsButton.pack(side='left')
deleteButton.pack(side='left')
root.mainloop()