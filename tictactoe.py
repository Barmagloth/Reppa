import tkinter as tk

CELL_SIZE = 100
BOARD_SIZE = 3

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=CELL_SIZE*BOARD_SIZE, height=CELL_SIZE*BOARD_SIZE)
        self.canvas.pack()
        self.status = tk.Label(root, text="Turn: X")
        self.status.pack()
        self.restart_btn = tk.Button(root, text="Restart", command=self.restart)
        self.board = [[None]*BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.current_player = 'X'
        self.running = True
        self.draw_grid()
        self.canvas.bind('<Button-1>', self.handle_click)

    def draw_grid(self):
        self.canvas.delete('all')
        for i in range(1, BOARD_SIZE):
            self.canvas.create_line(0, i*CELL_SIZE, CELL_SIZE*BOARD_SIZE, i*CELL_SIZE, width=2)
            self.canvas.create_line(i*CELL_SIZE, 0, i*CELL_SIZE, CELL_SIZE*BOARD_SIZE, width=2)
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                val = self.board[r][c]
                x1, y1 = c*CELL_SIZE, r*CELL_SIZE
                x2, y2 = x1+CELL_SIZE, y1+CELL_SIZE
                if val == 'X':
                    self.canvas.create_line(x1+10, y1+10, x2-10, y2-10, width=2, fill='blue')
                    self.canvas.create_line(x1+10, y2-10, x2-10, y1+10, width=2, fill='blue')
                elif val == 'O':
                    self.canvas.create_oval(x1+10, y1+10, x2-10, y2-10, width=2, outline='red')

    def handle_click(self, event):
        if not self.running:
            return
        row = event.y // CELL_SIZE
        col = event.x // CELL_SIZE
        if row >= BOARD_SIZE or col >= BOARD_SIZE:
            return
        if self.board[row][col] is not None:
            return
        self.board[row][col] = self.current_player
        self.draw_grid()
        if self.check_winner():
            self.running = False
            self.restart_btn.pack()
            return
        if all(all(cell is not None for cell in row) for row in self.board):
            self.status.config(text="It's a tie!")
            self.running = False
            self.restart_btn.pack()
            return
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        self.status.config(text=f"Turn: {self.current_player}")

    def check_winner(self):
        lines = []
        # Rows
        for r in range(BOARD_SIZE):
            lines.append([(r, i) for i in range(BOARD_SIZE)])
        # Columns
        for c in range(BOARD_SIZE):
            lines.append([(i, c) for i in range(BOARD_SIZE)])
        # Diagonals
        lines.append([(i, i) for i in range(BOARD_SIZE)])
        lines.append([(i, BOARD_SIZE-1-i) for i in range(BOARD_SIZE)])
        for line in lines:
            values = [self.board[r][c] for r, c in line]
            if values[0] is not None and all(v == values[0] for v in values):
                self.status.config(text=f"{values[0]} wins!")
                self.draw_win_line(line)
                return True
        return False

    def draw_win_line(self, line):
        r0, c0 = line[0]
        r1, c1 = line[-1]
        x1 = c0*CELL_SIZE + CELL_SIZE//2
        y1 = r0*CELL_SIZE + CELL_SIZE//2
        x2 = c1*CELL_SIZE + CELL_SIZE//2
        y2 = r1*CELL_SIZE + CELL_SIZE//2
        self.canvas.create_line(x1, y1, x2, y2, width=4, fill='green')

    def restart(self):
        self.board = [[None]*BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.current_player = 'X'
        self.status.config(text="Turn: X")
        self.running = True
        self.restart_btn.pack_forget()
        self.draw_grid()

def main():
    root = tk.Tk()
    root.title('Tic Tac Toe')
    game = TicTacToe(root)
    root.mainloop()

if __name__ == '__main__':
    main()
