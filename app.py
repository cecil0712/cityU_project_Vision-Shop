import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from route_planning import get_route
from database_connect import *
from text_detection import OCR
from speech import speak_item, SpeakText, play_audio
import threading

class NavigationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Navigation App")
        
        self.upload_button = tk.Button(root, text="Upload/Update Image", command=self.load_image)
        self.upload_button.pack()
        
        self.start_button = tk.Button(root, text="Start Navigation", command=self.start_navigation_thread)
        self.start_button.pack()
        
        self.image_label = tk.Label(root)
        self.image_label.pack()
        
        self.used_images_frame = tk.Frame(root)
        self.used_images_frame.pack()
        
        self.text_output = tk.Text(root, height=4)
        self.text_output.pack()
        
        self.img = None
        self.img_path = None
        self.used_images = []
        
    def start_navigation_thread(self):
        navigation_thread = threading.Thread(target=self.start_navigation)
        navigation_thread.start()

    def clear_displayed_image(self):
        self.image_label.config(image='')
        self.image_label.image = None


    def start_navigation(self):
            if self.img is None:
                raise ValueError("Please upload an image first.")
                
            self.text_output.insert(tk.END, "Starting navigation...\n")
            print("Starting navigation...")
            map = get_map()
            print("Map obtained")
            
            text = speak_item(get_item_list())
            print(f"Text obtained: {text}")
            if check_discount(text):
                play_audio('audio/discount.wav')
            destination = get_item_coor(text)
            print(f"Destination coordinates: {destination}")
            play_audio('audio/directing.wav')
            
            # print(f"Using image path: {self.img_path}")
            current_brand = check_exist(OCR(self.img_path))
            if current_brand is None:
                raise ValueError("OCR failed to detect text in the image.")
            print(f"Current brand: {current_brand}")
            
            start = get_region_coor(current_brand)
            if start is None:
                raise ValueError(f"Start coordinates for brand {current_brand} not found.")
            print(f"Start coordinates: {start}")
            
            route = get_route(start, destination)
            print(f"Route: {route}")
            current_coor = start
            
            route_num = 0
            
            while current_coor != route[-1]:
                self.get_direction(route[route_num], route[route_num + 1])
                
                # print(f"Using image path: {self.img_path}")
                current_brand = check_exist(OCR(self.img_path))
                if current_brand is None:
                    raise ValueError("OCR failed to detect text in the image.")
                print(f"Current brand after OCR check: {current_brand}")
                
                current_coor = get_region_coor(current_brand)
                print(f"Current coordinates: {current_coor}")
                if current_coor == route[route_num+1]:
                    route_num += 1
                    # print(route_num)
                elif current_coor != route[route_num+1] and current_coor != route[route_num]:
                    play_audio('audio/redirecting.wav')
                    route = get_route(current_coor, destination)
                    route_num =0
            
            play_audio('audio/arrive.wav')
            self.text_output.insert(tk.END, "Arrived at destination.\n")
            print("Arrived at destination.")

    def get_direction(self, start, end):
        if end[0] - start[0] == 1:
            play_audio('./audio/foward.wav')
            return "Forward"
        elif end[0] - start[0] == -1:
            play_audio('./audio/backward.wav')
            return "Backward"
        elif end[1] - start[1] == 1:
            play_audio('./audio/right.wav')
            return "Right"
        elif end[1] - start[1] == -1:
            play_audio('./audio/left.wav')
            return "Left"
    
    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            # Clear the displayed image on Tkinter
            self.clear_displayed_image()

            self.img_path = file_path
            # print(f"New image path: {self.img_path}")
            self.img = Image.open(file_path)
            self.img.thumbnail((200, 200))
            self.display_image(self.img)
            
            # Add to used_images only if not already present
            if self.img not in self.used_images:
                self.used_images.append(self.img)
            self.display_used_images()
    
    def display_image(self, img):
        img_tk = ImageTk.PhotoImage(img)
        self.image_label.config(image=img_tk)
        self.image_label.image = img_tk
    
    def display_used_images(self):
        for widget in self.used_images_frame.winfo_children():
            widget.destroy()
        for img in self.used_images:
            img_tk = ImageTk.PhotoImage(img)
            label = tk.Label(self.used_images_frame, image=img_tk)
            label.image = img_tk
            label.pack(side=tk.LEFT)

if __name__ == "__main__":
    root = tk.Tk()
    app = NavigationApp(root)
    root.mainloop()
