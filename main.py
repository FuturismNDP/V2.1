import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sys
import re



class DuplicateRemover:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        
        # Tạo main frame
        main_frame = ttk.Frame(parent_frame, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Cấu hình grid weight
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Tạo frame cho settings với kích thước lớn hơn
        settings_frame = ttk.LabelFrame(main_frame, text="Cài Đặt", padding="2")
        settings_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0,10))
        
        # Tạo style cho checkbox lớn hơn
        style = ttk.Style()
        style.configure("Large.TCheckbutton", font=("Arial", 11))
        # Thử map indicatorsize (có thể không work trên mọi theme)
        try:
              style.map("Large.TCheckbutton",
              indicatorsize=[('', 15)])
        except:
         pass
        
        # Tạo 2 hàng cho settings
        settings_row1 = ttk.Frame(settings_frame)
        settings_row1.pack(fill=tk.X, pady=(0, 5))
        
        settings_row2 = ttk.Frame(settings_frame)
        settings_row2.pack(fill=tk.X)
        
        # Hàng 1: Các cài đặt cũ
        # Checkbox để bật/tắt tính năng thêm dấu phẩy - kích thước lớn hơn
        self.add_comma_var = tk.BooleanVar(value=False)
        self.comma_checkbox = ttk.Checkbutton(
            settings_row1, 
            text="Thêm dấu phẩy ở cuối mỗi dòng trong kết quả", 
            variable=self.add_comma_var,
            command=self.on_setting_change,
            style="Large.TCheckbutton")
        self.comma_checkbox.pack(side=tk.LEFT, padx=(0, 50), pady=5)
        
        # Checkbox để loại bỏ khoảng trắng thừa - kích thước lớn hơn
        self.trim_spaces_var = tk.BooleanVar(value=True)
        self.spaces_checkbox = ttk.Checkbutton(
            settings_row1, 
            text="Loại bỏ khoảng trắng thừa", 
            variable=self.trim_spaces_var,
            command=self.on_setting_change,
            style="Large.TCheckbutton")
        self.spaces_checkbox.pack(side=tk.LEFT, padx=(0, 50), pady=5)
        
        # Checkbox để bỏ qua dòng trống - kích thước lớn hơn
        self.ignore_empty_var = tk.BooleanVar(value=True)
        self.empty_checkbox = ttk.Checkbutton(
            settings_row1, 
            text="Bỏ qua dòng trống", 
            variable=self.ignore_empty_var,
            command=self.on_setting_change,
            style="Large.TCheckbutton")
        self.empty_checkbox.pack(side=tk.LEFT, pady=5)
        
        # Hàng 2: Cài đặt VIDs
        self.vids_var = tk.BooleanVar(value=True)
        self.vids_checkbox = ttk.Checkbutton(
            settings_row2, 
            text="VIDs (Chỉ xử lý items ≥ 10 ký tự)", 
            variable=self.vids_var,
            command=self.on_setting_change,
            style="Large.TCheckbutton")
        self.vids_checkbox.pack(side=tk.LEFT, pady=5)
        
        # Tạo frame cho labels với counter và nút clear
        label_frame1 = ttk.Frame(main_frame)
        label_frame1.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=(0, 5), pady=(0, 5))
        
        label_frame2 = ttk.Frame(main_frame)
        label_frame2.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 5), pady=(0, 5))
        
        label_frame3 = ttk.Frame(main_frame)
        label_frame3.grid(row=1, column=2, sticky=(tk.W, tk.E), padx=(5, 0), pady=(0, 5))
        
        # Tạo labels với counter và nút clear
        # Frame 1
        left_part1 = ttk.Frame(label_frame1)
        left_part1.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Label(left_part1, text="Danh sách 1:", font=("Arial", 11, "")).pack(side=tk.LEFT)
        self.count_label1 = tk.Label(left_part1, text="(0)", 
                                   font=("Arial", 16, "bold"), fg="red")
        self.count_label1.pack(side=tk.LEFT, padx=(5, 0))
        
        self.clear_btn1 = ttk.Button(label_frame1, text="Clear", 
                                    command=self.clear_list1, style="Small.TButton")
        self.clear_btn1.pack(side=tk.RIGHT)
        
        # Frame 2
        left_part2 = ttk.Frame(label_frame2)
        left_part2.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Label(left_part2, text="Danh sách 2:", font=("Arial", 11, "")).pack(side=tk.LEFT)
        self.count_label2 = tk.Label(left_part2, text="(0)", 
                                   font=("Arial", 16, "bold"), fg="red")
        self.count_label2.pack(side=tk.LEFT, padx=(5, 0))
        
        self.clear_btn2 = ttk.Button(label_frame2, text="Clear", 
                                    command=self.clear_list2, style="Small.TButton")
        self.clear_btn2.pack(side=tk.RIGHT)
        
        # Frame 3 - KẾT QUẢ với Radio buttons
        left_part3 = ttk.Frame(label_frame3)
        left_part3.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Label và counter
        result_info_frame = ttk.Frame(left_part3)
        result_info_frame.pack(side=tk.LEFT)
        
        ttk.Label(result_info_frame, text="Kết quả:", font=("Arial", 11, "")).pack(side=tk.LEFT)
        self.count_label3 = tk.Label(result_info_frame, text="(0)", 
                                   font=("Arial", 16, "bold"), fg="red")
        self.count_label3.pack(side=tk.LEFT, padx=(5, 0))
        
        # Radio buttons cho kết quả
        self.result_type_var = tk.StringVar(value="unique")
        
        radio_frame = ttk.Frame(left_part3)
        radio_frame.pack(side=tk.LEFT, padx=(15, 0))
        
        self.unique_radio = ttk.Radiobutton(
            radio_frame, 
            text="Không trùng lặp", 
            variable=self.result_type_var, 
            value="unique",
            command=self.on_result_type_change,
            style="Custom.TRadiobutton")
        self.unique_radio.pack(side=tk.LEFT, padx=(0, 10))
        
        self.duplicate_radio = ttk.Radiobutton(
            radio_frame, 
            text="Trùng lặp", 
            variable=self.result_type_var, 
            value="duplicate",
            command=self.on_result_type_change,
            style="Custom.TRadiobutton")
        self.duplicate_radio.pack(side=tk.LEFT)
        
        # Tạo text areas
        self.text1 = scrolledtext.ScrolledText(
            main_frame, wrap=tk.WORD, width=35, height=25,
            font=("Consolas", 10))
        self.text1.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), 
                       padx=(0, 5), pady=(0, 10))
        
        self.text2 = scrolledtext.ScrolledText(
            main_frame, wrap=tk.WORD, width=35, height=25,
            font=("Consolas", 10))
        self.text2.grid(row=2, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), 
                       padx=(5, 5), pady=(0, 10))
        
        self.text3 = scrolledtext.ScrolledText(
            main_frame, wrap=tk.WORD, width=35, height=25,
            font=("Consolas", 10), state=tk.DISABLED)
        self.text3.grid(row=2, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), 
                       padx=(5, 0), pady=(0, 10))
        
        # Cấu hình tags cho màu sắc
        self.text1.tag_configure("duplicate", foreground="#FF8C00")  # Màu cam nhẹ cho trùng lặp giữa 2 danh sách
        self.text2.tag_configure("duplicate", foreground="#FF8C00")  # Màu cam nhẹ cho trùng lặp giữa 2 danh sách
        self.text1.tag_configure("internal_duplicate", foreground="#FF4500")  # Màu cam đậm cho trùng lặp trong cùng danh sách
        self.text2.tag_configure("internal_duplicate", foreground="#FF4500")  # Màu cam đậm cho trùng lặp trong cùng danh sách
        
        # Tạo frame cho buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=10)
        
        # Tạo buttons
        self.remove_btn = ttk.Button(
            button_frame, text="Process Data", 
            command=self.process_data,
            style="Accent.TButton")
        self.remove_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_btn = ttk.Button(
            button_frame, text="Clear All", 
            command=self.clear_all)
        self.clear_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.copy_btn = ttk.Button(
            button_frame, text="Copy Result", 
            command=self.copy_result)
        self.copy_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.preview_btn = ttk.Button(
            button_frame, text="Preview Processing", 
            command=self.preview_processing)
        self.preview_btn.pack(side=tk.LEFT)
        
        # Biến để lưu kết quả xử lý
        self.processed_unique_items = []
        self.processed_duplicate_items = []
        
        # Thêm placeholder text
        self.add_placeholder_text()
        
        # Bind events để tự động cập nhật counter và highlight khi nhập
        self.text1.bind('<KeyRelease>', lambda e: self.on_text_change())
        self.text1.bind('<Button-1>', lambda e: main_frame.after(10, self.on_text_change))
        self.text1.bind('<ButtonRelease-1>', lambda e: self.on_text_change())
        self.text1.bind('<Control-v>', lambda e: main_frame.after(10, self.on_text_change))
        
        self.text2.bind('<KeyRelease>', lambda e: self.on_text_change())
        self.text2.bind('<Button-1>', lambda e: main_frame.after(10, self.on_text_change))
        self.text2.bind('<ButtonRelease-1>', lambda e: self.on_text_change())
        self.text2.bind('<Control-v>', lambda e: main_frame.after(10, self.on_text_change))
        
        # Bind events cho tự động xuống dòng khi có dấu phẩy (KHÔNG GIỮ DẤU PHẨY)
        self.text1.bind('<KeyPress>', lambda e: self.handle_comma_input(e, self.text1))
        self.text2.bind('<KeyPress>', lambda e: self.handle_comma_input(e, self.text2))
        
        # Bind paste events cho tự động xử lý dấu phẩy (KHÔNG GIỮ DẤU PHẨY)
        self.text1.bind('<Control-v>', lambda e: self.handle_paste(e, self.text1))
        self.text2.bind('<Control-v>', lambda e: self.handle_paste(e, self.text2))
        
        # Cập nhật counter ban đầu
        self.update_all_counters()
    
    def handle_comma_input(self, event, text_widget):
        """Xử lý khi người dùng nhập dấu phẩy - tự động xuống dòng KHÔNG GIỮ DẤU PHẨY"""
        if event.char == ',':
            # Lấy vị trí con trỏ hiện tại
            current_pos = text_widget.index(tk.INSERT)
            
            # Lấy nội dung dòng hiện tại
            line_start = current_pos.split('.')[0] + '.0'
            line_end = current_pos.split('.')[0] + '.end'
            current_line = text_widget.get(line_start, line_end)
            
            # Nếu dòng hiện tại không trống, chỉ xuống dòng (không thêm dấu phẩy)
            if current_line.strip():
                text_widget.insert(tk.INSERT, '\n')
                # Ngăn không cho dấu phẩy được thêm vào
                return 'break'
    
    def handle_paste(self, event, text_widget):
        """Xử lý khi paste nội dung có dấu phẩy - KHÔNG GIỮ DẤU PHẨY"""
        try:
            # Lấy nội dung từ clipboard
            clipboard_content = self.parent_frame.clipboard_get()
            
            # Kiểm tra nếu có dấu phẩy
            if ',' in clipboard_content:
                # Thay thế dấu phẩy bằng xuống dòng (không giữ dấu phẩy)
                processed_content = clipboard_content.replace(',', '\n')
                
                # Xóa các dòng trống thừa
                lines = processed_content.split('\n')
                cleaned_lines = []
                for line in lines:
                    cleaned_line = line.strip()
                    if cleaned_line:  # Chỉ giữ lại dòng có nội dung
                        cleaned_lines.append(cleaned_line)
                
                final_content = '\n'.join(cleaned_lines)
                
                # Chèn nội dung đã xử lý
                text_widget.insert(tk.INSERT, final_content)
                
                # Cập nhật counter và highlight sau khi paste
                self.parent_frame.after(10, self.on_text_change)
                
                # Ngăn không cho paste mặc định
                return 'break'
        except tk.TclError:
            # Clipboard trống hoặc lỗi
            pass
    
    def parse_items_from_text(self, text_content):
        """Phân tích và trích xuất các items từ text"""
        if not text_content:
            return []
        
        items = []
        lines = text_content.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            items.append(line)
        
        return items
    
    def clean_line_for_processing(self, line):
        """Làm sạch một dòng ĐỂ XỬ LÝ/SO SÁNH"""
        if not line:
            return line
            
        # Chỉ loại bỏ khoảng trắng thừa nếu được bật
        if self.trim_spaces_var.get():
            line = line.strip()
        
        return line
    
    def format_line_for_result(self, line):
        """Format một dòng CHỈ CHO KẾT QUẢ - thêm hoặc không thêm dấu phẩy"""
        if not line:
            return line
            
        # Loại bỏ khoảng trắng thừa nếu được bật
        if self.trim_spaces_var.get():
            line = line.strip()
        
        # Thêm dấu phẩy ở cuối nếu được bật
        if self.add_comma_var.get():
            if not line.endswith(','):
                line = line + ','
        
        return line
    
    def process_text(self, text_content):
        """Xử lý text theo các cài đặt - trả về danh sách items đã được làm sạch ĐỂ XỬ LÝ"""
        if not text_content:
            return []
        
        # Lấy tất cả items từ text
        items = self.parse_items_from_text(text_content)
        processed_items = []
        
        for item in items:
            cleaned_item = self.clean_line_for_processing(item)
            
            # Bỏ qua item trống nếu được bật
            if self.ignore_empty_var.get() and not cleaned_item:
                continue
            
            # Kiểm tra điều kiện VIDs nếu được bật
            if self.vids_var.get():
                if len(cleaned_item) < 10:
                    continue  # Bỏ qua items có ít hơn 10 ký tự
                
            processed_items.append(cleaned_item)
        
        return processed_items
    
    def remove_duplicates_from_list(self, items):
        """Loại bỏ duplicate trong một danh sách, giữ lại phần tử đầu tiên"""
        seen = set()
        unique_items = []
        
        for item in items:
            if item not in seen:
                seen.add(item)
                unique_items.append(item)
        
        return unique_items
    
    def find_internal_duplicates(self, items):
        """Tìm các items trùng lặp trong cùng một danh sách"""
        seen = set()
        duplicates = set()
        
        for item in items:
            if item in seen:
                duplicates.add(item)
            else:
                seen.add(item)
        
        return duplicates
    
    def count_items_in_text(self, text_widget):
        """Đếm số items có nội dung trong text widget"""
        try:
            content = text_widget.get("1.0", tk.END).strip()
            if not content:
                return 0
            
            # Đếm số items thực tế
            items = self.parse_items_from_text(content)
            
            # Áp dụng cài đặt để đếm chính xác
            processed_items = []
            for item in items:
                cleaned_item = self.clean_line_for_processing(item)
                # Bỏ qua item trống nếu được bật
                if self.ignore_empty_var.get() and not cleaned_item:
                    continue
                
                # Kiểm tra điều kiện VIDs nếu được bật
                if self.vids_var.get():
                    if len(cleaned_item) < 10:
                        continue  # Bỏ qua items có ít hơn 10 ký tự
                
                processed_items.append(cleaned_item)
            
            return len(processed_items)
        except:
            return 0
    
    def update_counter(self, text_number):
        """Cập nhật counter cho text area cụ thể"""
        try:
            if text_number == 1:
                count = self.count_items_in_text(self.text1)
                self.count_label1.config(text=f"({count})")
            elif text_number == 2:
                count = self.count_items_in_text(self.text2)
                self.count_label2.config(text=f"({count})")
            elif text_number == 3:
                # Đếm theo loại kết quả hiện tại
                if self.result_type_var.get() == "unique":
                    count = len(self.processed_unique_items)
                else:
                    count = len(self.processed_duplicate_items)
                self.count_label3.config(text=f"({count})")
        except:
            pass
    
    def update_all_counters(self):
        """Cập nhật tất cả counters"""
        self.update_counter(1)
        self.update_counter(2)
        self.update_counter(3)
    
    def highlight_duplicates(self):
        """Highlight các items trùng lặp"""
        try:
            # Lấy nội dung từ hai text area
            content1 = self.text1.get("1.0", tk.END).strip()
            content2 = self.text2.get("1.0", tk.END).strip()
            
            # Xóa highlight cũ
            self.text1.tag_remove("duplicate", "1.0", tk.END)
            self.text2.tag_remove("duplicate", "1.0", tk.END)
            self.text1.tag_remove("internal_duplicate", "1.0", tk.END)
            self.text2.tag_remove("internal_duplicate", "1.0", tk.END)
            
            # Xử lý danh sách 1
            if content1:
                items1 = self.process_text(content1)
                internal_duplicates1 = self.find_internal_duplicates(items1)
                self.highlight_items_in_widget(self.text1, content1, internal_duplicates1, "internal_duplicate")
            
            # Xử lý danh sách 2
            if content2:
                items2 = self.process_text(content2)
                internal_duplicates2 = self.find_internal_duplicates(items2)
                self.highlight_items_in_widget(self.text2, content2, internal_duplicates2, "internal_duplicate")
            
            # Highlight trùng lặp giữa hai danh sách
            if content1 and content2:
                items1 = self.process_text(content1)
                items2 = self.process_text(content2)
                
                # Loại bỏ duplicate trong từng danh sách trước
                unique_items1 = self.remove_duplicates_from_list(items1)
                unique_items2 = self.remove_duplicates_from_list(items2)
                
                # Tìm các items trùng lặp giữa hai danh sách
                set1 = set(unique_items1)
                set2 = set(unique_items2)
                cross_duplicates = set1 & set2
                
                if cross_duplicates:
                    # Highlight trong text1
                    self.highlight_items_in_widget(self.text1, content1, cross_duplicates, "duplicate")
                    # Highlight trong text2
                    self.highlight_items_in_widget(self.text2, content2, cross_duplicates, "duplicate")
                
        except Exception as e:
            print(f"Error highlighting duplicates: {e}")
    
    def highlight_items_in_widget(self, text_widget, content, duplicates, tag_name):
        """Highlight các items cụ thể trong text widget"""
        try:
            lines = content.split('\n')
            line_number = 1
            
            for line in lines:
                line = line.strip()
                if not line:
                    line_number += 1
                    continue
                
                cleaned_line = self.clean_line_for_processing(line)
                
                # Kiểm tra điều kiện VIDs nếu được bật
                if self.vids_var.get():
                    if len(cleaned_line) < 10:
                        line_number += 1
                        continue  # Bỏ qua items có ít hơn 10 ký tự
                
                if cleaned_line in duplicates:
                    start_pos = f"{line_number}.0"
                    end_pos = f"{line_number}.end"
                    text_widget.tag_add(tag_name, start_pos, end_pos)
                
                line_number += 1
                
        except Exception as e:
            print(f"Error highlighting items: {e}")
    
    def clear_results(self):
        """Xóa kết quả xử lý"""
        self.processed_unique_items = []
        self.processed_duplicate_items = []
        
        # Xóa nội dung kết quả
        self.text3.config(state=tk.NORMAL)
        self.text3.delete("1.0", tk.END)
        self.text3.config(state=tk.DISABLED)
        
        # Cập nhật counter
        self.update_counter(3)
    
    def clear_list1(self):
        """Xóa nội dung danh sách 1"""
        self.text1.delete("1.0", tk.END)
        # Xóa highlight
        self.text1.tag_remove("duplicate", "1.0", tk.END)
        self.text1.tag_remove("internal_duplicate", "1.0", tk.END)
        
        # Xóa kết quả xử lý
        self.clear_results()
        
        # Cập nhật counter và highlight
        self.update_counter(1)
        self.parent_frame.after(10, self.highlight_duplicates)
    
    def clear_list2(self):
        """Xóa nội dung danh sách 2"""
        self.text2.delete("1.0", tk.END)
        # Xóa highlight
        self.text2.tag_remove("duplicate", "1.0", tk.END)
        self.text2.tag_remove("internal_duplicate", "1.0", tk.END)
        
        # Xóa kết quả xử lý
        self.clear_results()
        
        # Cập nhật counter và highlight
        self.update_counter(2)
        self.parent_frame.after(10, self.highlight_duplicates)
    
    def on_result_type_change(self):
        """Xử lý khi thay đổi loại kết quả hiển thị"""
        self.display_current_result()
        self.update_counter(3)
    
    def display_current_result(self):
        """Hiển thị kết quả theo loại được chọn"""
        try:
            self.text3.config(state=tk.NORMAL)
            self.text3.delete("1.0", tk.END)
            
            if self.result_type_var.get() == "unique":
                # Hiển thị items không trùng lặp
                if self.processed_unique_items:
                    formatted_items = []
                    for item in self.processed_unique_items:
                        formatted_item = self.format_line_for_result(item)
                        formatted_items.append(formatted_item)
                    self.text3.insert("1.0", '\n'.join(formatted_items))
                else:
                    self.text3.insert("1.0", "Chưa có dữ liệu. Nhấn 'Process Data' để xử lý.")
            else:
                # Hiển thị items trùng lặp
                if self.processed_duplicate_items:
                    formatted_items = []
                    for item in self.processed_duplicate_items:
                        formatted_item = self.format_line_for_result(item)
                        formatted_items.append(formatted_item)
                    self.text3.insert("1.0", '\n'.join(formatted_items))
                else:
                    self.text3.insert("1.0", "Không có items trùng lặp hoặc chưa xử lý dữ liệu.")
            
            self.text3.config(state=tk.DISABLED)
        except Exception as e:
            print(f"Error displaying result: {e}")
    
    def on_text_change(self):
        """Xử lý khi text thay đổi"""
        self.update_all_counters()
        # Delay một chút để tránh lag khi gõ nhanh
        self.parent_frame.after(300, self.highlight_duplicates)
    
    def on_setting_change(self):
        """Xử lý khi cài đặt thay đổi"""
        # Cập nhật lại counters và highlight khi cài đặt thay đổi
        self.update_all_counters()
        self.highlight_duplicates()
        # Cập nhật hiển thị kết quả với format mới
        self.display_current_result()
        
    def add_placeholder_text(self):
        """Thêm text mẫu để hướng dẫn sử dụng"""
        placeholder1 = """

"""
        
        placeholder2 = """


"""
        
        self.text1.insert("1.0", placeholder1)
        self.text2.insert("1.0", placeholder2)
        
        # Bind events để xóa placeholder khi click
        self.text1.bind("<FocusIn>", lambda e: self.clear_placeholder(self.text1, placeholder1))
        self.text2.bind("<FocusIn>", lambda e: self.clear_placeholder(self.text2, placeholder2))
        
        # Cập nhật counter sau khi thêm placeholder
        self.parent_frame.after(100, self.update_all_counters)
    
    def clear_placeholder(self, text_widget, placeholder):
        """Xóa placeholder text khi user bắt đầu nhập"""
        current_content = text_widget.get("1.0", tk.END).strip()
        if current_content == placeholder.strip():
            text_widget.delete("1.0", tk.END)
            # Cập nhật counter sau khi xóa placeholder
            self.parent_frame.after(10, self.update_all_counters)
    
    def preview_processing(self):
        """Hiển thị preview của việc xử lý dữ liệu"""
        try:
            content1 = self.text1.get("1.0", tk.END).strip()
            content2 = self.text2.get("1.0", tk.END).strip()
            
            if not content1 and not content2:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập dữ liệu để preview!")
                return
            
            # Xử lý dữ liệu
            items1 = self.process_text(content1) if content1 else []
            items2 = self.process_text(content2) if content2 else []
            
            # Tìm internal duplicates
            internal_duplicates1 = self.find_internal_duplicates(items1) if items1 else set()
            internal_duplicates2 = self.find_internal_duplicates(items2) if items2 else set()
            
            # Loại bỏ duplicate trong từng danh sách
            unique_items1 = self.remove_duplicates_from_list(items1) if items1 else []
            unique_items2 = self.remove_duplicates_from_list(items2) if items2 else []
            
            # Tìm duplicates giữa hai danh sách (nếu có cả 2 danh sách)
            cross_duplicates = set()
            if unique_items1 and unique_items2:
                set1 = set(unique_items1)
                set2 = set(unique_items2)
                cross_duplicates = set1 & set2
            
            # Tạo cửa sổ preview
            preview_window = tk.Toplevel(self.parent_frame)
            preview_window.title("Preview Processing - VNAT Def-Met")
            preview_window.geometry("1000x800")
            preview_window.transient(self.parent_frame.winfo_toplevel())
            
            # Tạo notebook để hiển thị tabs
            notebook = ttk.Notebook(preview_window)
            notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Tab 1: Danh sách 1 đã xử lý
            if items1:
                frame1 = ttk.Frame(notebook)
                notebook.add(frame1, text=f"Danh sách 1 ({len(items1)} → {len(unique_items1)} items)")
                text_preview1 = scrolledtext.ScrolledText(frame1, wrap=tk.WORD, font=("Consolas", 10))
                text_preview1.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
                text_preview1.tag_configure("cross_duplicate", foreground="#FF8C00", font=("Consolas", 10, "bold"))
                text_preview1.tag_configure("internal_duplicate", foreground="#FF4500", font=("Consolas", 10, "bold"))
                
                # Thêm nội dung và highlight - ÁP DỤNG FORMAT CHO PREVIEW
                seen1 = set()
                for item in items1:
                    display_item = self.format_line_for_result(item)  # Áp dụng format dấu phẩy
                    if item in internal_duplicates1:
                        if item not in seen1:
                            text_preview1.insert(tk.END, display_item + '\n', "internal_duplicate")
                            seen1.add(item)
                    elif item in cross_duplicates:
                        text_preview1.insert(tk.END, display_item + '\n', "cross_duplicate")
                    else:
                        text_preview1.insert(tk.END, display_item + '\n')
                text_preview1.config(state=tk.DISABLED)
            
            # Tab 2: Danh sách 2 đã xử lý
            if items2:
                frame2 = ttk.Frame(notebook)
                notebook.add(frame2, text=f"Danh sách 2 ({len(items2)} → {len(unique_items2)} items)")
                text_preview2 = scrolledtext.ScrolledText(frame2, wrap=tk.WORD, font=("Consolas", 10))
                text_preview2.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
                text_preview2.tag_configure("cross_duplicate", foreground="#FF8C00", font=("Consolas", 10, "bold"))
                text_preview2.tag_configure("internal_duplicate", foreground="#FF4500", font=("Consolas", 10, "bold"))
                
                # Thêm nội dung và highlight - ÁP DỤNG FORMAT CHO PREVIEW
                seen2 = set()
                for item in items2:
                    display_item = self.format_line_for_result(item)  # Áp dụng format dấu phẩy
                    if item in internal_duplicates2:
                        if item not in seen2:
                            text_preview2.insert(tk.END, display_item + '\n', "internal_duplicate")
                            seen2.add(item)
                    elif item in cross_duplicates:
                        text_preview2.insert(tk.END, display_item + '\n', "cross_duplicate")
                    else:
                        text_preview2.insert(tk.END, display_item + '\n')
                text_preview2.config(state=tk.DISABLED)
            
            # Thông tin thống kê
            info_text = f"""
Thống kê xử lý:
- Danh sách 1: {len(items1)} items gốc → {len(unique_items1)} items unique
- Danh sách 2: {len(items2)} items gốc → {len(unique_items2)} items unique
- Duplicate trong danh sách 1: {len(internal_duplicates1)} loại
- Duplicate trong danh sách 2: {len(internal_duplicates2)} loại
- Duplicate giữa 2 danh sách: {len(cross_duplicates)} items
- VIDs (≥10 ký tự): {'Bật' if self.vids_var.get() else 'Tắt'}
- Thêm dấu phẩy vào kết quả: {'Bật' if self.add_comma_var.get() else 'Tắt'}
- Loại bỏ khoảng trắng: {'Bật' if self.trim_spaces_var.get() else 'Tắt'}
- Bỏ qua item trống: {'Bật' if self.ignore_empty_var.get() else 'Tắt'}

Chú thích màu sắc:
- Màu cam nhạt (#FF8C00): Item trùng lặp giữa hai danh sách
- Màu cam đậm (#FF4500): Item trùng lặp trong cùng danh sách (chỉ hiện lần đầu)
- Màu đen: Item không trùng lặp

Quy trình xử lý:
1. Phân tích items từ text (mỗi dòng 1 item, không có dấu phẩy)
2. Áp dụng bộ lọc VIDs nếu được bật (≥10 ký tự)
3. Loại bỏ duplicate trong từng danh sách (giữ lại 1 cá thể)
4. So sánh hai danh sách đã được làm sạch (nếu có cả 2)
5. Tạo 2 kết quả: Không trùng lặp và Trùng lặp
6. Áp dụng format dấu phẩy CHỈ CHO KẾT QUẢ

Tính năng mới:
- Radio buttons để chọn hiển thị "Không trùng lặp" hoặc "Trùng lặp"
- Danh sách gốc không có dấu phẩy (chỉ xuống dòng)
- Thêm/bỏ dấu phẩy chỉ áp dụng cho kết quả theo cài đặt
- VIDs: Chỉ xử lý items có ≥10 ký tự
- Hỗ trợ xử lý từng danh sách riêng biệt

Developed by: VNAT Def-Met/nguyen, dinh phuong
Version: 1.7
"""
            
            # Tab 3: Thông tin
            frame3 = ttk.Frame(notebook)
            notebook.add(frame3, text="Thông tin")
            info_label = tk.Label(frame3, text=info_text, justify=tk.LEFT, font=("Arial", 10))
            info_label.pack(padx=10, pady=10, anchor=tk.W)
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi preview: {str(e)}")
    
    def process_data(self):
        """Xử lý dữ liệu và tạo cả 2 loại kết quả - HỖ TRỢ TỪNG DANH SÁCH RIÊNG BIỆT"""
        try:
            # Lấy nội dung từ hai text area
            content1 = self.text1.get("1.0", tk.END).strip()
            content2 = self.text2.get("1.0", tk.END).strip()
            
            if not content1 and not content2:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập dữ liệu vào ít nhất một trong hai ô!")
                return
            
            # Xử lý dữ liệu theo cài đặt
            items1 = self.process_text(content1) if content1 else []
            items2 = self.process_text(content2) if content2 else []
            
            # Đếm duplicate ban đầu
            original_count1 = len(items1)
            original_count2 = len(items2)
            internal_duplicates1 = len(items1) - len(set(items1)) if items1 else 0
            internal_duplicates2 = len(items2) - len(set(items2)) if items2 else 0
            
            # Loại bỏ duplicate trong từng danh sách trước (giữ lại 1 cá thể)
            unique_items1 = self.remove_duplicates_from_list(items1) if items1 else []
            unique_items2 = self.remove_duplicates_from_list(items2) if items2 else []
            
            # XỬ LÝ THEO TRƯỜNG HỢP
            if content1 and content2:
                # CÓ CẢ 2 DANH SÁCH - xử lý như cũ
                set1 = set(unique_items1)
                set2 = set(unique_items2)
                
                # Tìm các phần tử không trùng lặp (có trong một set nhưng không có trong set kia)
                unique_to_1 = set1 - set2
                unique_to_2 = set2 - set1
                
                # Tìm các phần tử trùng lặp (có trong cả hai set)
                duplicate_items = set1 & set2
                
                # Lưu kết quả vào biến class
                self.processed_unique_items = sorted(list(unique_to_1) + list(unique_to_2))
                self.processed_duplicate_items = sorted(list(duplicate_items))
                
                cross_duplicates_count = len(duplicate_items)
                
            elif content1:
                # CHỈ CÓ DANH SÁCH 1
                # Tất cả items unique trong danh sách 1 đều là "không trùng lặp"
                self.processed_unique_items = sorted(unique_items1)
                # Items trùng lặp là những items xuất hiện nhiều lần trong danh sách 1
                internal_dups1 = self.find_internal_duplicates(items1)
                self.processed_duplicate_items = sorted(list(internal_dups1))
                
                cross_duplicates_count = 0
                
            elif content2:
                # CHỈ CÓ DANH SÁCH 2
                # Tất cả items unique trong danh sách 2 đều là "không trùng lặp"
                self.processed_unique_items = sorted(unique_items2)
                # Items trùng lặp là những items xuất hiện nhiều lần trong danh sách 2
                internal_dups2 = self.find_internal_duplicates(items2)
                self.processed_duplicate_items = sorted(list(internal_dups2))
                
                cross_duplicates_count = 0
            
            # Hiển thị kết quả theo loại được chọn
            self.display_current_result()
            
            # Cập nhật counter cho kết quả
            self.update_counter(3)
            
            # Thông tin chi tiết
            vids_status = "Bật (≥10 ký tự)" if self.vids_var.get() else "Tắt (mọi ký tự)"
            comma_status = "Bật (thêm dấu phẩy)" if self.add_comma_var.get() else "Tắt (không dấu phẩy)"
            
            # Tạo thông báo phù hợp với trường hợp
            if content1 and content2:
                info_msg = f"""Kết quả xử lý (2 danh sách):

📊 THỐNG KÊ CHI TIẾT:
• Danh sách 1: {original_count1} items → {len(unique_items1)} items unique
• Danh sách 2: {original_count2} items → {len(unique_items2)} items unique
• Duplicate loại bỏ trong DS1: {internal_duplicates1} items
• Duplicate loại bỏ trong DS2: {internal_duplicates2} items
• Duplicate giữa 2 danh sách: {cross_duplicates_count} items

🎯 KẾT QUẢ CUỐI CÙNG:
• Items không trùng lặp: {len(self.processed_unique_items)}
  - Chỉ có trong danh sách 1: {len(set(unique_items1) - set(unique_items2))}
  - Chỉ có trong danh sách 2: {len(set(unique_items2) - set(unique_items1))}
• Items trùng lặp giữa 2 DS: {len(self.processed_duplicate_items)}

⚙️ CÀI ĐẶT ÁP DỤNG:
• VIDs: {vids_status}
• Dấu phẩy ở kết quả: {comma_status}

✅ Xử lý hoàn tất! Sử dụng radio buttons để chuyển đổi giữa "Không trùng lặp" và "Trùng lặp"."""
            
            elif content1:
                info_msg = f"""Kết quả xử lý (chỉ danh sách 1):

📊 THỐNG KÊ CHI TIẾT:
• Danh sách 1: {original_count1} items → {len(unique_items1)} items unique
• Duplicate loại bỏ trong DS1: {internal_duplicates1} items

🎯 KẾT QUẢ CUỐI CÙNG:
• Items không trùng lặp: {len(self.processed_unique_items)} (tất cả items unique)
• Items trùng lặp nội bộ: {len(self.processed_duplicate_items)}

⚙️ CÀI ĐẶT ÁP DỤNG:
• VIDs: {vids_status}
• Dấu phẩy ở kết quả: {comma_status}

✅ Xử lý hoàn tất! Sử dụng radio buttons để chuyển đổi giữa "Không trùng lặp" và "Trùng lặp"."""
            
            elif content2:
                info_msg = f"""Kết quả xử lý (chỉ danh sách 2):

📊 THỐNG KÊ CHI TIẾT:
• Danh sách 2: {original_count2} items → {len(unique_items2)} items unique
• Duplicate loại bỏ trong DS2: {internal_duplicates2} items

🎯 KẾT QUẢ CUỐI CÙNG:
• Items không trùng lặp: {len(self.processed_unique_items)} (tất cả items unique)
• Items trùng lặp nội bộ: {len(self.processed_duplicate_items)}

⚙️ CÀI ĐẶT ÁP DỤNG:
• VIDs: {vids_status}
• Dấu phẩy ở kết quả: {comma_status}

✅ Xử lý hoàn tất! Sử dụng radio buttons để chuyển đổi giữa "Không trùng lặp" và "Trùng lặp"."""
            
            messagebox.showinfo("Thành công", info_msg)
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {str(e)}")
    
    def clear_all(self):
        """Xóa tất cả nội dung"""
        self.text1.delete("1.0", tk.END)
        self.text2.delete("1.0", tk.END)
        self.text3.config(state=tk.NORMAL)
        self.text3.delete("1.0", tk.END)
        self.text3.config(state=tk.DISABLED)
        
        # Xóa kết quả đã xử lý
        self.processed_unique_items = []
        self.processed_duplicate_items = []
        
        # Xóa highlight
        self.text1.tag_remove("duplicate", "1.0", tk.END)
        self.text2.tag_remove("duplicate", "1.0", tk.END)
        self.text1.tag_remove("internal_duplicate", "1.0", tk.END)
        self.text2.tag_remove("internal_duplicate", "1.0", tk.END)
        
        self.add_placeholder_text()
        # Cập nhật counters
        self.update_all_counters()
    
    def copy_result(self):
        """Copy kết quả vào clipboard"""
        try:
            result = self.text3.get("1.0", tk.END).strip()
            if result and not result.startswith("Chưa có dữ liệu") and not result.startswith("Không có items"):
                self.parent_frame.clipboard_clear()
                self.parent_frame.clipboard_append(result)
                
                # Đếm items theo loại hiện tại
                if self.result_type_var.get() == "unique":
                    count = len(self.processed_unique_items)
                    result_type = "items không trùng lặp"
                else:
                    count = len(self.processed_duplicate_items)
                    result_type = "items trùng lặp"
                
                messagebox.showinfo("Thành công", f"Đã copy {count} {result_type} vào clipboard!")
            else:
                messagebox.showwarning("Cảnh báo", "Không có kết quả để copy!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể copy: {str(e)}")


class UnitConverter:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        
        # Tạo main frame với grid layout
        main_frame = ttk.Frame(parent_frame, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Cấu hình grid - PHÂN BỔ ĐỀU 50-50
        main_frame.columnconfigure(0, weight=1)  # Cột trái - 50%
        main_frame.columnconfigure(1, weight=1)  # Cột phải - 50%
        main_frame.rowconfigure(1, weight=1)     # Hàng chính có thể mở rộng
        
        # Title
        title_label = tk.Label(main_frame, text="Unit Converter - μm ⇄ mils", 
                              font=("Arial", 16, "bold"), fg="#0078d4")
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 15), sticky="ew")
        
        # =========================
        # PHẦN TRÁI: Chuyển đổi đơn lẻ + Thông tin (50%)
        # =========================
        left_frame = ttk.Frame(main_frame)
        left_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        
        # Frame chuyển đổi đơn lẻ
        converter_frame = ttk.LabelFrame(left_frame, text="🔄 Chuyển đổi nhanh", padding="15")
        converter_frame.pack(fill=tk.X, pady=(0, 15))
        
        # μm to mils
        um_frame = ttk.LabelFrame(converter_frame, text="μm → mils", padding="10")
        um_frame.pack(fill=tk.X, pady=(0, 10))
        
        um_input_frame = ttk.Frame(um_frame)
        um_input_frame.pack(fill=tk.X, pady=(0, 8))
        
        ttk.Label(um_input_frame, text="Nhập giá trị (μm):", font=("Arial", 10)).pack(anchor=tk.W)
        
        um_entry_frame = ttk.Frame(um_input_frame)
        um_entry_frame.pack(fill=tk.X, pady=(3, 0))
        
        self.um_var = tk.StringVar()
        self.um_entry = ttk.Entry(um_entry_frame, textvariable=self.um_var, font=("Arial", 11))
        self.um_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
        
        ttk.Button(um_entry_frame, text="Convert", 
                  command=self.convert_um_to_mils, style="Small.TButton").pack(side=tk.RIGHT)
        
        # Result μm
        self.um_result_var = tk.StringVar(value="Nhập số và nhấn Convert")
        result_label1 = tk.Label(um_frame, textvariable=self.um_result_var, 
                                font=("Arial", 10, "bold"), fg="#008000", bg="#f0f0f0", 
                                relief=tk.SUNKEN, padx=8, pady=5, wraplength=350)
        result_label1.pack(fill=tk.X, pady=(5, 0))
        
        # mils to μm
        mils_frame = ttk.LabelFrame(converter_frame, text="mils → μm", padding="10")
        mils_frame.pack(fill=tk.X)
        
        mils_input_frame = ttk.Frame(mils_frame)
        mils_input_frame.pack(fill=tk.X, pady=(0, 8))
        
        ttk.Label(mils_input_frame, text="Nhập giá trị (mils):", font=("Arial", 10)).pack(anchor=tk.W)
        
        mils_entry_frame = ttk.Frame(mils_input_frame)
        mils_entry_frame.pack(fill=tk.X, pady=(3, 0))
        
        self.mils_var = tk.StringVar()
        self.mils_entry = ttk.Entry(mils_entry_frame, textvariable=self.mils_var, font=("Arial", 11))
        self.mils_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
        
        ttk.Button(mils_entry_frame, text="Convert", 
                  command=self.convert_mils_to_um, style="Small.TButton").pack(side=tk.RIGHT)
        
        # Result mils
        self.mils_result_var = tk.StringVar(value="Nhập số và nhấn Convert")
        result_label2 = tk.Label(mils_frame, textvariable=self.mils_result_var, 
                                font=("Arial", 10, "bold"), fg="#008000", bg="#f0f0f0", 
                                relief=tk.SUNKEN, padx=8, pady=5, wraplength=350)
        result_label2.pack(fill=tk.X, pady=(5, 0))
        
        # Information frame
        info_frame = ttk.LabelFrame(left_frame, text="ℹ️ Thông tin chuyển đổi", padding="15")
        info_frame.pack(fill=tk.BOTH, expand=True)
        
        info_text = """📐 Công thức chuyển đổi:
• 1 mil = 25.4 μm (micrometers)
• 1 μm = 0.0393701 mils

📝 Ví dụ thực tế:
• 100 μm = 3.937 mils
• 10 mils = 254 μm
• 50.8 μm = 2 mils
• 5 mils = 127 μm

💡 Mẹo sử dụng:
• Nhấn Enter để convert nhanh
• Sử dụng chuyển đổi hàng loạt bên phải 
  cho nhiều giá trị cùng lúc
• Có thể paste từ Excel/CSV

👨‍💻 Developed by: VNAT Def-Met
    nguyen, dinh phuong"""
        
        info_label = tk.Label(info_frame, text=info_text, justify=tk.LEFT, 
                             font=("Arial", 9), fg="#444444")
        info_label.pack(anchor=tk.W, fill=tk.BOTH, expand=True)
        
        # =========================
        # PHẦN PHẢI: Chuyển đổi hàng loạt (50%)
        # =========================
        right_frame = ttk.LabelFrame(main_frame, text="📊 Chuyển đổi hàng loạt", padding="15")
        right_frame.grid(row=1, column=1, sticky="nsew")
        
        # Cấu hình grid cho right_frame
        right_frame.columnconfigure(0, weight=1)
        right_frame.columnconfigure(1, weight=1)
        right_frame.rowconfigure(1, weight=1)
        
        # Control frame - TRÊN CÙNG
        control_frame = ttk.LabelFrame(right_frame, text="⚙️ Cài đặt chuyển đổi", padding="10")
        control_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        
        # Radio buttons và Convert button
        control_top_frame = ttk.Frame(control_frame)
        control_top_frame.pack(fill=tk.X)
        
        self.unit_var = tk.StringVar(value="um")
        
        # Radio buttons - TRÁI - SỬA LẠI KHÔNG DÙNG FONT
        radio_frame = ttk.Frame(control_top_frame)
        radio_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Radiobutton(radio_frame, text="μm → mils", 
                       variable=self.unit_var, value="um", 
                       style="Custom.TRadiobutton").pack(anchor=tk.W, pady=1)
        
        ttk.Radiobutton(radio_frame, text="mils → μm", 
                       variable=self.unit_var, value="mils",
                       style="Custom.TRadiobutton").pack(anchor=tk.W, pady=1)
        
        # Convert button - PHẢI
        button_frame = ttk.Frame(control_top_frame)
        button_frame.pack(side=tk.RIGHT, padx=(10, 0))
        
        self.batch_convert_btn = ttk.Button(button_frame, text="🔄 CONVERT ALL", 
                                           command=self.batch_convert, 
                                           style="Accent.TButton")
        self.batch_convert_btn.pack()
        
        # Input frame - TRÁI
        input_frame = ttk.LabelFrame(right_frame, text="📝 Input Data", padding="8")
        input_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 8))
        
        self.batch_input = scrolledtext.ScrolledText(input_frame, font=("Consolas", 10))
        self.batch_input.pack(fill=tk.BOTH, expand=True, pady=(0, 8))
        
        # Input buttons
        input_btn_frame = ttk.Frame(input_frame)
        input_btn_frame.pack(fill=tk.X)
        
        ttk.Button(input_btn_frame, text="🗑️ Clear Input", 
                  command=self.clear_batch_input).pack(side=tk.LEFT)
        
        input_info = tk.Label(input_btn_frame, text="Mỗi dòng 1 số", 
                             font=("Arial", 8), fg="#666666")
        input_info.pack(side=tk.RIGHT)
        
        # Output frame - PHẢI
        output_frame = ttk.LabelFrame(right_frame, text="📊 Results", padding="8")
        output_frame.grid(row=1, column=1, sticky="nsew", padx=(8, 0))
        
        self.batch_output = scrolledtext.ScrolledText(output_frame, font=("Consolas", 10), 
                                                     state=tk.DISABLED, bg="#f8f8f8")
        self.batch_output.pack(fill=tk.BOTH, expand=True, pady=(0, 8))
        
        # Output buttons
        output_btn_frame = ttk.Frame(output_frame)
        output_btn_frame.pack(fill=tk.X)
        
        ttk.Button(output_btn_frame, text="📋 Copy", 
                  command=self.copy_batch_results).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(output_btn_frame, text="🗑️ Clear", 
                  command=self.clear_batch_output).pack(side=tk.LEFT)
        
        # Thêm placeholder cho batch input
        self.add_batch_placeholder()
        
        # Bind Enter key
        self.um_entry.bind('<Return>', lambda e: self.convert_um_to_mils())
        self.mils_entry.bind('<Return>', lambda e: self.convert_mils_to_um())
        
        # Auto-clear results when typing
        try:
            self.um_var.trace_add('write', self.clear_um_result)
            self.mils_var.trace_add('write', self.clear_mils_result)
        except AttributeError:
            self.um_var.trace('w', self.clear_um_result)
            self.mils_var.trace('w', self.clear_mils_result)
    
    def add_batch_placeholder(self):
        """Thêm placeholder cho batch input"""
        placeholder_text = """100
254
50.8
127
25.4
76.2
203.2
381
508"""
        
        self.batch_input.insert("1.0", placeholder_text)
        self.batch_input.config(fg="gray")
        
        def on_focus_in(event):
            if self.batch_input.get("1.0", tk.END).strip() == placeholder_text:
                self.batch_input.delete("1.0", tk.END)
                self.batch_input.config(fg="black")
        
        def on_focus_out(event):
            if not self.batch_input.get("1.0", tk.END).strip():
                self.batch_input.insert("1.0", placeholder_text)
                self.batch_input.config(fg="gray")
        
        self.batch_input.bind("<FocusIn>", on_focus_in)
        self.batch_input.bind("<FocusOut>", on_focus_out)
    
    def clear_batch_input(self):
        """Xóa input batch"""
        self.batch_input.delete("1.0", tk.END)
        self.batch_input.config(fg="black")
    
    def clear_batch_output(self):
        """Xóa output batch"""
        self.batch_output.config(state=tk.NORMAL)
        self.batch_output.delete("1.0", tk.END)
        self.batch_output.config(state=tk.DISABLED)
    
    def clear_um_result(self, *args):
        """Clear μm result when typing"""
        if self.um_var.get():
            self.um_result_var.set("Nhấn Convert để xem kết quả")
    
    def clear_mils_result(self, *args):
        """Clear mils result when typing"""
        if self.mils_var.get():
            self.mils_result_var.set("Nhấn Convert để xem kết quả")
    
    def convert_um_to_mils(self):
        """Convert micrometers to mils"""
        try:
            um_value = float(self.um_var.get().replace(',', '.'))
            mils_value = um_value * 0.0393701
            
            result_text = f"✅ {um_value:,.6g} μm = {mils_value:.6g} mils"
            self.um_result_var.set(result_text)
            
        except ValueError:
            self.um_result_var.set("❌ Vui lòng nhập số hợp lệ!")
        except Exception as e:
            self.um_result_var.set(f"❌ Lỗi: {str(e)}")
    
    def convert_mils_to_um(self):
        """Convert mils to micrometers"""
        try:
            mils_value = float(self.mils_var.get().replace(',', '.'))
            um_value = mils_value * 25.4
            
            result_text = f"✅ {mils_value:,.6g} mils = {um_value:.6g} μm"
            self.mils_result_var.set(result_text)
            
        except ValueError:
            self.mils_result_var.set("❌ Vui lòng nhập số hợp lệ!")
        except Exception as e:
            self.mils_result_var.set(f"❌ Lỗi: {str(e)}")
    
    def batch_convert(self):
        """Convert multiple values"""
        try:
            input_text = self.batch_input.get("1.0", tk.END).strip()
            
            # Kiểm tra nếu là placeholder text
            placeholder_text = """100
254
50.8
127
25.4
76.2
203.2
381
508"""
            
            if not input_text or input_text == placeholder_text:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập dữ liệu để chuyển đổi!")
                return
            
            lines = input_text.split('\n')
            results = []
            conversion_type = self.unit_var.get()
            valid_count = 0
            error_count = 0
            
            # Header cho kết quả
            if conversion_type == "um":
                results.append("=== μm → mils ===")
            else:
                results.append("=== mils → μm ===")
            
            results.append("=" * 25)
            
            for i, line in enumerate(lines, 1):
                line = line.strip()
                if not line:
                    continue
                
                try:
                    value = float(line.replace(',', '.'))
                    
                    if conversion_type == "um":
                        # μm to mils
                        converted = value * 0.0393701
                        results.append(f"{value:>7.2f} μm → {converted:<7.3f} mils")
                    else:
                        # mils to μm
                        converted = value * 25.4
                        results.append(f"{value:>7.2f} mils → {converted:<7.2f} μm")
                    
                    valid_count += 1
                        
                except ValueError:
                    results.append(f"❌ Dòng {i}: '{line}' - Lỗi")
                    error_count += 1
            
            # Footer thống kê
            results.append("=" * 25)
            results.append(f"✅ Thành công: {valid_count}")
            if error_count > 0:
                results.append(f"❌ Lỗi: {error_count}")
            
            # Display results
            self.batch_output.config(state=tk.NORMAL)
            self.batch_output.delete("1.0", tk.END)
            self.batch_output.insert("1.0", '\n'.join(results))
            self.batch_output.config(state=tk.DISABLED)
            
            if valid_count > 0:
                messagebox.showinfo("Thành công! 🎉", 
                                  f"Đã chuyển đổi {valid_count} giá trị!")
            else:
                messagebox.showwarning("Cảnh báo", "Không có giá trị hợp lệ!")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi chuyển đổi: {str(e)}")
    
    def copy_batch_results(self):
        """Copy batch conversion results"""
        try:
            results = self.batch_output.get("1.0", tk.END).strip()
            if results:
                self.parent_frame.clipboard_clear()
                self.parent_frame.clipboard_append(results)
                messagebox.showinfo("Thành công! 📋", "Đã copy kết quả vào clipboard!")
            else:
                messagebox.showwarning("Cảnh báo", "Không có kết quả để copy!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể copy: {str(e)}")


class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("VNAT Def-Met Tool - V1.7                               Owner: Nguyen, Dinh Phuong")
        self.root.geometry("1000x800")
        
        # Đặt icon cho ứng dụng (nếu có file icon)
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass
        
        # Cấu hình grid weight
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Tạo notebook (tab container)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tab 1: Duplicate Remover
        self.duplicate_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.duplicate_frame, text="🔍 Duplicate Remover")
        self.duplicate_remover = DuplicateRemover(self.duplicate_frame)
        
        # Tab 2: Unit Converter
        self.converter_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.converter_frame, text="🔄 Conversion")
        self.unit_converter = UnitConverter(self.converter_frame)


def main():
    root = tk.Tk()
    
    # Cấu hình style
    style = ttk.Style()
    style.theme_use('clam')
    
    # Tạo style cho button chính
    style.configure("Accent.TButton", 
                   foreground="white", 
                   background="#0078d4",
                   focuscolor="none",
                   font=("Arial", 10, "bold"))
    
    # Style cho button nhỏ
    style.configure("Small.TButton", 
                   font=("Arial", 9))
    
    # Style cho radio button - SỬA LẠI
    style.configure("Custom.TRadiobutton", 
                   font=("Arial", 10))
    
    app = MainApplication(root)
    
    # Xử lý sự kiện đóng cửa sổ
    def on_closing():
        if messagebox.askokcancel("Thoát", "Bạn có chắc chắn muốn thoát?"):
            root.quit()
            root.destroy()
            sys.exit()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Đặt cửa sổ ở giữa màn hình
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()
