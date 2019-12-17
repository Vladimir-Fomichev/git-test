from tkinter import *
import sqlite3
import random

# Соединение с базой данных слов.
conn = sqlite3.connect('flashcards.db')
cursor = conn.cursor()
cursor.execute('SELECT max(id) FROM minilex')
id_max = cursor.fetchone()
		
def new_word():
	
	#Проверка количества оставшихся для изучения слов.
	cursor.execute('SELECT COUNT(*) FROM minilex WHERE score < 2')
	words_remain = cursor.fetchone()
	
	while words_remain[0] > 0:
		
		#Выбор случайного id слова.
		global id_rand
		id_rand = random.randint(1, id_max[0])
		cursor.execute('SELECT COUNT(*) FROM minilex WHERE score < 2')
		words_remain = cursor.fetchone()
		cursor.execute('SELECT * FROM minilex WHERE score < 2 and id = ?', (id_rand,))
		global word_eng
		word_eng = cursor.fetchone()
		
		if word_eng is None:
			continue
		
		#Вывод английского слова, подстройка размера окна под количество букв.
		else:
			lbl_eng['text'] = word_eng[2]
		
			if len(word_eng[2]) > num_letters:
				lbl_eng['width'] = len(word_eng[2])
			else:
				lbl_eng['width'] = num_letters
				
			lbl_rus['text'] = ''
			lbl_rus['width'] = num_letters
			btn_check.grid(pady = 5)
			btn_yes.grid_remove()
			btn_no.grid_remove()
			return word_eng
	
	#Все слова изучены, вывод сообщения об этом. Конец программы.
	else:
		top_frame.pack_forget()
		bottom_frame.pack_forget()

		lbl_end = Label(text = "Bravo! That's all words!",font=('Times 36'))
		lbl_end.pack()

#Вывод перевода, подстройка размера окна под количество букв.
def Checking():
	lbl_rus['text'] = word_eng[1]
	if len(word_eng[1]) > num_letters:
		lbl_rus['width'] = len(word_eng[1])
	else:
		lbl_rus['width'] = num_letters
	btn_check.grid_remove()
	btn_yes.grid(column=0, row=0, pady = 5, padx = 10)
	btn_no.grid(column=1, row=0)

#Если перевод верен, увеличивается баллы у слова.
def ScorePlus():
    cursor.execute('UPDATE minilex SET score = score + 1 WHERE id = ?', (id_rand,))
    conn.commit()
    new_word()

#Создание полей и кнопок.
window = Tk()
window.title('English-Russian')

top_frame = Frame()
top_frame.pack()

bottom_frame = Frame()
bottom_frame.pack( side = BOTTOM )	

#Размер окна по заданному количеству букв в слове.
num_letters = 10

lbl_eng = Label(top_frame, width = num_letters, font=('Times 24'), bg='white')
lbl_eng.pack(pady = 5)
lbl_rus = Label(top_frame, width = num_letters, font=('Times 24'), bg='white')
lbl_rus.pack(pady = 5)

btn_check = Button(bottom_frame, text='Check', font=(24), bg='yellow', command=Checking)

btn_yes = Button(bottom_frame, text='Yes', font=(24), bg='green', command = ScorePlus)
btn_no = Button(bottom_frame, text='No', font=(24), bg='red', command = new_word)

#Запуск карточек.
new_word()

window=mainloop()