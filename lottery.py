import ttkbootstrap as tk
import random
import time

class LotteryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("抽奖程序")
        
        self.title_label = tk.Label(root, text="抽奖程序", font=("Helvetica", 20))
        self.title_label.pack(pady=20)
        
        self.scroll_label = tk.Label(root, text="", font=("Helvetica", 16))
        self.scroll_label.pack()
        
        self.start_button = tk.Button(root, text="开始抽奖", command=self.start_lottery)
        self.start_button.pack(pady=20)
        
        self.winner_label = tk.Label(root, text="已中奖参与者：", font=("Helvetica", 14))
        self.winner_label.pack()
        
        self.winner_list = tk.Label(root, text="", font=("Helvetica", 12))
        self.winner_list.pack()
        
        self.prizes = ["奖项1", "奖项2", "奖项3", "奖项4", "奖项5"]
        self.lottery_counts = [3, 5, 2, 4, 1]  # 每个奖项的抽奖次数
        self.current_prize_index = 0
        self.current_lottery_count = self.lottery_counts[self.current_prize_index]
        self.participants = ["参与者1", "参与者2", "参与者3", "参与者4", "参与者5"]
        self.winner = None
        self.is_lottery_running = False
        self.all_winners = []

    def start_lottery(self):
        if not self.is_lottery_running:
            self.is_lottery_running = True
            self.start_button.config(text="停止抽奖", command=self.stop_lottery)
            self.scroll_label.config(text="")
            self.scroll_lottery()
        else:
            self.is_lottery_running = False
            self.start_button.config(text="开始抽奖", command=self.start_lottery)
            self.current_lottery_count = self.lottery_counts[self.current_prize_index]
            if self.winner:
                self.scroll_label.config(text=f"恭喜 {self.winner} 中奖！")
                self.participants.remove(self.winner)
                self.all_winners.append(self.winner)
                self.update_winner_list()
                self.winner = None

    def stop_lottery(self):
        if self.is_lottery_running:
            self.is_lottery_running = False
            self.start_button.config(text="开始抽奖", command=self.start_lottery)
            self.current_lottery_count = self.lottery_counts[self.current_prize_index]
            if self.participants:
                self.winner = random.choice(self.participants)
                self.scroll_label.config(text=f"恭喜 {self.winner} 中奖！")
                self.participants.remove(self.winner)
                self.all_winners.append(self.winner)
                self.update_winner_list()
                self.lottery_counts[self.current_prize_index] -= 1
                if self.lottery_counts[self.current_prize_index] == 0:
                    self.current_prize_index = (self.current_prize_index + 1) % len(self.prizes)
                    self.current_lottery_count = self.lottery_counts[self.current_prize_index]
                    if self.current_lottery_count == 0:
                        self.scroll_label.config(text="所有奖项抽完啦！")
                else:
                    self.scroll_label.config(text=f"{self.prizes[self.current_prize_index]} 剩余 {self.current_lottery_count} 次")
            else:
                self.scroll_label.config(text="没有更多参与者了")
        else:
            self.scroll_label.config(text="")

    def scroll_lottery(self):
        if self.is_lottery_running:
            random.shuffle(self.participants)
            self.scroll_label.config(text="正在抽奖中...")
            for participant in self.participants:
                if not self.is_lottery_running:
                    break
                self.scroll_label.config(text=participant)
                self.root.update()
                time.sleep(0.2)
            self.stop_lottery()
        else:
            self.scroll_label.config("")

    def update_winner_list(self):
        winner_text = "\n".join(self.all_winners)
        self.winner_list.config(text=winner_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = LotteryApp(root)
    root.mainloop()
