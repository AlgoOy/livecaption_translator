import threading
import tkinter as tk
import tkinter.font as tkFont
import tkinter.scrolledtext as ScrolledText


class Interface:
    def __init__(self, title='livecaption_translator'):
        self.title = title
        self.root = tk.Tk()
        self.root.title(self.title)
        self.original_text = tk.StringVar()
        self.translated_text = tk.StringVar()

        self.root.geometry('600x400')
        self.root.configure(bg='white')  # 设置窗口背景颜色
        # # 设置美化字体
        # self.font = tkFont.Font(family="Helvetica", size=12)
        # self.title_font = tkFont.Font(family="Helvetica", size=14, weight="bold")

        self.display_text = ScrolledText.ScrolledText(self.root, wrap=tk.WORD, bg="#f0f0f0",
                                                      borderwidth=2, relief="groove")
        self.display_text.pack(padx=10, pady=10, fill='both', expand=True)
        self.display_text.configure(state='disabled')  # 设置文本框为只读

    def append_text(self, original, translated):
        self.display_text.configure(state='normal')  # 允许写入文本
        # 添加文本到文本框
        self.display_text.insert(tk.END, "原始文本：" + original + "\n")
        self.display_text.insert(tk.END, "翻译文本：" + translated + "\n\n")
        self.display_text.configure(state='disabled')  # 设置文本框为只读
        self.display_text.yview(tk.END)  # 滚动到最新文本

    def set_ui(self):
        pass
        # top_frame = tk.Frame(self.root, bg='white')
        # top_frame.pack(padx=10, pady=10, fill='both')
        #
        # tk.Label(top_frame, text="Original Text", font=self.title_font, bg='white').pack()
        # original_label = tk.Label(top_frame, textvariable=self.original_text, wraplength=580, font=self.font,
        #                           bg="#f0f0f0", borderwidth=2, relief="groove")
        # original_label.pack(fill='both', expand=True, padx=5, pady=5)
        #
        # # 设置翻译文本标签和其容器
        # bottom_frame = tk.Frame(self.root, bg='white')
        # bottom_frame.pack(padx=10, pady=10, fill='both')
        #
        # tk.Label(bottom_frame, text="Translated Text", font=self.title_font, bg='white').pack()
        # translated_label = tk.Label(bottom_frame, textvariable=self.translated_text, wraplength=300, font=self.font,
        #                             bg="#f0f0f0", borderwidth=2, relief="groove")
        # translated_label.pack(fill='both', expand=True, padx=5, pady=5)

        # original_label = tk.Label(self.root, textvariable=self.original_text, wraplength=300)
        # original_label.pack()
        #
        # translated_label = tk.Label(self.root, textvariable=self.translated_text, wraplength=300)
        # translated_label.pack()

    def run(self):
        self.set_ui()
        self.root.mainloop()


def update_text(interface, original, translated):
    def task(i, o, t):
        i.append_text(o, t)
        # i.original_text.set(o)
        # i.translated_text.set(t)
    interface.root.after(0, lambda o=original, t=translated: task(interface, o, t))
