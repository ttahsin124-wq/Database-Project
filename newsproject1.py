import tkinter as tk
from tkinter import messagebox, END
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import mysql.connector

def get_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="nisa_tahsin",
            password="123456789",
            database="news_project"
        )
        return conn
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Could not connect to MySQL:\n{e}")    
        return None



class NewsBlogApp(ttk.Window):
    def __init__(self):
        super().__init__(themename="cyborg")
        self.title("News Blog Management System")
        self.geometry("1200x700")

        
        self.active_view = None

        self.create_sidebar()
        self.create_header()
        self.create_content()

        self.show_user_management()  

   
    def create_sidebar(self):
        self.sidebar = ttk.Frame(self, padding=10, bootstyle="dark")
        self.sidebar.pack(side=LEFT, fill=Y)

        ttk.Label(self.sidebar, text="MENU", font=("Arial", 14, "bold")).pack(pady=10)

        ttk.Button(self.sidebar, text="👤 Users", width=20, bootstyle="secondary",
                   command=self.show_user_management).pack(pady=5)

        ttk.Button(self.sidebar, text="📰 News", width=20, bootstyle="secondary",
                   command=self.show_news_management).pack(pady=5)

    
    def create_header(self):
        self.header = ttk.Frame(self, padding=10)
        self.header.pack(fill=tk.X)
        self.title_label = tk.Label(
        self.header,
        text="News Blog Management System",
        font=("Arial", 22, "bold"),
        fg="white",
        bg="#001330"   # navy blue
    )
        self.title_label.pack(fill=tk.X, pady=5)

   
    def create_content(self):
        self.content = ttk.Frame(self)
        self.content.pack(fill=BOTH, expand=True)

    def clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()
        for w in self.header.winfo_children():
            if w is not self.title_label:
             w.destroy()
    

    def sort_treeview(self,tree,col,reverse):
        for c in tree["columns"]:
            text=c.title()
            tree.heading(c,text=text,command=lambda _c=c:self.sort_treeview(tree,_c,False))
        arrow=" ↑" if not reverse else " ↓" 
        tree.heading(col,text=col.title()+arrow,command=lambda:self.sort_treeview(tree,col,not reverse))

        data=[(tree.set(k,col),k) for k in tree.get_children('')]
        try:
            data.sort(key=lambda t:float(t[0]),reverse=reverse)
        except:
            data.sort(key=lambda t:t[0].lower(),reverse=reverse)
        for index,(val,k) in enumerate(data):
            tree.move(k,'',index)
        
   
    def show_user_management(self):
        self.active_view = "users"
        self.clear_content()

        
        
        ttk.Button(self.header, text="➕ Add User", bootstyle="success",
                   command=self.add_user_popup).pack(side=LEFT, padx=5)

        ttk.Button(self.header, text="✏ Edit User", bootstyle="info",
                   command=self.edit_selected_user).pack(side=LEFT, padx=5)

        ttk.Button(self.header, text="🗑 Delete User", bootstyle="danger",
                   command=self.delete_selected_user).pack(side=LEFT, padx=5)

        ttk.Button(self.header, text="🔄 Refresh", bootstyle="secondary",
                   command=self.show_user_management).pack(side=LEFT, padx=5)

        
        search_frame = ttk.Frame(self.header)
        search_frame.pack(side=RIGHT, padx=20)

        search_fields = ["name", "user_id", "age"]
        self.user_search_field = ttk.Combobox(search_frame, values=search_fields, width=10, state="readonly")
        self.user_search_field.set("name")
        self.user_search_field.pack(side=LEFT, padx=2)

        self.user_search_entry = ttk.Entry(search_frame, width=25)
        self.user_search_entry.pack(side=LEFT, padx=2)

        ttk.Button(search_frame, text="🔍 Search", bootstyle="info",
                   command=self.search_users).pack(side=LEFT, padx=2)

        
        self.tree = ttk.Treeview(self.content,
                                 columns=("user_id", "name", "email", "age", "contact"),
                                 show="headings")
        self.tree.pack(fill=BOTH, expand=True, padx=10, pady=10)

        for col in ("user_id", "name", "email", "age", "contact"):
            self.tree.heading(col, text=col.title(),command=lambda c=col:self.sort_treeview(self.tree,c,False))
            if col=="age":
                self.tree.column(col,width=150,anchor='center')
            else:
                self.tree.column(col, width=150)

        self.load_users()

        self.tree.bind("<Double-1>", lambda e: self.show_user_news())
    def show_user_news(self):
      user_id = self.get_selected_user()
      if not user_id:
        return

      conn = get_db()
      cur = conn.cursor()
    
      cur.execute("SELECT name FROM users WHERE user_id=%s", (user_id,))
      user_name = cur.fetchone()[0]

    
      cur.execute("SELECT news_id, title, created_at FROM news WHERE user_id=%s ORDER BY news_id DESC", (user_id,))
      news_list = cur.fetchall()
      conn.close()

    
      modal = tk.Toplevel(self)
      modal.title(f"News by {user_name}")
      modal.geometry("600x400")
      modal.grab_set()

      tree = ttk.Treeview(modal, columns=("news_id", "title", "created_at"), show="headings")
      tree.pack(fill=BOTH, expand=True, padx=10, pady=10)

      for col in ("news_id", "title", "created_at"):
          tree.heading(col, text=col.title())
          tree.column(col, width=180)

      for row in news_list:
          tree.insert("", END, values=row)
      def show_full_news(event):
           selected_item=tree.focus()
           if not selected_item:
                return
           news_id=tree.item(selected_item,"values")[0]
           conn2=get_db()
           cur2=conn2.cursor()
           cur2.execute("SELECT title, body FROM news WHERE news_id=%s", (news_id,))
           news=cur2.fetchone()
           conn2.close()
           if news:
               full_modal=tk.Toplevel(modal)
               full_modal.title(news[0])
               full_modal.geometry("500x400")
               full_modal.grab_set()
               ttk.Label(full_modal, text=news[0], font=("Arial", 14, "bold")).pack(pady=5)
               body_text = tk.Text(full_modal, wrap="word")
               body_text.pack(fill=BOTH, expand=True, padx=10, pady=10)
               body_text.insert("1.0", news[1])
               body_text.config(state="disabled")
      tree.bind("<Double-1>",show_full_news)


    def load_users(self):
        self.tree.delete(*self.tree.get_children())
        conn = get_db()
        if conn:
            cur = conn.cursor()
            cur.execute("SELECT user_id, name, email, age, contact_number FROM users ORDER BY user_id DESC")
            for row in cur.fetchall():
                self.tree.insert("", END, iid=row[0], values=row)
            conn.close()

    def search_users(self):
        field = self.user_search_field.get()
        keyword = self.user_search_entry.get().strip()

        if keyword == "":
            self.load_users()
            return

        query = f"SELECT user_id, name, email, age, contact_number FROM users WHERE {field} LIKE %s"

        conn = get_db()
        if conn:
            cur = conn.cursor()
            cur.execute(query, (f"%{keyword}%",))
            data = cur.fetchall()
            conn.close()

            self.tree.delete(*self.tree.get_children())
            for row in data:
                self.tree.insert("", END, iid=row[0], values=row)

    def add_user_popup(self):
        modal = tk.Toplevel(self)
        modal.title("Add User")
        modal.geometry("350x300")
        modal.grab_set()

        name = tk.StringVar()
        email = tk.StringVar()
        age = tk.StringVar()
        contact = tk.StringVar()

        ttk.Label(modal, text="Name:").pack()
        ttk.Entry(modal, textvariable=name).pack()

        ttk.Label(modal, text="Email:").pack()
        ttk.Entry(modal, textvariable=email).pack()

        ttk.Label(modal, text="Age:").pack()
        ttk.Entry(modal, textvariable=age).pack()

        ttk.Label(modal, text="Contact:").pack()
        ttk.Entry(modal, textvariable=contact).pack()

        def save():
            if age.get() != "" and not age.get().isdigit():
                messagebox.showwarning("Invalid Age", "Age must be numeric.")
                return

            conn = get_db()
            if conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO users (name,email,age,contact_number) VALUES (%s,%s,%s,%s)",
                            (name.get(), email.get(), age.get(), contact.get()))
                conn.commit()
                conn.close()

                modal.destroy()
                self.show_user_management()

        ttk.Button(modal, text="Save", bootstyle="success", command=save).pack(pady=10)

    def get_selected_user(self):
        item = self.tree.focus()
        if not item:
            messagebox.showwarning("Select User", "Please select a user.")
            return None
        return int(item)

    def edit_selected_user(self):
        user_id = self.get_selected_user()
        if not user_id:
            return

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT name,email,age,contact_number FROM users WHERE user_id=%s", (user_id,))
        user = cur.fetchone()
        conn.close()

        modal = tk.Toplevel(self)
        modal.title("Edit User")
        modal.geometry("350x300")
        modal.grab_set()

        name = tk.StringVar(value=user[0])
        email = tk.StringVar(value=user[1])
        age = tk.StringVar(value=user[2])
        contact = tk.StringVar(value=user[3])

        ttk.Label(modal, text="Name:").pack()
        ttk.Entry(modal, textvariable=name).pack()

        ttk.Label(modal, text="Email:").pack()
        ttk.Entry(modal, textvariable=email).pack()

        ttk.Label(modal, text="Age:").pack()
        ttk.Entry(modal, textvariable=age).pack()

        ttk.Label(modal, text="Contact:").pack()
        ttk.Entry(modal, textvariable=contact).pack()

        def update_user():
            conn2 = get_db()
            cur2 = conn2.cursor()
            cur2.execute("""UPDATE users 
                            SET name=%s, email=%s, age=%s, contact_number=%s 
                            WHERE user_id=%s""",
                         (name.get(), email.get(), age.get(), contact.get(), user_id))
            conn2.commit()
            conn2.close()

            modal.destroy()
            self.show_user_management()

        ttk.Button(modal, text="Update", bootstyle="info", command=update_user).pack(pady=10)

    def delete_selected_user(self):
        user_id = self.get_selected_user()
        if not user_id:
            return

        if not messagebox.askyesno("Confirm Delete",
                                   "This user and their news will be permanently deleted.\nProceed?"):
            return

        conn = get_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE user_id=%s", (user_id,))
        conn.commit()
        conn.close()

        self.show_user_management()

   
    def show_news_management(self):
        self.active_view = "news"
        self.clear_content()

        
        ttk.Button(self.header, text="➕ Add News", bootstyle="success",
                   command=self.add_news_popup).pack(side=LEFT, padx=5)

        ttk.Button(self.header, text="✏ Edit News", bootstyle="info",
                   command=self.edit_selected_news).pack(side=LEFT, padx=5)

        ttk.Button(self.header, text="🗑 Delete News", bootstyle="danger",
                   command=self.delete_selected_news).pack(side=LEFT, padx=5)

        ttk.Button(self.header, text="🔄 Refresh", bootstyle="secondary",
                   command=self.show_news_management).pack(side=LEFT, padx=5)

        
        search_frame = ttk.Frame(self.header)
        search_frame.pack(side=RIGHT, padx=20)

        search_fields = ["title", "news_id", "name"]
        self.news_search_field = ttk.Combobox(search_frame, values=search_fields, width=10, state="readonly")
        self.news_search_field.set("title")
        self.news_search_field.pack(side=LEFT, padx=2)

        self.news_search_entry = ttk.Entry(search_frame, width=25)
        self.news_search_entry.pack(side=LEFT, padx=2)

        ttk.Button(search_frame, text="🔍 Search", bootstyle="info",
                   command=self.search_news).pack(side=LEFT, padx=2)

        self.tree = ttk.Treeview(self.content,
                                 columns=("news_id", "name", "title", "created_at"),
                                 show="headings")
        self.tree.pack(fill=BOTH, expand=True, padx=10, pady=10)

        for col in ("news_id", "name", "title", "created_at"):
            self.tree.heading(col, text=col.title(),command=lambda c=col:self.sort_treeview(self.tree,c,False))
            if col=="created_at":
                self.tree.column(col,width=200,anchor="center")
            else:
                self.tree.column(col, width=200)

        self.load_news()

        self.tree.bind("<Double-1>", lambda e: self.edit_selected_news())

    def load_news(self):
        self.tree.delete(*self.tree.get_children())
        conn = get_db()
        if conn:
            cur = conn.cursor()
            cur.execute("SELECT news_id,name,title,created_at FROM news ORDER BY news_id DESC")
            for row in cur.fetchall():
                news_id, name, title, created_at = row
                words = title.split()
                short_title = " ".join(words[:4]) + ("..." if len(words) > 4 else "")
                self.tree.insert("", END, iid=news_id, values=(news_id, name, short_title, created_at))
            conn.close()

    
    def search_news(self):
        field = self.news_search_field.get()
        keyword = self.news_search_entry.get().strip()

        if keyword == "":
            self.load_news()
            return

        query = f"SELECT news_id,name,title,created_at FROM news WHERE {field} LIKE %s"

        conn = get_db()
        if conn:
            cur = conn.cursor()
            cur.execute(query, (f"%{keyword}%",))
            data = cur.fetchall()
            conn.close()

            self.tree.delete(*self.tree.get_children())
            for row in data:
                self.tree.insert("", END, iid=row[0], values=row)

   
    def add_news_popup(self):
        modal = tk.Toplevel(self)
        modal.title("Add News")
        modal.geometry("500x450")
        modal.grab_set()

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT user_id, name FROM users ORDER BY name")
        users = cur.fetchall()
        conn.close()

        user_var = tk.StringVar()
        title_var = tk.StringVar()

        ttk.Label(modal, text="Select User:").pack()
        user_combo = ttk.Combobox(modal, textvariable=user_var,
                                  values=[f"{u[0]} - {u[1]}" for u in users], state="readonly")
        user_combo.pack()

        ttk.Label(modal, text="Title:").pack()
        ttk.Entry(modal, textvariable=title_var, width=40).pack()

        ttk.Label(modal, text="Body:").pack()
        body_text = tk.Text(modal, height=12)
        body_text.pack()

        def save_news():
            if not user_var.get():
                messagebox.showwarning("Select User", "Select a user.")
                return

            user_id = int(user_var.get().split(" - ")[0])
            username = user_var.get().split(" - ")[1]

            conn2 = get_db()
            cur2 = conn2.cursor()
            cur2.execute(
                "INSERT INTO news (user_id,name,title,body) VALUES (%s,%s,%s,%s)",
                (user_id, username, title_var.get(), body_text.get("1.0", END)))
            conn2.commit()
            conn2.close()

            modal.destroy()
            self.show_news_management()

        ttk.Button(modal, text="Save", bootstyle="success", command=save_news).pack(pady=10)

    def get_selected_news(self):
        item = self.tree.focus()
        if not item:
            messagebox.showwarning("Select News", "Please select a news item.")
            return None
        return int(item)

    def edit_selected_news(self):
        news_id = self.get_selected_news()
        if not news_id:
            return

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT title,body FROM news WHERE news_id=%s", (news_id,))
        news = cur.fetchone()
        conn.close()

        modal = tk.Toplevel(self)
        modal.title("Edit News")
        modal.geometry("500x450")
        modal.grab_set()

        title_var = tk.StringVar(value=news[0])

        ttk.Label(modal, text="Title:").pack()
        ttk.Entry(modal, textvariable=title_var, width=40).pack()

        ttk.Label(modal, text="Body:").pack()
        body_text = tk.Text(modal, height=12)
        body_text.pack()
        body_text.insert("1.0", news[1])

        def update_news():
            conn2 = get_db()
            cur2 = conn2.cursor()
            cur2.execute(
                "UPDATE news SET title=%s, body=%s WHERE news_id=%s",
                (title_var.get(), body_text.get("1.0", END), news_id))
            conn2.commit()
            conn2.close()

            modal.destroy()
            self.show_news_management()

        ttk.Button(modal, text="Update", bootstyle="info", command=update_news).pack(pady=10)

    def delete_selected_news(self):
        news_id = self.get_selected_news()
        if not news_id:
            return

        if not messagebox.askyesno("Confirm Delete", "Delete selected news?"):
            return

        conn = get_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM news WHERE news_id=%s", (news_id,))
        conn.commit()
        conn.close()

        self.show_news_management()



if __name__ == "__main__":
    app = NewsBlogApp()
    app.mainloop()
