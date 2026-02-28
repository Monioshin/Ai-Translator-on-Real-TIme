import os
import sys
import time
import threading
import pyperclip
from dotenv import load_dotenv
from pynput import keyboard
from PyQt6.QtWidgets import QApplication

# Загружаем настройки
load_dotenv()

from core.translator import AIEngine
from ui.window import MiniWindow

API_KEY = os.getenv("GOOGLE_API_KEY")
PROXY_URL = os.getenv("PROXY_URL")
PAUSE_DELAY = float(os.getenv("PAUSE_DELAY", 1.5))

class SmartTranslatorApp:
    def __init__(self):
        if not API_KEY:
            print("ОШИБКА: API KEY не найден")
            sys.exit(1)

        self.app = QApplication(sys.argv)
        
        self.ui = MiniWindow()
        self.ai = AIEngine(API_KEY, proxy_url=PROXY_URL)
        
        self.is_running = False
        self.buffer = ""
        self.last_key_time = time.time()
        
        self.ui.toggle_signal.connect(self.set_active)
        
        # Слушатель клавиатуры
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()
        
        # Поток для отслеживания паузы
        threading.Thread(target=self.check_pause_loop, daemon=True).start()

    def set_active(self, val):
        self.is_running = val
        self.buffer = ""

    def on_press(self, key):
        if not self.is_running:
            return
        try:
            self.last_key_time = time.time()
            if hasattr(key, 'char') and key.char:
                self.buffer += key.char
            elif key == keyboard.Key.space:
                self.buffer += " "
            elif key == keyboard.Key.backspace:
                self.buffer = self.buffer[:-1]
        except:
            pass

    def check_pause_loop(self):
        while True:
            if self.is_running and self.buffer.strip():
                if time.time() - self.last_key_time > PAUSE_DELAY:
                    text_to_process = self.buffer
                    self.buffer = ""
                    threading.Thread(target=self.do_replace, args=(text_to_process,)).start()
            time.sleep(0.1)

    def do_replace(self, text):
        target = "English" if "EN" in self.ui.lang_choice.currentText() else "Russian"
        translated = self.ai.translate_and_fix(text, target)
        
        if translated and not translated.startswith("Error:"):
            controller = keyboard.Controller()
            
            # Стираем старый текст
            for _ in range(len(text)):
                controller.press(keyboard.Key.backspace)
                controller.release(keyboard.Key.backspace)
                time.sleep(0.01)

            # Вставляем перевод
            pyperclip.copy(translated)
            with controller.pressed(keyboard.Key.cmd):
                controller.press('v')
                controller.release('v')

    def run(self):
        self.ui.show()
        sys.exit(self.app.exec())

if __name__ == "__main__":
    main_app = SmartTranslatorApp()
    main_app.run()