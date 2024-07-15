import heapq  # برای استفاده از صف اولویت‌دار

class NPuzzle:
    def __init__(self, start, goal):
        # ماتریس شروع
        self.start = start
        # ماتریس هدف
        self.goal = goal
        # اندازه ماتریس (تعداد سطرها)
        self.n = len(start)

    def heuristic(self, state):
        """محاسبه تابع هزینه فاصله منهتن برای یک حالت."""
        distance = 0  # فاصله اولیه
        # محاسبه فاصله منهتن برای هر کاشی
        for i in range(self.n):
            for j in range(self.n):
                if state[i][j] != 0:  # صرفنظر از خانه خالی
                    x, y = divmod(state[i][j] - 1, self.n)  # محاسبه موقعیت هدف کاشی
                    distance += abs(x - i) + abs(y - j)  # محاسبه فاصله منهتن و اضافه کردن به فاصله کلی
        return distance  # بازگشت فاصله منهتن

    def get_neighbors(self, state):
        """تولید همسایه‌ها با جابجا کردن کاشی‌ها."""
        neighbors = []  # لیست همسایه‌ها
        # پیدا کردن موقعیت خانه خالی
        x, y = [(ix, iy) for ix, row in enumerate(state) for iy, i in enumerate(row) if i == 0][0]
        # جهت‌های ممکن حرکت (بالا، پایین، چپ، راست)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy  # موقعیت جدید بعد از حرکت
            # بررسی محدودیت‌های ماتریس
            if 0 <= nx < self.n and 0 <= ny < self.n:
                # کپی ماتریس جاری
                new_state = [row[:] for row in state]
                # جابجایی خانه خالی با خانه هدف
                new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
                # اضافه کردن حالت جدید به لیست همسایه‌ها
                neighbors.append(new_state)
        return neighbors  # بازگشت لیست همسایه‌ها

    def solve(self):
        """حل پازل n تایی با استفاده از الگوریتم A*."""
        # تبدیل ماتریس شروع به tuple برای استفاده در دیکشنری
        start_tuple = tuple(tuple(row) for row in self.start)
        # تبدیل ماتریس هدف به tuple برای استفاده در دیکشنری
        goal_tuple = tuple(tuple(row) for row in self.goal)
        # صف اولویت‌دار شامل گره شروع با هزینه اولیه
        frontier = [(self.heuristic(self.start), 0, start_tuple, None)]
        # تبدیل لیست به heap
        heapq.heapify(frontier)
        # دیکشنری برای دنبال کردن مسیر از گره‌ها
        came_from = {start_tuple: None}
        # دیکشنری برای نگهداری هزینه تا هر گره
        cost_so_far = {start_tuple: 0}

        # تا زمانی که صف اولویت‌دار خالی نشده است
        while frontier:
            # گرفتن گره با کمترین هزینه
            _, current_cost, current, previous = heapq.heappop(frontier)
            # اگر گره جاری هدف باشد
            if current == goal_tuple:
                path = []  # لیست مسیر
                # بازسازی مسیر از هدف به شروع
                while current:
                    path.append(current)
                    current = came_from[current]
                return path[::-1]  # برعکس کردن مسیر و بازگشت آن

            # پیدا کردن همسایه‌های گره جاری
            for neighbor in self.get_neighbors([list(row) for row in current]):
                # تبدیل همسایه به tuple
                neighbor_tuple = tuple(tuple(row) for row in neighbor)
                # محاسبه هزینه جدید
                new_cost = current_cost + 1
                # بررسی اگر هزینه جدید کمتر است
                if neighbor_tuple not in cost_so_far or new_cost < cost_so_far[neighbor_tuple]:
                    # به‌روزرسانی هزینه
                    cost_so_far[neighbor_tuple] = new_cost
                    # محاسبه اولویت
                    priority = new_cost + self.heuristic(neighbor)
                    # اضافه کردن همسایه به صف
                    heapq.heappush(frontier, (priority, new_cost, neighbor_tuple, current))
                    # به‌روزرسانی مسیر برگشتی
                    came_from[neighbor_tuple] = current
        return None  # اگر مسیر یافت نشد، بازگشت None

# تست پیاده‌سازی
start = [
    [1, 2, 3],  # ماتریس شروع
    [4, 0, 5],
    [7, 8, 6]
]

goal = [
    [1, 2, 3],  # ماتریس هدف
    [4, 5, 6],
    [7, 8, 0]
]
# ساخت شیء NPuzzle با ماتریس‌های شروع و هدف
puzzle = NPuzzle(start, goal)
# حل پازل
solution = puzzle.solve()

# چاپ مراحل حل پازل
for step in solution:
    for row in step:
        print(row)
    print()
    print("next level>>")