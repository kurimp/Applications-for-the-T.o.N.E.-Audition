import tkinter as tk

class label_wraplength:
  def __init__(self, root):
    self.root = root
    self.label_list = []
    self.after_id = None
  
  def label_maker(self, parent, text=None):
    label = tk.Label(parent, text=text)
    self.label_list.append(label)
    return label
  
  def debounce_update_all_label_wraplength(self, event=None):
    if self.after_id:
      self.root.after_cancel(self.after_id)
    self.after_id = self.root.after(100, self.update_all_label_wraplength)
  
  def update_all_label_wraplength(self, event=None):
    self.root.update_idletasks()
    padding = 20
    
    for label in self.label_list:
      if label.winfo_exists():
        parent_widget = self.root.nametowidget(label.winfo_parent())
        parent_width = parent_widget.winfo_width()
        label.config(wraplength=parent_width - padding)
    
  def treatment(self):
    self.root.bind("<Configure>", self.debounce_update_all_label_wraplength)
    self.root.after(100, self.update_all_label_wraplength)