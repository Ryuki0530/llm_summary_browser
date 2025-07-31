from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QSplitter, QTextEdit
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QUrl# メインウィンドウとUI部品のレイアウト
"""
メインウィンドウのUI設計とレイアウト管理
"""
class MainWindow(QMainWindow):
    def __init__ (self):
        super().__init__()
        # メインウィンドウの初期化
        self.setWindowTitle("LLM Summary Browser")
        self.setGeometry(100, 100, 1200, 800)
        
        # アイコンの設定(未定)
        # self.setWindowIcon(QIcon("icon.png"))

        # URL入力バーの追加
        self.url_bar = QLineEdit()

        # URL入力バーのボタン
        self.go_button = QPushButton("Go")

        # WEBエンジンビューの追加
        self.browser_view = QWebEngineView()
        self.browser_view.setUrl(QUrl("https://www.google.com"))

        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.browser_view)
        self.splitter.setSizes([800, 400])

        
        # 全体レイアウト
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.url_bar)
        main_layout.addWidget(self.go_button)
        main_layout.addWidget(self.splitter)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
