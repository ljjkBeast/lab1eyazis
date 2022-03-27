from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter import filedialog
import pickle
import vocabularylib as vl
from striprtf.striprtf import rtf_to_text

root = Tk()
vocabulary = []

# ==================================INPUT FRAME=========================================================================
space0 = Label(root, text='\n')
inputFrame = Frame(root, bg='grey', bd=5)
inputText = Text(inputFrame, height=15, width=130, wrap=WORD)
createVocabularyButton = Button(inputFrame, text='Create vocabulary from text', width=55, height=2, bg='green')
# orLabel = Label(inputFrame, text=' Or', width=35, height=2, bg='grey', fg='white')
openVocabularyButton = Button(inputFrame, text='Open vocabulary from file', width=55, height=2, bg='blue')
openTxtButton = Button(inputFrame, text='Open txt', width=17, height=2, bg='grey')
openRtfButton = Button(inputFrame, text='Open rtf', width=18, height=2, bg='grey')

# ==================================VOCABULARY FRAME====================================================================
space1 = Label(root, text='\n')
vocabularyFrame = Frame(root, bg='grey', bd=5)
vocabularyTree = ttk.Treeview(vocabularyFrame, columns=("Lemma", "Part of speech", "Endings"), selectmode='browse', height=11)
vocabularyTree.heading('Lemma', text="Lemma", anchor=W)
vocabularyTree.heading('Part of speech', text="Part of speech", anchor=W)
vocabularyTree.heading('Endings', text="Endings", anchor=W)
vocabularyTree.column('#0', stretch=NO, minwidth=0, width=0)
vocabularyTree.column('#1', stretch=NO, minwidth=347, width=347)
vocabularyTree.column('#2', stretch=NO, minwidth=347, width=347)
vocabularyTree.column('#3', stretch=NO, minwidth=347, width=347)
saveButton = Button(vocabularyFrame, text='Save vocabulary to file', width=55, height=2, bg='green')
orLabel2 = Label(vocabularyFrame, text=' Or', width=35, height=2, bg='grey', fg='white')
clearButton = Button(vocabularyFrame, text='Clear vocabulary', width=55, height=2, bg='red')

# ==================================ADDING, EDITING, DELETING FRAME=====================================================
space2 = Label(root, text='\n')
addingFrame = Frame(root, bg='grey', bd=5)
lemmaAddingLabel = Label(addingFrame, text=' Lemma: ', width=10, height=2, bg='grey', fg='white')
lemmaAddingEntry = Entry(addingFrame, width=23)
posAddingLabel = Label(addingFrame, text=' Part of speech: ', width=14, height=2, bg='grey', fg='white')
posAddingEntry = Entry(addingFrame, width=23)
endingsAddingLabel = Label(addingFrame, text=' Endings: ', width=10, height=2, bg='grey', fg='white')
endingsAddingEntry = Entry(addingFrame, width=23)
space21 = Label(addingFrame, text='          ', bg='grey')
addButton = Button(addingFrame, text='Add', width=5, height=2, bg='green')
editButton = Button(addingFrame, text='Edit selected', width=11, height=2, bg='green')
formsButton = Button(addingFrame, text='Create all forms of selected', width=22, height=2, bg='green')
deleteButton = Button(addingFrame, text='Delete selected', width=14, height=2, bg='red')

# ==================================FUNCTIONS===========================================================================
rows = 0


def show_vocabulary():
	global rows
	rows = 0
	vocabularyTree.delete(*vocabularyTree.get_children())
	for lexeme in vocabulary:
		vocabularyTree.insert('', 'end', values=(lexeme.lemma, lexeme.part_of_speech, lexeme.endings), iid=rows)
		rows += 1


def create_vocabulary():
	global vocabulary
	vocabulary = vl.create_vocabulary_from_text(inputText.get('1.0', END))
	vocabulary.sort()
	show_vocabulary()


def open_vocabulary():
	global vocabulary
	file_path = filedialog.askopenfilename()
	if file_path != "":
		f = open(file_path, 'rb')
		vocabulary = pickle.load(f)
		f.close()
		show_vocabulary()


def open_rtf():
	global vocabulary
	file_path = filedialog.askopenfilename()
	if file_path != "":
		f = open(file_path, 'r')
		text = rtf_to_text(f.read())
		vocabulary = vl.create_vocabulary_from_text(text)
		f.close()
		vocabulary.sort()
		show_vocabulary()


def open_txt():
	global vocabulary
	file_path = filedialog.askopenfilename()
	if file_path != "":
		f = open(file_path, 'r')
		text = f.read()
		vocabulary = vl.create_vocabulary_from_text(text)
		f.close()
		vocabulary.sort()
		show_vocabulary()


def save_vocabulary():
	file_path = filedialog.asksaveasfilename()
	if file_path != "":
		f = open(file_path, 'wb')
		pickle.dump(vocabulary, f)
		f.close()


def clear_vocabulary():
	global rows, vocabulary
	rows = 0
	vocabulary = []
	vocabularyTree.delete(*vocabularyTree.get_children())


def add_vocabulary():
	if lemmaAddingEntry.get() != "" and posAddingEntry.get() != "":
		vocabulary.append(vl.Lexeme(lemmaAddingEntry.get(), posAddingEntry.get(), endingsAddingEntry.get()))
		vocabulary.sort()
		show_vocabulary()


def edit_vocabulary():
	if vocabularyTree.selection() != () and lemmaAddingEntry.get() != "" and posAddingEntry.get() != "":
		vocabulary[int(vocabularyTree.selection()[0])] = vl.Lexeme(lemmaAddingEntry.get(), posAddingEntry.get(), endingsAddingEntry.get())
		vocabulary.sort()
		show_vocabulary()


def delete_vocabulary():
	if vocabularyTree.selection() != ():
		del vocabulary[int(vocabularyTree.selection()[0])]
		vocabulary.sort()
		show_vocabulary()


def forms_vocabulary():
	if vocabularyTree.selection() != ():
		messagebox.showinfo("Forms", vl.create_forms(vocabulary[int(vocabularyTree.selection()[0])]))


def vocabulary_tree_click(event):
	item = vocabularyTree.identify('item', event.x, event.y)
	if item:
		lemmaAddingEntry.delete(0, END)
		posAddingEntry.delete(0, END)
		endingsAddingEntry.delete(0, END)
		lemmaAddingEntry.insert(0, vocabularyTree.item(item, "values")[0])
		posAddingEntry.insert(0, vocabularyTree.item(item, "values")[1])
		endingsAddingEntry.insert(0, vocabularyTree.item(item, "values")[2])


createVocabularyButton.config(command=create_vocabulary)
openVocabularyButton.config(command=open_vocabulary)
openTxtButton.config(command=open_txt)
openRtfButton.config(command=open_rtf)
saveButton.config(command=save_vocabulary)
clearButton.config(command=clear_vocabulary)
addButton.config(command=add_vocabulary)
editButton.config(command=edit_vocabulary)
deleteButton.config(command=delete_vocabulary)
formsButton.config(command=forms_vocabulary)
vocabularyTree.bind("<Button-1>", vocabulary_tree_click)

# ==================================PACKING UI ELEMENTS=================================================================
space0.pack()
inputFrame.pack()
inputText.pack()
createVocabularyButton.pack(side='left')
# orLabel.pack(side='left')
openTxtButton.pack(side='left')
openRtfButton.pack(side='left')
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
