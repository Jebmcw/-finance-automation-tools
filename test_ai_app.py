"""
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout,
    QTextEdit, QLabel, QLineEdit
)
import sys
import openai
import os

class AccountingAI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Accounting AI Assistant")
        self.setGeometry(100, 100, 600, 400)

        # Layout and widgets
        layout = QVBoxLayout()

        self.prompt_label = QLabel("Enter your request (e.g. 'Compare GL and AP'):")
        layout.addWidget(self.prompt_label)

        self.prompt_input = QLineEdit()
        layout.addWidget(self.prompt_input)

        self.compare_button = QPushButton("Compare")
        self.compare_button.clicked.connect(self.handle_compare)
        layout.addWidget(self.compare_button)

        self.autocorrect_button = QPushButton("Auto Correct")
        self.autocorrect_button.clicked.connect(self.handle_autocorrect)
        layout.addWidget(self.autocorrect_button)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        self.setLayout(layout)

    def handle_compare(self):
        prompt = self.prompt_input.text()
        result = self.run_openai_prompt(prompt + " (only compare, do not change)")
        self.output.append(f"🧾 Compare result:\n{result}\n")

    def handle_autocorrect(self):
        prompt = self.prompt_input.text()
        result = self.run_openai_prompt(prompt + " (auto correct differences)")
        self.output.append(f"🔧 Auto-correct result:\n{result}\n")

    def run_openai_prompt(self, text):
        openai.api_key = os.getenv("OPENAI_API_KEY")

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",  # or gpt-3.5-turbo
                messages=[
                    {"role": "system", "content": "You are an accounting assistant for reconciling .csv files."},
                    {"role": "user", "content": text}
                ],
                max_tokens=500,
                temperature=0.2
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            return f"[ERROR]: {e}"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AccountingAI()
    window.show()
    sys.exit(app.exec_())



















































"""