import tkinter as tk
from tkinter import colorchooser as cc
from tkinter.scrolledtext import ScrolledText
import tkinter.filedialog as fd
import re
from spell_check import rectify, all_words
import spell_check_fa
import grammar
import picture_analysis
import os
import mmap
import time


class Window():
    
    def __init__(self):
        
        self.root = tk.Tk()
        self.root.geometry("1117x800")
        self.root.title("Spell Checker")
        self.text = ScrolledText(self.root, font=('Times New Roman', 27))
        self.text.bind("<KeyRelease>", self.check)
        self.text.pack()
        self.old_spaces = 0
        self.grammar = ''
        #self.line = 1 
        self.highlight_color = 'red'
        #self.new_win = tk.Toplevel(self.root)
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        
        self.view_menu = tk.Menu(self.menubar, tearoff=False)
        self.menubar.add_cascade(label="Theme", menu=self.view_menu)
        self.view_menu.add_command(label="Light Theme", command=self.light_theme)
        self.view_menu.add_command(label="Dark Theme", command=self.dark_theme)
        self.view_menu.add_command(label="Ultra Dark Theme", command=self.ultra_dark_theme)
        self.view_menu.add_separator()
        self.view_menu.add_command(label="Change Background Color", command=self.change_bg)
        self.view_menu.add_command(label="Change Text Color", command=self.change_fg)
        self.view_menu.add_command(label="Change Highlight Color", command=self.change_highlight)
        self.view_menu.add_separator()

        self.other_menu = tk.Menu(self.menubar, tearoff=False)
        self.menubar.add_cascade(label="Other", menu=self.other_menu)
        self.other_menu.add_command(label="Grammar check", command=self.grammar_check)
        self.other_menu.add_separator()
        self.other_menu.add_command(label='Picture analysis', command=self.picture_catch)
        
        self.test_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='words', menu=self.test_menu)
        self.test_menu.add_command(label='add_word', command=self.add_word)
        self.test_menu.add_command(label='delete word', command=self.delete_word)
        self.test_menu.add_separator()
        self.test_menu.add_command(label='sort_words', command=self.sort_words)
        #self.test_menu.add_command(label='test', command=new_label_word)

    #self.root.bind('<return>', line_inc)
        self.root.bind('<Control-n>', self.new_window)
        #self.root.bind('<Control-r>', new_label_word)
        self.root.mainloop()

    def new_window(self, event):
        win_guess = tk.Toplevel(self.root)
        win_guess.geometry("343x343")
        tk.Label(win_guess, text=f'{self.incorrect_word} at line:{self.line}').pack()
        tk.Label(win_guess, text=f'{self.grammar} at line {self.line}').pack()
            
    # def new_label_word(event):
    #tk.Label(self.new_win, text=f'{self.incorrect_word}').pack()

    def light_theme(self):
        self.text.config(bg='white', fg='black')
    
    def dark_theme(self):
        self.text.config(bg="#0b213d", fg='white')
    
    def ultra_dark_theme(self):
        self.text.config(bg='black', fg='white')
    
    def change_bg(self):
        bg_color: str = cc.askcolor()[1] or 'black' 
        self.text.config(bg=bg_color) 
         
    def change_fg(self):
        fg_color = cc.askcolor()[1] or 'white'
        self.text.config(fg=fg_color)
    
    def change_highlight(self):
        h_color = cc.askcolor()
        self.highlight_color = h_color[1]        
    
    def grammar_check(self):
        sentence = self.text.get('1.0', 'end-1c')
        self.grammar = grammar.gf.correct(sentence)
        print(grammar.gf.correct(sentence))
    
    # def line_inc(event):
    #     self.line = self.line + 1

    def picture_catch(self):
        file = fd.askopenfilename(defaultextension='.png' ,filetypes=[('PNG files', '*.png*')])
        if file:
                self.text.insert('1.0', picture_analysis.analyze(os.path.basename(file)))

    def add_word():
        win_word = tk.Toplevel(self.root)
        win_word.geometry("343x117")
        tk.Label(win_word, text='Please enter the word:').pack()
        box = tk.Text(win_word)
        
        def update():
            with open('Dictionary.txt', 'a') as f:
                f.write(box.get('1.0', 'end-1c'))
                
        tk.Button(win_word, text='Update', command=update).pack() 
        box.pack()

    def sort_words():
        with open('Dictionary.txt', 'r') as f:
            names = [line.strip() for line in f.readlines()]
        names.sort()

    def delete_word():
        pass
        # #     win_word = tk.Toplevel(self.root)
        # #     win_word.geometry("343x117")
        # #     tk.Label(win_word, text='Please enter a word').pack()
        # #     box = tk.Text(win_word)
        # #     # with open('Dictionary.txt', 'rb') as f, \
        # #     #     mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as match:
        # #     #     if match.find(str_box) != -1:
        # #     # with open('Dictionary.txt', 'r') as f:
        # #     #   if f'{box.get('1.0', 'end-1c')}' in f.read():
        # #     #       f.replace()
        #

            
    
    def check(self, event):
       
        #if event.keycode != 65:
        #   return

        word_line = self.text.index(tk.INSERT).split('.')[0]
        lines = []
        if int(word_line) == 1:
            lines = ['1', '2']
        else:
            for i in range(int(word_line)-1, int(word_line)+2):
                print(i)
                lines.append(str(i))
        for word_line in lines:
            self.content = self.text.get(f'{word_line}.0', f'{word_line}.end')
            for tag in self.text.tag_names():
                if not tag.endswith(word_line):
                    continue
                self.text.tag_delete(tag)

            word_start = 0
            for word in self.content.split():
                if word not in all_words:
                    print(rectify(word))
                    #print(spell_check_fa.rectify(word))
                    self.incorrect_word = rectify(word)
                    self.line = word_line
                    print(word_line)
                    self.text.tag_add(word+word_line, f"{word_line}.{word_start}", f"{word_line}.{word_start+len(word)}")
                    self.text.tag_config(word+word_line, foreground=self.highlight_color)
                word_start += len(word) + 1




    #    self.content = self.text.get('1.0', tk.END)
    #     space_count = self.content.count(" ")
    # 
    #     if space_count != self.old_spaces:
    #         self.old_spaces = space_count
    #
    #         for tag in self.text.tag_names():
    #             self.text.tag_delete(tag)
    #
    #         for word in self.content.split(" "):
    #             if re.sub(r"[^\w+]", '',word.lower()) not in all_words:
    #                 self.incorrect_words = rectify(word)
    #                 print(rectify(word))
    #                 position = self.content.find(word)
    #                 #breakpoint()
    #                  
    #                 self.text.tag_add(word, f"1.{position}", f"1.{position + len(word)}")
    #                 self.text.tag_config(word, foreground=self.highlight_color)
    #



        #     t = time.time()
        #     reg = re.compile(r'([A-Za-z][^\.!?]*[\.!?])')
        #     sentence = nltk.sent_tokenize(content)[-1]
        #     print(grammar.gf.correct(sentence))
        #     print(f'took {time.time() - t}s')
        # if reg.findall(content):
        # 
        # line = self.text.get("insert linestart", "insert lineend")
        # word = self.text.get("insert wordstart", "insert wordend")
        # insert = list(map(int, self.text.index(tk.INSERT).split('.')))
        #
        # for tag in self.text.tag_names():
        #     if tag.startswith(f'{insert[0]}_'):
        #         self.text.tag_delete(tag)
        #
        # last_word = ''
        # for d, c in enumerate(line):
        #     if c == ' ':
        #         word = last_word
        #         last_word = ''
        #         if word in all_words:
        #             continue
        #         if word == ' ':
        #             return
        #         print(word)
        #         rectify(word)
        #
        #         word = f'{insert[0]}_{word}{d}'
        #
        #         start = f'{insert[0]}.{d-len(word)}'
        #         end = f'{insert[0]}.{d}'
        #         print(f'{start=} {end=}')
        #
        #         self.text.tag_add(word, start, end)
        #         self.text.tag_config(word, foreground=self.highlight_color)
        #
        #
        #         continue
        #     last_word += c
        #
'''
        if word == '\n':
            line = line[:insert[1]]
            words = line.split()
            word = words[-1]

        if word in all_words:
            return
        
        #for tag in self.text.tag_names():
            #self.text.tag_delete(tag)
 

        word_index = line.rfind(word)
        position_start = f'{insert[0]}.{word_index}'
        position_end = f'{insert[0]}.{word_index + len(word)}'
      
        self.text.tag_add(word, position_start, position_end)
        self.text.tag_config(word, foreground=self.highlight_color)
        print(rectify(word))
        '''
        
Window()
