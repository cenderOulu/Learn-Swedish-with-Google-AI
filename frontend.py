from tkinter import *
from tkinter import font
import backend
import webbrowser
state = 0
exercise = None
new_window = None
text = None
questions_frame = None
current_question = 0
rightanswer = False
settings_window = None
api_key_var = None
root = None


def menu():
    title_font = font.Font(family="Helvetica", size=24, weight="bold")
    custom_font = font.Font(family="Helvetica", size=16)
    title = Label(root, text="I Want To Learn Swedish", font=title_font)
    title.place(relx=0.5, rely=0.1, anchor=CENTER)
    options = [
        "A1-A2",
        "A2-B1",
        "B1-B2",
        "B2-C1",
        "C1-C2"
    ]
    selected_option = StringVar(root)
    selected_option.set(options[0])
    drop_down_menu = OptionMenu(root, selected_option, *options)
    frame = Frame(root, width=600, height=400)
    imat_label = Label(frame, text="I'm at", font=custom_font)
    imat_label.pack(side=LEFT, padx=(0, 10))
    drop_down_menu = OptionMenu(frame, selected_option, *options)
    drop_down_menu.pack(side=LEFT)
    frame.place(relx=0.5, rely=0.2, anchor=CENTER)
    start_button = Button(root, text="Start",width=50,command=lambda: start(selected_option.get()))
    start_button.place(relx=0.5, rely=0.3, anchor=CENTER)
    exit_button = Button(root, text="Exit",width=50, command=root.quit)
    exit_button.place(relx=0.5, rely=0.5, anchor=CENTER)
    setting_button = Button(root, text="Setting",width=50, command=create_settings_window)
    setting_button.place(relx=0.5, rely=0.4, anchor=CENTER)




def start(level):
    global new_window
    global exercise
    print(level)
    if new_window and new_window.winfo_exists():
        new_window.lift() 
        new_window.focus_force()
        return
    exercise = backend.Exercise(level)
    new_window = Toplevel(root)
    new_window.title(exercise.title)
    new_window.geometry("1000x900")
    paragraph(exercise.paragraph)
    show_question(current_question)

def show_definition(event):
    index = text.index("@%s,%s" % (event.x, event.y))
    tags = text.tag_names(index)
    webbrowser.open(f'https://folkets-lexikon.csc.kth.se/folkets/folkets.en.html#lookup&{tags[0]}')

def add_clickable_words(widget, text_content):
    words = text_content.split()
    for word in words:
        start_index = widget.index("end-1c")
        if start_index != "1.0":
            widget.insert("end", " ")
        widget.insert("end", word)
        end_index = widget.index("end-1c")
        tag_name = f"{word.strip('.,?!')}"
        widget.tag_add(tag_name, start_index, end_index)
        widget.tag_bind(tag_name, "<Button-1>", show_definition)
        widget.tag_config(tag_name, foreground="black", underline=False)


def paragraph(par):
    global text
    text = Text(new_window, wrap="word", font=("Arial", 12), borderwidth=0, highlightthickness=0, height=20, width=80)
    text.pack(padx=20, pady=20)
    add_clickable_words(text, par)
    text.config(state="disabled")

def show_question(question_index):
    global questions_frame, current_question, rightanswer
    
    if questions_frame and questions_frame.winfo_exists():
        rightanswer=False
        questions_frame.destroy()
    
    questions_frame = Frame(new_window)
    questions_frame.pack(pady=20)
    question_text = Text(questions_frame, wrap="word", font=("Arial", 12), 
                        borderwidth=0, highlightthickness=0, height=3, width=80)
    question_text.pack(pady=10)
    add_clickable_words(question_text, exercise.questions[question_index]['question'])
    question_text.config(state="disabled")
    options_frame = Frame(questions_frame)
    options_frame.pack()
    
    nav_frame = Frame(questions_frame)
    nav_frame.pack(pady=20)
    
    next_btn = Button(nav_frame, text="Next", 
                     width=30,command=lambda: navigate(1), 
                     state=NORMAL if question_index < len(exercise.questions)-1 and rightanswer else DISABLED)
    next_btn.pack(side=TOP, padx=10)
    nexit_button = Button(nav_frame, text="Exit", width=10,command=new_window.destroy)
    nexit_button.pack(side=BOTTOM, pady=40)
    for i, option in enumerate(exercise.questions[question_index]['options']):
        btn = Button(options_frame, text=option, width=50, wraplength=600,
                    command=lambda idx=i: check_answer(idx, question_index, next_btn))
        btn.pack(pady=5)
    current_question = question_index

def check_answer(selected_index, question_index, nextt):
    global rightanswer
    correct_answer = exercise.questions[question_index]['answer']
    options = ['A', 'B', 'C', 'D']
    correct_index = options.index(correct_answer)
    options_frame = questions_frame.winfo_children()[1]
    buttons = [child for child in options_frame.winfo_children() if isinstance(child, Button)]
    if selected_index == correct_index:
        buttons[selected_index].config(bg="green")
        nextt.config(state=NORMAL)
    else:
        buttons[selected_index].config(bg="red")

def navigate(direction):
    global current_question
    new_index = current_question + direction
    if 0 <= new_index < len(exercise.questions):
        show_question(new_index)
def create_settings_window():
    global settings_window, api_key_var
    if settings_window and settings_window.winfo_exists():
        settings_window.lift() 
        settings_window.focus_force()
        return
    settings_window = Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("400x300")
    api_frame = Frame(settings_window)
    api_frame.pack(pady=20)
    
    Label(api_frame, text="Gemini API Key:").pack()
    
    api_key_var = StringVar()
    try:
        from backend import get_api_key
        saved_key = get_api_key()
        if saved_key:
            api_key_var.set(saved_key)
    except:
        pass
    
    Entry(api_frame, textvariable=api_key_var, width=40, show="*").pack(pady=5)
    Button(settings_window, 
           text="Save API Key", 
           command=save_api_key_settings).pack(pady=10)
    
    
    Label(settings_window, 
          text="Keys are stored locally in .env file",
          font=("Arial", 8)).pack(side=BOTTOM, pady=10)

def save_api_key_settings():
    from backend import save_api_key
    api_key = api_key_var.get()
    
    if not api_key:
        messagebox.showerror("Error", "Please enter an API key")
        return
    

    save_api_key(api_key)
    settings_window.destroy()



def main():
    global root
    root = Tk()
    root.geometry(f"{600}x{400}")
    root.title("Swedish Learning App")
    print (f"Screen size: {root.winfo_width()}x{root.winfo_height()}")
    menu()
    root.mainloop()
if __name__ == "__main__":
    main()