import customtkinter as ctk
import openai
from googletrans import Translator
import threading


API_KEY = ''
model = "gpt-3.5-turbo"
msg_counter = 0
Dark = True
main_bg = "#33383f"


def translate_text(text, target_lang):
    try:
        translation = translator.translate(text, dest=target_lang)


        if translation is not None and hasattr(translation, 'text'):
            return translation.text
        else:
            print("خطای ترجمه: امکان ترجمه متن وجود ندارد.")
    except Exception as e:
        print(f"خطای ترجمه: {e}")
    return ""

def get_model_response(user_input):
    response = ''
    tokens_left = 4096
    if user_input:
        # translated_message = translate_text(user_input, 'en')


        translated_message = user_input
        while len(translated_message) > 0 and tokens_left > 0:
            input_text = translated_message[:tokens_left]
            translated_message = translated_message[tokens_left:]
            tokens_left = max(4096 - len(input_text), 0)
            response_part = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": "you are a profetional teacher assistant"},
                    {"role": "user", "content": input_text}
                ],
                max_tokens=4000,
                temperature=0.6,)
            if response_part.choices and len(response_part.choices) > 0:
                assistant_response = response_part.choices[0].message.content.strip()
                # translated_response = translate_text(assistant_response, 'fa')

                translated_response = assistant_response
                response += translated_response
    if response:
        return response
    else:
        return "متأسفانه مدل قادر به پاسخگویی نیست."

def save_username():
    username = user_input_entry.get()
    with open("username.txt", "w", encoding="utf-8") as file:
        file.write(username)
    return username

def load_username():
    try:
        with open("username.txt", "r", encoding="utf-8") as file:
            username = file.read()
        return username
    except FileNotFoundError:
        return None

def send_message():
    global msg_counter
    text = user_input_entry.get()
    user_input_entry.delete(0, ctk.END)
    username = load_username()
    if username is None:
        username = save_username()
    label = ctk.CTkLabel(scrol,
                         corner_radius=10,
                         wraplength=350,
                         text=f"user: {text}",
                         fg_color='#141a70',
                         text_color="white",
                         font=("lucida", 16, 'bold'),
                         justify="left")
    label.grid(row=msg_counter, column=0, padx=2, pady=2, sticky="e")
    msg_counter += 1
    threading.Thread(target=respose_message, args=(text,)).start()

def respose_message(text):
    global msg_counter
    response = get_model_response(text)
    label2 = ctk.CTkLabel(scrol,
                          corner_radius=10,
                          wraplength=350,
                          text=f"GPT: {response}",
                          fg_color='#adb3bd',
                          text_color="black",
                          font=("lucida", 16, 'bold'),
                          justify="left")
    label2.grid(row=msg_counter, column=0, padx=2, pady=2, sticky="w")
    msg_counter += 1

def light():
    global main_bg
    global Dark
    if Dark:
        main_bg = '#eaecee'
        chat_frame.configure(fg_color='#adb3bd')
        ctk.set_appearance_mode('light')
        header_frame.configure(fg_color=main_bg)
        scrol.configure(fg_color=main_bg)
        user_input_entry.configure(fg_color=main_bg,
                                   placeholder_text_color="black",
                                   text_color='black')
        header_label.configure(text_color='black')
        light_btn.configure(text="\u263E")
        Dark = False
    else:
        main_bg = "#33383f"
        ctk.set_appearance_mode('dark')
        chat_frame.configure(fg_color='#606770')
        header_frame.configure(fg_color=main_bg)
        scrol.configure(fg_color=main_bg)
        user_input_entry.configure(fg_color=main_bg,
                                   placeholder_text_color="white",
                                   text_color='white')
        header_label.configure(text_color='white')
        light_btn.configure(text="\u263c")
        Dark = True

openai.api_key = API_KEY

translator = Translator()

root = ctk.CTk()

root.title("Chat Application")

# Setting up the main frame
root.geometry("800x600+100+50")
root.resizable(width=False, height=False)
ctk.set_appearance_mode("dark")


# chat_frame settings
chat_frame = ctk.CTkFrame(root,
                          fg_color='#606770')
chat_frame.pack(fill="both",
                expand=True)

# header_frame settings
header_frame = ctk.CTkFrame(chat_frame,
                            fg_color=main_bg,
                            height=80)
header_frame.pack(pady=5,
                  padx=5,
                  fill="x")

# mode_btn settings
light_btn = ctk.CTkButton(header_frame,
                          command=light,
                          fg_color="#19a0ac",
                          text="\u263c",
                          font=ctk.CTkFont(size=28),
                          width=15)
light_btn.pack(padx=(5, 0),
               pady=5,
               side="left")

# header_label settings
header_label = ctk.CTkLabel(header_frame,
                            text="GPT 3.5 Turbo",
                            font=("Arial", 32, "bold"),
                            text_color="white")
header_label.pack(padx=(250, 0),
                  side='left')

# scrol settings
scrol = ctk.CTkScrollableFrame(chat_frame,
                               fg_color=main_bg)
scrol.columnconfigure(0, weight=1)
scrol.pack(padx=5,
           pady=0,
           fill="both",
           expand=True)


# input_frame settings
input_frame = ctk.CTkFrame(chat_frame,
                           fg_color="transparent")
input_frame.pack(padx=10,
                 pady=10)

# user_input_entry settings
user_input_entry = ctk.CTkEntry(input_frame,
                                width=700,
                                height=50,
                                fg_color=main_bg,
                                font=("Söhne", 16),
                                placeholder_text="Send a message.",
                                placeholder_text_color="white",
                                text_color='white',
                                corner_radius=30)
user_input_entry.pack(side='left')

# send_btn settings
send_btn = ctk.CTkButton(input_frame,
                         text='\u27A4',
                         width=5,
                         height=40,
                         font=ctk.CTkFont(size=15),
                         fg_color="#19a0ac",
                         text_color='white',
                         corner_radius=15,
                         command=send_message
                         )
send_btn.pack(side='left',
              padx=8,
              pady=8)

root.mainloop()
