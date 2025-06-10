import tkinter as tk
from tkinter import font

CELL_SIZE = 120
BOARD_SIZE = 3
BG_COLOR = '#2c3e50'
GRID_COLOR = '#ecf0f1'
X_COLOR = '#e74c3c'
O_COLOR = '#3498db'
WIN_LINE_COLOR = '#f39c12'
TEXT_COLOR = '#ecf0f1'


class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)

        # Шрифты
        self.title_font = font.Font(family='Arial', size=24, weight='bold')
        self.status_font = font.Font(family='Arial', size=16)
        self.button_font = font.Font(family='Arial', size=12, weight='bold')

        # Заголовок
        self.title = tk.Label(root, text="🎮 КРЕСТИКИ-НОЛИКИ",
                              font=self.title_font, fg=TEXT_COLOR, bg=BG_COLOR)
        self.title.pack(pady=10)

        # Канвас с рамкой
        canvas_frame = tk.Frame(root, bg=GRID_COLOR, relief='raised', bd=3)
        canvas_frame.pack(pady=10)

        self.canvas = tk.Canvas(canvas_frame, width=CELL_SIZE * BOARD_SIZE,
                                height=CELL_SIZE * BOARD_SIZE, bg=GRID_COLOR,
                                highlightthickness=0)
        self.canvas.pack(padx=3, pady=3)

        # Статус
        self.status = tk.Label(root, text="🎯 Ход: X", font=self.status_font,
                               fg=TEXT_COLOR, bg=BG_COLOR)
        self.status.pack(pady=10)

        # Кнопки
        button_frame = tk.Frame(root, bg=BG_COLOR)
        button_frame.pack(pady=10)

        self.restart_btn = tk.Button(button_frame, text="🔄 Новая игра",
                                     command=self.restart, font=self.button_font,
                                     bg='#27ae60', fg='white', relief='flat',
                                     padx=20, pady=5, cursor='hand2')

        self.quit_btn = tk.Button(button_frame, text="❌ Выход",
                                  command=root.quit, font=self.button_font,
                                  bg='#e74c3c', fg='white', relief='flat',
                                  padx=20, pady=5, cursor='hand2')
        self.quit_btn.pack(side='right', padx=5)

        # Игровое состояние
        self.board = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.current_player = 'X'
        self.running = True
        self.scores = {'X': 0, 'O': 0, 'ties': 0}

        # Счетчик
        self.score_label = tk.Label(root, text=self.get_score_text(),
                                    font=self.status_font, fg=TEXT_COLOR, bg=BG_COLOR)
        self.score_label.pack()

        self.draw_grid()
        self.canvas.bind('<Button-1>', self.handle_click)
        self.canvas.bind('<Motion>', self.handle_hover)

    def get_score_text(self):
        return f"📊 X: {self.scores['X']} | O: {self.scores['O']} | Ничьи: {self.scores['ties']}"

    def draw_grid(self):
        self.canvas.delete('all')

        # Рисуем сетку с тенями
        for i in range(1, BOARD_SIZE):
            # Горизонтальные линии
            self.canvas.create_line(5, i * CELL_SIZE, CELL_SIZE * BOARD_SIZE - 5, i * CELL_SIZE,
                                    width=4, fill='#bdc3c7')
            self.canvas.create_line(3, i * CELL_SIZE - 1, CELL_SIZE * BOARD_SIZE - 3, i * CELL_SIZE - 1,
                                    width=2, fill=BG_COLOR)

            # Вертикальные линии
            self.canvas.create_line(i * CELL_SIZE, 5, i * CELL_SIZE, CELL_SIZE * BOARD_SIZE - 5,
                                    width=4, fill='#bdc3c7')
            self.canvas.create_line(i * CELL_SIZE - 1, 3, i * CELL_SIZE - 1, CELL_SIZE * BOARD_SIZE - 3,
                                    width=2, fill=BG_COLOR)

        # Рисуем фигуры
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                self.draw_cell(r, c)

    def draw_cell(self, row, col):
        val = self.board[row][col]
        x1, y1 = col * CELL_SIZE, row * CELL_SIZE
        x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
        center_x, center_y = x1 + CELL_SIZE // 2, y1 + CELL_SIZE // 2

        if val == 'X':
            # Красивый X с градиентом
            offset = 25
            # Тень
            self.canvas.create_line(center_x - offset + 2, center_y - offset + 2,
                                    center_x + offset + 2, center_y + offset + 2,
                                    width=8, fill='#c0392b', capstyle='round')
            self.canvas.create_line(center_x - offset + 2, center_y + offset + 2,
                                    center_x + offset + 2, center_y - offset + 2,
                                    width=8, fill='#c0392b', capstyle='round')
            # Основные линии
            self.canvas.create_line(center_x - offset, center_y - offset,
                                    center_x + offset, center_y + offset,
                                    width=6, fill=X_COLOR, capstyle='round')
            self.canvas.create_line(center_x - offset, center_y + offset,
                                    center_x + offset, center_y - offset,
                                    width=6, fill=X_COLOR, capstyle='round')

        elif val == 'O':
            # Красивый O с градиентом
            radius = 30
            # Тень
            self.canvas.create_oval(center_x - radius + 2, center_y - radius + 2,
                                    center_x + radius + 2, center_y + radius + 2,
                                    width=6, outline='#2980b9')
            # Основной круг
            self.canvas.create_oval(center_x - radius, center_y - radius,
                                    center_x + radius, center_y + radius,
                                    width=6, outline=O_COLOR)
            # Внутренний блик
            self.canvas.create_oval(center_x - radius + 8, center_y - radius + 8,
                                    center_x + radius - 8, center_y + radius - 8,
                                    width=2, outline='#85c1e9')

    def handle_hover(self, event):
        if not self.running:
            return

        # Подсветка клетки при наведении
        row = event.y // CELL_SIZE
        col = event.x // CELL_SIZE

        if (row < BOARD_SIZE and col < BOARD_SIZE and
                self.board[row][col] is None):
            self.canvas.configure(cursor='hand2')
            # Можно добавить подсветку клетки
        else:
            self.canvas.configure(cursor='arrow')

    def handle_click(self, event):
        if not self.running:
            return

        row = event.y // CELL_SIZE
        col = event.x // CELL_SIZE

        if (row >= BOARD_SIZE or col >= BOARD_SIZE or
                self.board[row][col] is not None):
            return

        # Анимация хода
        self.board[row][col] = self.current_player
        self.draw_cell(row, col)

        if self.check_winner():
            self.scores[self.current_player] += 1
            self.running = False
            self.restart_btn.pack(side='left', padx=5)
            self.score_label.config(text=self.get_score_text())
            return

        if all(all(cell is not None for cell in row) for row in self.board):
            self.status.config(text="🤝 Ничья!")
            self.scores['ties'] += 1
            self.running = False
            self.restart_btn.pack(side='left', padx=5)
            self.score_label.config(text=self.get_score_text())
            return

        self.current_player = 'O' if self.current_player == 'X' else 'X'
        player_emoji = '❌' if self.current_player == 'X' else '⭕'
        self.status.config(text=f"🎯 Ход: {player_emoji} {self.current_player}")

    def check_winner(self):
        lines = []
        # Строки
        for r in range(BOARD_SIZE):
            lines.append([(r, i) for i in range(BOARD_SIZE)])
        # Столбцы
        for c in range(BOARD_SIZE):
            lines.append([(i, c) for i in range(BOARD_SIZE)])
        # Диагонали
        lines.append([(i, i) for i in range(BOARD_SIZE)])
        lines.append([(i, BOARD_SIZE - 1 - i) for i in range(BOARD_SIZE)])

        for line in lines:
            values = [self.board[r][c] for r, c in line]
            if values[0] is not None and all(v == values[0] for v in values):
                winner_emoji = '🎉❌' if values[0] == 'X' else '🎉⭕'
                self.status.config(text=f"{winner_emoji} {values[0]} ПОБЕДИЛ!")
                self.draw_win_line(line)
                return True
        return False

    def draw_win_line(self, line):
        r0, c0 = line[0]
        r1, c1 = line[-1]
        x1 = c0 * CELL_SIZE + CELL_SIZE // 2
        y1 = r0 * CELL_SIZE + CELL_SIZE // 2
        x2 = c1 * CELL_SIZE + CELL_SIZE // 2
        y2 = r1 * CELL_SIZE + CELL_SIZE // 2

        # Анимированная линия победы
        self.canvas.create_line(x1, y1, x2, y2, width=8, fill=WIN_LINE_COLOR,
                                capstyle='round', tags='win_line')
        # Эффект свечения
        self.canvas.create_line(x1, y1, x2, y2, width=12, fill='#f7dc6f',
                                capstyle='round', tags='win_glow')
        self.canvas.tag_lower('win_glow')

    def restart(self):
        self.board = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.current_player = 'X'
        self.status.config(text="🎯 Ход: ❌ X")
        self.running = True
        self.restart_btn.pack_forget()
        self.draw_grid()


def main():
    root = tk.Tk()
    root.title('🎮 Крестики-нолики')

    # Центрируем окно
    window_width = CELL_SIZE * BOARD_SIZE + 50
    window_height = CELL_SIZE * BOARD_SIZE + 200
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f'{window_width}x{window_height}+{x}+{y}')

    game = TicTacToe(root)
    root.mainloop()


if __name__ == '__main__':
    main()