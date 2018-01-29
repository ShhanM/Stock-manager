from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
from tkinter import ttk
import tkinter
import random
import time
import json
import os
import re

class Formatchecker():
    def __init__(self):
        pass
        
    def not_null(self, input_string):
        if not input_string:
            return False
        else:
            return True
    
    def is_pos_num(self, input_string):
        try:
            num = int(input_string)
            if num >=0:
                return True
            else:
                return False
        except:
            return False
            
class Data():
    def __init__(self):
        self.data = self.read_data() #dict
        self.record = self.read_record() #list
        self.config = self.read_ini()
        
        if not os.path.exists('data'):
            os.mkdir('data')
            
    def refresh_data(self):
        with open('data/data.json', 'w') as f:
            json.dump(self.data, f)

    def read_data(self):
        with open('data/data.json', 'r') as f:
            data = json.load(f)
        return data
    
    def refresh_record(self):
        with open('data/record.json', 'w') as f:
            json.dump(self.record, f)
        
    def read_record(self):
        with open('data/record.json', 'r') as f:
            record = json.load(f)
        return record
    
    def read_ini(self):
        with open('data/config.ini', 'r') as f:
            config = [line.strip().split(' ') for line in f.readlines() if not line.startswith('#') and not line.startswith('\n')]
        return dict(config)
            
    def get_item_list(self):
        return list(self.read_data().keys())

class Gui():
    def __init__(self):
        self.data = Data()
        self.format_checker = Formatchecker()
        self.colorbox = ['DodgerBlue', 'Plum', 'BlueViolet', 'LightSalmon', 'FireBrick', \
        'Tomato', 'MediumSeaGreen', 'PaleVioletRed', 'LightGreen', 'MediumOrchid', 'Aqua']
        try:
            self.color = self.data.config['color']
        except:
            self.color = random.choice(self.colorbox)
                
    def gen_root_window(self):
        def get_today():
            total = len(self.data.data)
            date = time.strftime('%y-%m-%d')
            today_in = 0
            today_out = 0
            for rec in self.data.record:
                if date in rec[0]:
                    if rec[2] == '入库':
                        today_in += 1
                    else:
                        today_out += 1
            return '今日：入库 [{}] 次  出库 [{}] 次\n库存 [{}] 种物品'.format(today_in, today_out, total)
            
        def tick():
            today_state.set(get_today())
            now = time.strftime('%Y-%m-%d %H:%M:%S\n%a')
            xingqi = {'Mon':'星期一', 'Tue':'星期二', 'Wed':'星期三', 'Thu':'星期四', 'Fri':'星期五', 'Sat':'星期六', 'Sun':'星期日'}
            for k,v in xingqi.items():
                now = re.sub(k, v, now)
            clock.config(text=now)
            clock.after(50, tick)
            
        print('root_window')
        global root_window
        root_window = tkinter.Tk()
        root_window.title('出入库管理系统')
        root_window.geometry('500x272+550+300')
        root_window.resizable(width=False, height=False)
        
        btn_items = ['入库', '出库', '库存查看', '出入记录']
        #color = ['grey', 'grey', 'grey', 'grey']
        btn_cmd = [self.gen_in_window, self.gen_out_window, self.gen_stk_window, self.gen_rec_window]
        for i in range(2):
            btn_name = 'button' + str(i)
            btn_name = tkinter.Button(root_window, text=btn_items[i], width=20, height=4, font=('MS Serif', '14'), bg=self.color, bd=2, command=btn_cmd[i])
            btn_name.grid(row=0, column=i, padx=10, pady=10)

        for i in range(2):
            btn_name = 'button' + str(i+2)
            btn_name = tkinter.Button(root_window, text=btn_items[i+2], width=20, height=4, font=('MS Serif', '14'), bd=2, bg=self.color, command=btn_cmd[i+2])
            btn_name.grid(row=1, column=i)
        
        today_state = tkinter.StringVar()
        state = tkinter.Label(root_window, font=('Arial', 10), textvariable=today_state)
        state.grid(row=2, column=0, pady=10, padx=10)
        today_state.set(get_today())
        clock = tkinter.Label(root_window, font=('Arial', 10))
        clock.grid(row=2, column=1, pady=10, padx=10)

        tick()
        root_window.mainloop()
        
    def gen_in_window(self):
        def flow_to_Data(new_data):
            item = new_data[0]
            unit = new_data[1]
            number = new_data[2]
            who = new_data[3]
            t = new_data[4]
            
            if item in self.data.data.keys():
                self.data.data[item][1] += int(number)
                self.data.refresh_data()
                print('已有此物品 data数据已更新 ')
            else:
                self.data.data[item] = [unit, int(number)]
                self.data.refresh_data()
                print('没有此物品，data已新增条目')
            
            self.data.record.append([t, who, '入库', number, unit, item, self.data.data[item][1]])
            self.data.refresh_record()
            print('记录已保存')
            
        def confirm_in():
            item = item_name.get()
            unit = etys[0].get()
            number = etys[1].get()
            who = etys[2].get()
            t = time.strftime('%y-%m-%d %H:%M')
            
            if '' in (item, unit, who):
                messagebox.showinfo('栏目不全', '各栏目都要填写哦', parent=in_window)
                return
                
            if not self.format_checker.is_pos_num(number):
                messagebox.showinfo('数量有误', '"数量"栏只能输入一个正整数', parent=in_window)
                return

            flow_to_Data((item, unit, number, who, t))
            in_window.withdraw()
            messagebox.showinfo('入库成功', '已将 {}{}{} 存入仓库，经手人：{}'.format(number, unit, item, who))
            
        def refresh_ety(event):
            item = item_name.get()
            unit_var.set(self.data.data[item][0])
            stock_var.set(self.data.data[item][1])

        print('in_window')
        in_window = tkinter.Toplevel(root_window)
        in_window.title('入库管理')
        in_window.geometry('576x140+510+360')
        in_window.resizable(width = False, height = False)
        
        lab_items = ['单位', '数量', '经手', '现有']
        label_head = tkinter.Label(in_window, text='')
        label_head.grid(row=0, column=0, padx=10)
        
        lab_name = tkinter.Label(in_window, text='物品', width=14)
        lab_name.grid(row=1, column=0, padx=10)
        
        item_name = ttk.Combobox(in_window, width=14)
        item_name['values'] = self.data.get_item_list()
        item_name.grid(row=2, column=0, padx=10)
        item_name.bind("<<ComboboxSelected>>", refresh_ety)
        
        etys = ['entry_in0', 'entry_in1', 'entry_in2', 'entry_in3']
        for i in range(len(lab_items)):

            lab_name = 'label_in' + str(i)
            lab_item = lab_items[i]

            lab_name = tkinter.Label(in_window, text=lab_item)
            lab_name.grid(row=1, column=i+1, padx=10)
    
            etys[i] = tkinter.Entry(in_window, width=12)
            etys[i].grid(row=2, column=i+1, padx=10)

        btn_in = tkinter.Button(in_window, text='确定入库', width=10, font=('MS Serif', '13'), bd=2, bg=self.color, command=confirm_in)
        btn_in.grid(row=3, columnspan=5, pady=20)

        unit_var = tkinter.StringVar()
        etys[0]['textvariable'] = unit_var
        stock_var = tkinter.StringVar()
        etys[3]['textvariable'] = stock_var
        etys[3]['state'] = 'disabled'
        in_window.mainloop()
        
    def gen_out_window(self):
        if len(self.data.data) == 0:
            tkinter.messagebox.showinfo('库存为空', '当前库存中没有物品，不能执行领取操作')
            return
            
        def flow_to_Data(new_data):
            item = new_data[0]
            unit = new_data[1]
            number = new_data[2]
            who = new_data[3]
            t = new_data[4]
            
            self.data.data[item][1] -= int(number)
            if self.data.data[item][1] == 0:
                del self.data.data[item]
            self.data.refresh_data()
            print('已有此物品 data数据已更新 ')

            self.data.record.append([t, who, '出库', number, unit, item, self.data.data[item][1]])
            self.data.refresh_record()
            print('记录已保存')
            
        def confirm_in():
            item = item_name.get()
            unit = etys[0].get()
            number = etys[1].get()
            who = etys[2].get()
            stock = etys[3].get()
            t = time.strftime('%y-%m-%d %H:%M')
            
            if '' in (item, unit, who):
                tkinter.messagebox.showinfo('栏目不全', '各栏目都要填写哦', parent=out_window)
                return
                
            if not self.format_checker.is_pos_num(number):
                tkinter.messagebox.showinfo('数量有误', '"领取"栏只能输入一个正整数', parent=out_window)
                return
                
            if int(number) > int(stock):
                tkinter.messagebox.showinfo('库存不够', '目前库中只有{}{}{}，不能领取{}{}'.format(stock, unit, item, number, unit), parent=out_window)
                return
            
            try:
                flow_to_Data((item, unit, number, who, t))
            except:
                pass
            out_window.withdraw()
            messagebox.showinfo('出库成功', '{}{}{} 出库成功，剩余{}{}\n经手人：{}'.format(number, unit, item, int(stock)-int(number), unit, who))
            
        def refresh_ety(event):
            item = item_name.get()
            unit_var.set(self.data.data[item][0])
            stock_var.set(self.data.data[item][1])

        print('out_window')
        out_window = tkinter.Toplevel(root_window)
        out_window.title('出库管理')
        out_window.geometry('576x140+510+360')
        out_window.resizable(width = False, height = False)
        
        lab_items = ['单位', '领取', '经手', '现有']
        label_head = tkinter.Label(out_window, text='')
        label_head.grid(row=0, column=0, padx=10)
        
        lab_name = tkinter.Label(out_window, text='物品', width=14)
        lab_name.grid(row=1, column=0, padx=10)
        
        item_name = ttk.Combobox(out_window, width=14, state='readonly')
        item_name['values'] = self.data.get_item_list()
        item_name.grid(row=2, column=0, padx=10)
        item_name.current(0)
        item_name.bind("<<ComboboxSelected>>", refresh_ety)
        
        etys = ['entry_in0', 'entry_in1', 'entry_in2', 'entry_in3']
        for i in range(len(lab_items)):
            lab_name = 'label_in' + str(i)
            lab_item = lab_items[i]

            lab_name = tkinter.Label(out_window, text=lab_item)
            lab_name.grid(row=1, column=i+1, padx=10)
    
            etys[i] = tkinter.Entry(out_window, width=12)
            etys[i].grid(row=2, column=i+1, padx=10)
        
        btn_out = tkinter.Button(out_window, text='确定出库', width=10, font=('MS Serif', '13'), bd=2, bg=self.color, command=confirm_in)
        btn_out.grid(row=3, column=0, pady=20, columnspan=5)

        unit_var = tkinter.StringVar()
        stock_var = tkinter.StringVar()
        etys[0]['textvariable'] = unit_var
        etys[3]['textvariable'] = stock_var
        etys[3]['state'] = 'disabled'
        etys[0]['state'] = 'disabled'
        out_window.mainloop()
             
    def gen_stk_window(self):
        def click_select_btn():
            choice = combobox.get()
            item = entry.get()
            if choice == '物品名称':
                lines = []
                for k,v in self.data.data.items():
                    if item in k:
                        lines.append([k, v[1], v[0]])
                if not lines:
                    frame['text'] = '没有找到'
                else:
                    frame['text'] = '{} 条记录'.format(len(lines))
                insert_lines_to_tree(lines)
                
            else:
                if not self.format_checker.is_pos_num(item):
                    tkinter.messagebox.showinfo('数量有误', '库存数只能是一个正整数', parent=stk_window)
                    return
                    
                if choice == '库存大于':
                    lines = []
                    for k,v in self.data.data.items():
                        if v[1] >= int(item):
                            lines.append([k, v[1], v[0]])
                    if not lines:
                        frame['text'] = '没有找到'
                    else:
                        frame['text'] = '{} 条记录'.format(len(lines))
                    insert_lines_to_tree(lines)
                else:
                    lines = []
                    for k,v in self.data.data.items():
                        if v[1] <= int(item):
                            lines.append([k, v[1], v[0]])
                    if not lines:
                        frame['text'] = '没有找到'
                    else:
                        frame['text'] = '{} 条记录'.format(len(lines))
                    insert_lines_to_tree(lines)
                    pass
        ids = []        
        def insert_lines_to_tree(lines):
            print('lines\n', lines)
            while ids:
                for i in ids:
                    tree.delete(i)
                    ids.remove(i)
                    print('清除了', i)
            for i in range(len(lines)):
                ids.append(tree.insert('', i, values=lines[i]))
            print('ids', ids)
            
        print('stk_window')
        stk_window = tkinter.Toplevel(root_window)
        stk_window.title('库存')
        stk_window.geometry('362x340+620+270')
        stk_window.resizable(width=False, height=False)
        
        label_head = tkinter.Label(stk_window, text='')
        label_head.grid(row=0, column=0, padx=10)
        
        combobox = ttk.Combobox(stk_window, width=10, state='readonly')
        combobox['values'] = ['物品名称', '库存大于', '库存小于']
        combobox.grid(row=1, column=0, padx=10)
        combobox.current(0)
        
        entry = tkinter.Entry(stk_window, width=12)
        entry.grid(row=1, column=1, padx=10)

        button = tkinter.Button(stk_window, width=12, text='筛选', command=click_select_btn, bg=self.color)
        button.grid(row=1, column=2, padx=10)
        
        frame = tkinter.LabelFrame(stk_window, text='筛选结果')
        frame.grid(row=2, column=0, columnspan=3, padx=10, pady=20)
        scrollbar = tkinter.Scrollbar(frame)
        scrollbar.grid(row=3, column=1, sticky=tkinter.W)
        tree = tkinter.ttk.Treeview(frame, columns=('c1', 'c2', 'c3'), show='headings', yscrollcommand=scrollbar.set)
        tree.column('c1', width=106, anchor='center')
        tree.column('c2', width=106, anchor='center')
        tree.column('c3', width=106, anchor='center')
        tree.heading('c1', text='物品')
        tree.heading('c2', text='数量')
        tree.heading('c3', text='单位')
        tree.grid(row=3, column=0, sticky=tkinter.W)
        scrollbar.config(command=tree.yview)
        
    def gen_rec_window(self):
        def click_select_btn():
            choice = combobox.get()
            item = entry.get()
            if choice == '时间':
                lines = []
                for rec in self.data.record:
                    lines.append(rec)
                if not lines:
                    frame['text'] = '没有找到'
                else:
                    frame['text'] = '{} 条记录'.format(len(lines))
                insert_lines_to_tree(lines)
            elif choice == '物品':
                lines = []
                for rec in self.data.record:
                    if item in rec[5]:
                        lines.append(rec)
                if not lines:
                    frame['text'] = '没有找到'
                else:
                    frame['text'] = '{} 条记录'.format(len(lines))
                insert_lines_to_tree(lines)

            elif choice == '数量':
                lines = []
                for rec in self.data.record:
                    if item == rec[3]:
                        lines.append(rec)
                if not lines:
                    frame['text'] = '没有找到'
                else:
                    frame['text'] = '{} 条记录'.format(len(lines))
                insert_lines_to_tree(lines)
            elif choice == '入/出':
                lines = []
                for rec in self.data.record:
                    if item in rec[2]:
                        lines.append(rec)
                if not lines:
                    frame['text'] = '没有找到'
                else:
                    frame['text'] = '{} 条记录'.format(len(lines))
                insert_lines_to_tree(lines)
            else:
                lines = []
                for rec in self.data.record:
                    if item == rec[1]:
                        lines.append(rec)
                if not lines:
                    frame['text'] = '没有找到'
                else:
                    frame['text'] = '{} 条记录'.format(len(lines))
                insert_lines_to_tree(lines)
            
        ids = []
        #tree.insert('', 0, values=['17-10-15 14:58', '马诗涵', '入库', 57, '台', '电脑', '57000'])
        def insert_lines_to_tree(lines):
            while ids:
                for i in ids:
                    tree.delete(i)
                    ids.remove(i)
                    print('清除了', i)
            for i in range(len(lines)):
                ids.append(tree.insert('', i, values=lines[i]))
            print('ids', ids)
            
        print('rec_window')
        rec_window = tkinter.Toplevel(root_window)
        rec_window.title('出入记录')
        rec_window.geometry('504x330+546+270')
        rec_window.resizable(width=False, height=False)
        
        label_head = tkinter.Label(rec_window, text='')
        label_head.grid(row=0, column=0, padx=10)
        
        label = tkinter.Label(rec_window, text='按照', width=8)
        label.grid(row=1, column=0, padx=10)
        
        combobox = ttk.Combobox(rec_window, width=10, state='readonly')
        combobox['values'] = ['时间', '物品', '数量', '入/出', '经办人']
        combobox.grid(row=1, column=1, padx=10)
        combobox.current(0)
        
        label2 = tkinter.Label(rec_window, text='==', width=8)
        label2.grid(row=1, column=2, padx=10)
        
        entry = tkinter.Entry(rec_window, width=12)
        entry.grid(row=1, column=3, padx=10)

        button = tkinter.Button(rec_window, width=12, text='筛选', command=click_select_btn, bg=self.color)
        button.grid(row=1, column=4, padx=10)
        
        frame = tkinter.LabelFrame(rec_window, text='筛选结果')
        frame.grid(row=2, column=0, columnspan=5, padx=10, pady=20)
        scrollbar = tkinter.Scrollbar(frame)
        scrollbar.grid(row=3, column=1, sticky=tkinter.W)
        tree = tkinter.ttk.Treeview(frame, columns=('c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7'), show='headings', yscrollcommand=scrollbar.set)
        tree.column('c1', width=100, anchor='center')
        tree.column('c2', width=60, anchor='center')
        tree.column('c3', width=40, anchor='center')
        tree.column('c4', width=60, anchor='center')
        tree.column('c5', width=40, anchor='center')
        tree.column('c6', width=100, anchor='center')
        tree.column('c7', width=60, anchor='center')
        tree.heading('c1', text='时间')
        tree.heading('c2', text='经手')
        tree.heading('c3', text='入/出')
        tree.heading('c4', text='数量')
        tree.heading('c5', text='单位')
        tree.heading('c6', text='物品')
        tree.heading('c7', text='库存')
        
        tree.grid(row=3, column=0, sticky=tkinter.W)
        scrollbar.config(command=tree.yview)


main = Gui()
main.gen_root_window()
