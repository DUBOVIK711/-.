import tkinter as tk
from datetime import datetime

class DoorHanForm:
    def __init__(self, root):
        self.root = root
        self.root.title("DoorHan Западная Сибирь")
        
        # Размер окна
        self.root.geometry("540x780")
        self.root.configure(bg='#667eea')
        
        self.create_ui()
    
    def create_ui(self):
        # Белая карточка
        self.card = tk.Frame(self.root, bg='#ffffff')
        self.card.place(relx=0.04, rely=0.03, relwidth=0.92, relheight=0.94)
        
        # ===== ШАПКА =====
        header = tk.Frame(self.card, bg='#ffffff')
        header.pack(fill='x', padx=20, pady=30)
        
        title = tk.Label(header, text="DoorHan", 
                        font=("Arial", 28, "bold"),
                        bg='#ffffff', fg='#212529')
        title.pack(pady=(0, 5))
        
        subtitle = tk.Label(header, text="Западная Сибирь",
                           font=("Arial", 18, "bold"),
                           bg='#ffffff', fg='#667eea')
        subtitle.pack(pady=5)
        
        tagline = tk.Label(header, text="Запись на замеры",
                          font=("Arial", 12),
                          bg='#ffffff', fg='#495057')
        tagline.pack(pady=5)
        
        # Разделитель
        tk.Frame(self.card, bg='#dee2e6', height=2).pack(fill='x', padx=20, pady=15)
        
        # ===== ФОРМА =====
        form_frame = tk.Frame(self.card, bg='#ffffff')
        form_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Имя
        tk.Label(form_frame, text="Имя", font=("Arial", 10, "bold"),
                bg='#ffffff', fg='#495057', anchor='w').pack(fill='x', pady=(10, 5))
        
        self.name_entry = tk.Entry(form_frame, font=("Arial", 11),
                                  relief='solid', bd=1,
                                  highlightbackground='#dee2e6',
                                  highlightcolor='#667eea',
                                  highlightthickness=1)
        self.name_entry.pack(fill='x', pady=5, ipady=8)
        
        self.name_error = tk.Label(form_frame, text="", font=("Arial", 9),
                                  bg='#ffffff', fg='#dc3545', anchor='w')
        self.name_error.pack(fill='x')
        
        # Email
        tk.Label(form_frame, text="Email", font=("Arial", 10, "bold"),
                bg='#ffffff', fg='#495057', anchor='w').pack(fill='x', pady=(10, 5))
        
        self.email_entry = tk.Entry(form_frame, font=("Arial", 11),
                                   relief='solid', bd=1,
                                   highlightbackground='#dee2e6',
                                   highlightcolor='#667eea',
                                   highlightthickness=1)
        self.email_entry.pack(fill='x', pady=5, ipady=8)
        
        self.email_error = tk.Label(form_frame, text="", font=("Arial", 9),
                                   bg='#ffffff', fg='#dc3545', anchor='w')
        self.email_error.pack(fill='x')
        
        # Сообщение
        tk.Label(form_frame, text="Сообщение", font=("Arial", 10, "bold"),
                bg='#ffffff', fg='#495057', anchor='w').pack(fill='x', pady=(10, 5))
        
        self.message_text = tk.Text(form_frame, font=("Arial", 11),
                                   height=4, relief='solid', bd=1,
                                   highlightbackground='#dee2e6',
                                   highlightcolor='#667eea',
                                   highlightthickness=1)
        self.message_text.pack(fill='x', pady=5)
        
        self.message_error = tk.Label(form_frame, text="", font=("Arial", 9),
                                     bg='#ffffff', fg='#dc3545', anchor='w')
        self.message_error.pack(fill='x')
        
        # Чекбокс
        check_frame = tk.Frame(form_frame, bg='#ffffff')
        check_frame.pack(fill='x', pady=15)
        
        self.agree_var = tk.BooleanVar()
        self.agree_check = tk.Checkbutton(check_frame, variable=self.agree_var,
                                         bg='#ffffff', activebackground='#ffffff')
        self.agree_check.pack(side='left')
        
        tk.Label(check_frame, text="Я согласен на обработку\nперсональных данных",
                font=("Arial", 9), bg='#ffffff', fg='#495057',
                justify='left').pack(side='left', fill='x', expand=True, padx=8)
        
        self.agree_error = tk.Label(form_frame, text="", font=("Arial", 9),
                                   bg='#ffffff', fg='#dc3545', anchor='w')
        self.agree_error.pack(fill='x')
        
        # Кнопка
        submit_btn = tk.Button(form_frame, text="Отправить",
                              font=("Arial", 12, "bold"),
                              bg='#667eea', fg='white',
                              activebackground='#5568d3',
                              activeforeground='white',
                              relief='flat', cursor='hand2',
                              command=self.on_submit)
        submit_btn.pack(fill='x', pady=(20, 10), ipady=10)
        
        # ===== СООБЩЕНИЕ ОБ УСПЕХЕ =====
        self.success_frame = tk.Frame(self.card, bg='#ffffff')
        
        tk.Label(self.success_frame, text="✅", font=("Arial", 60),
                bg='#ffffff').pack(pady=(40, 10))
        tk.Label(self.success_frame, text="Спасибо за вашу заявку!",
                font=("Arial", 18, "bold"), bg='#ffffff', fg='#28a745').pack(pady=5)
        tk.Label(self.success_frame, text="Вы записаны",
                font=("Arial", 13), bg='#ffffff', fg='#495057').pack(pady=5)
    
    # ===== ВАЛИДАЦИЯ =====
    def validate_name(self):
        value = self.name_entry.get().strip()
        if not value:
            self.name_error.config(text='Пожалуйста, введите ваше имя')
            self.name_entry.config(highlightbackground='#dc3545')
            return False
        self.name_error.config(text='')
        self.name_entry.config(highlightbackground='#dee2e6')
        return True
    
    def validate_email(self):
        value = self.email_entry.get().strip()
        if not value:
            self.email_error.config(text='Пожалуйста, введите email')
            self.email_entry.config(highlightbackground='#dc3545')
            return False
        if '@' not in value:
            self.email_error.config(text='Email должен содержать символ @')
            self.email_entry.config(highlightbackground='#dc3545')
            return False
        at_idx = value.index('@')
        if '.' not in value[at_idx+1:]:
            self.email_error.config(text='Email должен содержать точку после @')
            self.email_entry.config(highlightbackground='#dc3545')
            return False
        self.email_error.config(text='')
        self.email_entry.config(highlightbackground='#dee2e6')
        return True
    
    def validate_message(self):
        value = self.message_text.get("1.0", "end-1c").strip()
        if len(value) < 10:
            self.message_error.config(text='Сообщение должно содержать минимум 10 символов')
            self.message_text.config(highlightbackground='#dc3545')
            return False
        self.message_error.config(text='')
        self.message_text.config(highlightbackground='#dee2e6')
        return True
    
    def validate_agree(self):
        if not self.agree_var.get():
            self.agree_error.config(text='Необходимо согласие на обработку данных')
            return False
        self.agree_error.config(text='')
        return True
    
    # ===== ОТПРАВКА =====
    def on_submit(self):
        if (self.validate_name() and 
            self.validate_email() and 
            self.validate_message() and 
            self.validate_agree()):
            
            # Сохраняем заявку
            data = {
                'name': self.name_entry.get().strip(),
                'email': self.email_entry.get().strip(),
                'message': self.message_text.get("1.0", "end-1c").strip(),
                'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Сохраняем в файл
            with open('applications.txt', 'a', encoding='utf-8') as f:
                f.write(f"\n{'='*50}\n")
                f.write(f"Дата: {data['time']}\n")
                f.write(f"Имя: {data['name']}\n")
                f.write(f"Email: {data['email']}\n")
                f.write(f"Сообщение: {data['message']}\n")
            
            # Показываем успех
            self.name_entry.pack_forget()
            self.name_error.pack_forget()
            self.email_entry.pack_forget()
            self.email_error.pack_forget()
            self.message_text.pack_forget()
            self.message_error.pack_forget()
            self.agree_check.pack_forget()
            self.agree_error.pack_forget()
            
            # Находим все label и кнопки
            for widget in self.card.winfo_children():
                if isinstance(widget, tk.Frame):
                    widget.pack_forget()
            
            self.success_frame.pack(fill='both', expand=True, padx=20, pady=10)
            
            # Через 3 секунды
            self.root.after(3000, self.reset_form)
    
    def reset_form(self):
        # Очищаем поля
        self.name_entry.delete(0, 'end')
        self.email_entry.delete(0, 'end')
        self.message_text.delete('1.0', 'end')
        self.agree_var.set(False)
        
        # Показываем форму снова
        self.success_frame.pack_forget()
        self.create_ui()


if __name__ == '__main__':
    root = tk.Tk()
    app = DoorHanForm(root)
    root.mainloop()
