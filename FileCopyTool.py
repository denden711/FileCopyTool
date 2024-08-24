import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

def validate_name(name):
    """ファイル名が無効かどうかをチェックする"""
    if not name or name.isspace():
        return False
    if any(char in name for char in r'\/:*?"<>|'):
        return False
    return True

def handle_existing_file(name, dest_file):
    """同じ名前のファイルが存在する場合の処理"""
    if os.path.exists(dest_file):
        messagebox.showwarning("警告", f"ファイル '{name}' は既に存在します。コピーをスキップします。")
        return False
    return True

def copy_file(src_file, dest_file):
    """ファイルのコピー処理"""
    try:
        shutil.copy(src_file, dest_file)
        messagebox.showinfo("成功", f"'{os.path.basename(dest_file)}' にファイルをコピーしました")
    except Exception as e:
        messagebox.showerror("エラー", f"'{os.path.basename(dest_file)}' へのファイルコピーに失敗しました: {str(e)}")

def copy_files():
    """メインのファイルコピー処理"""
    src_file = select_file()
    if not src_file:
        return

    dest_dir = select_directory()
    if not dest_dir:
        return

    names = get_names()
    if not names:
        return

    _, file_extension = os.path.splitext(src_file)

    for name in names:
        name = name.strip()
        if not validate_name(name):
            messagebox.showwarning("警告", f"無効なファイル名: '{name}'")
            continue

        if not name.endswith(file_extension):
            name += file_extension

        dest_file = os.path.join(dest_dir, name)
        
        if handle_existing_file(name, dest_file):
            copy_file(src_file, dest_file)

    messagebox.showinfo("完了", "すべてのファイルのコピーが完了しました")

def select_file():
    """コピー元のファイルを選択"""
    src_file = filedialog.askopenfilename(title="コピーしたいファイルを選択してください")
    if not src_file:
        messagebox.showwarning("警告", "ファイルが選択されていません")
    return src_file

def select_directory():
    """コピー先のディレクトリを選択"""
    dest_dir = filedialog.askdirectory(title="ファイルをコピーする先のディレクトリを選択してください")
    if not dest_dir:
        messagebox.showwarning("警告", "コピー先のディレクトリが選択されていません")
    return dest_dir

def get_names():
    """コピーするファイルの名前を取得"""
    names = name_entry.get("1.0", tk.END).strip().split("\n")
    if not names:
        messagebox.showwarning("警告", "ファイル名が指定されていません")
    return names

# GUIの設定
root = tk.Tk()
root.title("FileCopyTool")

frame = tk.Frame(root)
frame.pack(pady=20, padx=20)

tk.Label(frame, text="コピーするファイルの名前を入力してください（改行で複数入力可）:").pack(anchor=tk.W)

name_entry = tk.Text(frame, height=10, width=50)
name_entry.pack(pady=10)

copy_button = tk.Button(frame, text="コピーを開始", command=copy_files)
copy_button.pack(pady=10)

root.mainloop()
