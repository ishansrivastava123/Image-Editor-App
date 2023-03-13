
from tkinter import ttk, Tk, PhotoImage, filedialog, Canvas, colorchooser, Scale, GROOVE, HORIZONTAL,  ROUND, RIDGE
import cv2
from PIL import ImageTk, Image
import numpy as np

class FrontEnd:
    def __init__(self, master):
        self.master = master
        self.master.geometry("840x610+50+20")
        self.master.title("Image Editor app using Tkinter and OpenCV")

# **********************************************************Header**********************************************************

        self.frame_header = ttk.Frame(self.master)
        self.frame_header.pack()

        self.logo = PhotoImage(file = "python_logo.gif").subsample(3, 3)
        ttk.Label(self.frame_header, image = self.logo).grid(row = 0, column = 0, rowspan = 2, padx = (20, 20), pady = (10, 10))
        ttk.Label(self.frame_header, text = "Welcome to the Image Editor app!").grid(row = 0, column = 1, columnspan = 1, pady = (10, 0))
        ttk.Label(self.frame_header, text = "Upload, edit and save your images easily!").grid(row = 1, column = 1, columnspan = 1, pady = (0, 10))
        ttk.Label(self.frame_header, image = self.logo).grid(row = 0, column = 2, rowspan = 2, padx = (20, 20), pady = (10, 10))

# **********************************************************Header**********************************************************

# **********************************************************Main Menu**********************************************************

        self.frame_menu = ttk.Frame(self.master)
        self.frame_menu.pack()
        self.frame_menu.config(relief = RIDGE, padding = (50, 15))

        ttk.Button(self.frame_menu, text = "Upload an Image", command = self.upload_action).grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "w")
        ttk.Button(self.frame_menu, text = "Crop Image", command = self.crop_action).grid(row = 1, column = 0, padx = 5, pady = 5, sticky = "w")
        ttk.Button(self.frame_menu, text = "Add Text", command = self.text_action_1).grid(row = 2, column = 0, padx = 5, pady = 5, sticky = "w")
        ttk.Button(self.frame_menu, text = "Draw Over Image", command = self.draw_action).grid(row = 3, column = 0, padx = 5, pady = 5, sticky = "w")
        ttk.Button(self.frame_menu, text = "Apply Filters", command = self.filter_action).grid(row = 4, column = 0,  padx = 5, pady = 5, sticky = "w")
        ttk.Button(self.frame_menu, text = "Blur/Smoothening", command = self.blur_action).grid(row = 5, column = 0, padx = 5, pady = 5, sticky = "w")
        ttk.Button(self.frame_menu, text = "Adjust Levels", command = self.adjust_action).grid(row = 6, column = 0, padx = 5, pady = 5, sticky = "w")
        ttk.Button(self.frame_menu, text = "Rotate", command = self.rotate_action).grid(row = 7, column = 0, padx = 5, pady = 5, sticky = "w")
        ttk.Button(self.frame_menu, text = "Flip", command = self.flip_action).grid(row = 8, column = 0, padx = 5, pady = 5, sticky = "w")
        ttk.Button(self.frame_menu, text = "Save As", command = self.save_action).grid(row = 9, column = 0, padx = 5, pady = 5, sticky = "w")

        self.canvas = Canvas(self.frame_menu, bg = "gray", width = 300, height = 400)
        self.canvas.grid(row = 0, column = 1, rowspan = 10, padx = 20)

# **********************************************************Main Menu**********************************************************

# **********************************************************Footer Menu**********************************************************

        self.frame_footer = ttk.Frame(self.master)
        self.frame_footer.pack()

        ttk.Label(self.frame_footer, text = 'Click "Apply" after every edit to retain the effect!').grid(row = 0, column = 0, columnspan = 3, padx = 10, pady = (15, 10))
        ttk.Button(self.frame_footer, text = "Apply", command = self.apply_action).grid(row = 1, column = 0, padx = 10, pady = (0, 20))
        ttk.Button(self.frame_footer, text = "Cancel", command = self.cancel_action).grid(row = 1, column = 1, padx = 10, pady = (0, 20))
        ttk.Button(self.frame_footer, text = "Revert All Changes", command = self.revert_action).grid(row = 1, column = 2, padx = 10, pady = (0, 20))
        
# **********************************************************Footer Menu**********************************************************


# **********************************************************Functions**********************************************************

# **********************************************************Refreshing Side Frame**********************************************************
        
    def refresh_side_frame(self):
        try:
            self.side_frame.grid_forget()
        except:
            pass
        
        self.side_frame = ttk.Frame(self.frame_menu)
        self.side_frame.grid(row = 0, column = 2, rowspan = 10, padx = (20, 0))
        self.side_frame.config(relief = GROOVE, padding = (50, 15))

# **********************************************************Refreshing Side Frame**********************************************************

# **********************************************************Upload Function**********************************************************
    
    def upload_action(self):
        self.canvas.delete("all")
        self.filename = filedialog.askopenfilename()

        self.original_image = cv2.imread(self.filename)
        self.edited_image = cv2.imread(self.filename)
        self.filtered_image = cv2.imread(self.filename)
        self.display_image(self.edited_image)

# **********************************************************Upload Function**********************************************************

# **********************************************************Crop Function**********************************************************

    def crop_action(self):
        try:
            self.side_frame.grid_forget()
        except:
            pass
        # self.crop_label = ttk.Label(self.side_frame, text = "Drag on the image to crop").pack()
        self.rectangle_id = 0
        self.crop_start_x = 0
        self.crop_start_y = 0
        self.crop_end_x = 0
        self.crop_end_y = 0
        self.canvas.bind("<ButtonPress>", self.start_crop)
        self.canvas.bind("<B1-Motion>", self.crop)
        self.canvas.bind("<ButtonRelease>", self.end_crop)

    def start_crop(self, event):
        self.crop_start_x = event.x
        self.crop_start_y = event.y

    def crop(self, event):
        if self.rectangle_id:
            self.canvas.delete(self.rectangle_id)
        self.crop_end_x = event.x
        self.crop_end_y = event.y
        self.rectangle_id = self.canvas.create_rectangle(self.crop_start_x, self.crop_start_y, self.crop_end_x, self.crop_end_y, width = 1)

    def end_crop(self, event):
        if (self.crop_start_x <= self.crop_end_x) and (self.crop_start_y <= self.crop_end_y):
            start_x = int(self.crop_start_x * self.ratio)
            start_y = int(self.crop_start_y * self.ratio)
            end_x = int(self.crop_end_x * self.ratio)
            end_y = int(self.crop_end_y * self.ratio)
        elif (self.crop_start_x > self.crop_end_x) and (self.crop_start_y <= self.crop_end_y):
            start_x = int(self.crop_end_x * self.ratio)
            start_y = int(self.crop_start_y * self.ratio)
            end_x = int(self.crop_start_x * self.ratio)
            end_y = int(self.crop_end_y * self.ratio)
        elif (self.crop_start_x <= self.crop_end_x) and (self.crop_start_y > self.crop_end_y):
            start_x = int(self.crop_start_x * self.ratio)
            start_y = int(self.crop_end_y * self.ratio)
            end_x = int(self.crop_end_x * self.ratio)
            end_y = int(self.crop_start_y * self.ratio)
        else:
            start_x = int(self.crop_end_x * self.ratio)
            start_y = int(self.crop_end_y * self.ratio)
            end_x = int(self.crop_start_x * self.ratio)
            end_y = int(self.crop_start_y * self.ratio)
        x = slice(start_x, end_x, 1)
        y = slice(start_y, end_y, 1)
        self.filtered_image = self.edited_image[y, x]
        self.display_image(self.filtered_image)

# **********************************************************Crop Function**********************************************************

# **********************************************************Add Text Function**********************************************************

    def text_action_1(self):
        self.text_extracted = "Text Here!"
        self.refresh_side_frame()
        ttk.Label(self.side_frame, text = "Enter the text!").grid(row = 0, column = 0, pady = 5)
        self.text_on_image = ttk.Entry(self.side_frame)
        self.text_on_image.grid(row = 1, column = 0, pady = 5)
        ttk.Button(self.side_frame, text = "Pick A Font Color", command = self.choose_color).grid(row = 2, column = 0, pady = 5)
        self.text_action()

    def text_action(self):
        self.rectangle_id = 0
        self.crop_start_x = 0
        self.crop_start_y = 0
        self.crop_end_x = 0
        self.crop_end_y = 0
        self.canvas.bind("<ButtonPress>", self.start_crop)
        self.canvas.bind("<B1-Motion>", self.crop)
        self.canvas.bind("<ButtonRelease>", self.end_text_crop)

    def end_text_crop(self, event):
        if self.crop_start_x <= self.crop_end_x and self.crop_start_y <= self.crop_end_y:
            start_x = int(self.crop_start_x * self.ratio)
            start_y = int(self.crop_start_y * self.ratio)
            end_x = int(self.crop_end_x * self.ratio)
            end_y = int(self.crop_end_y * self.ratio)
        elif self.crop_start_x > self.crop_end_x and self.crop_start_y <= self.crop_end_y:
            start_x = int(self.crop_end_x * self.ratio)
            start_y = int(self.crop_start_y * self.ratio)
            end_x = int(self.crop_start_x * self.ratio)
            end_y = int(self.crop_end_y * self.ratio)
        elif self.crop_start_x <= self.crop_end_x and self.crop_start_y > self.crop_end_y:
            start_x = int(self.crop_start_x * self.ratio)
            start_y = int(self.crop_end_y * self.ratio)
            end_x = int(self.crop_end_x * self.ratio)
            end_y = int(self.crop_start_y * self.ratio)
        else:
            start_x = int(self.crop_end_x * self.ratio)
            start_y = int(self.crop_end_y * self.ratio)
            end_x = int(self.crop_start_x * self.ratio)
            end_y = int(self.crop_start_y * self.ratio)
        if self.text_on_image.get():
            self.text_extracted = self.text_on_image.get()
        start_font = start_x, start_y
        #((r,g,b),'#ff00000')
        print(self.color_code)
        r, g, b = tuple(map(int, self.color_code[0]))
        self.filtered_image = cv2.putText(
            self.edited_image, self.text_extracted, start_font, cv2.FONT_HERSHEY_SIMPLEX, 2, (b, g, r), 5)
        self.display_image(self.filtered_image)

# **********************************************************Add Text Function**********************************************************

# **********************************************************Draw Function**********************************************************

    def draw_action(self):
        self.color_code = ((255, 0 , 0), "#ff0000")
        self.refresh_side_frame()
        self.canvas.bind("<ButtonPress>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.draw_color_button = ttk.Button(self.side_frame, text = "Pick a color", command = self.choose_color)
        self.draw_color_button.grid(row = 0, column = 0, pady = 5)

    def start_draw(self, event):
        self.x = event.x
        self.y = event.y
        self.draw_ids = []

    def draw(self, event):
        r, g, b = (tuple(map(int, self.color_code[0])))
        self.draw_ids.append(self.canvas.create_line(self.x, self.y, event.x, event.y, width = 2, fill = self.color_code[-1], capstyle = ROUND, smooth = True))
        cv2.line(self.filtered_image, (int(self.x * self.ratio), int(self.y * self.ratio)), (int(event.x * self.ratio), int(event.y * self.ratio)), (b, g, r), thickness = int(self.ratio * 2), lineType = 8)
        self.x = event.x
        self.y = event.y

# **********************************************************Draw Function**********************************************************

# **********************************************************Color Chooser Function**********************************************************

    def choose_color(self):
        self.color_code = colorchooser.askcolor(title = "Choose Color")

# **********************************************************Color Chooser Function**********************************************************

# **********************************************************Filters Function**********************************************************

    def filter_action(self):
        self.refresh_side_frame()
        ttk.Button(self.side_frame, text = "Negative", command = self.negative_action).grid(row = 0, column = 0, pady = 5)
        ttk.Button(self.side_frame, text = "Black & White", command = self.bw_action).grid(row = 2, column = 0, pady = 5)
        ttk.Button(self.side_frame, text = "Stylisation", command = self.stylisation_action).grid(row = 4, column = 0, pady = 5)
        ttk.Button(self.side_frame, text = "Sketch Effect", command = self.sketch_action).grid(row = 6, column = 0, pady = 5)
        ttk.Button(self.side_frame, text = "Emboss", command = self.emb_action).grid(row = 8, column = 0, pady = 5)
        ttk.Button(self.side_frame, text = "Sepia", command = self.sepia_action).grid(row = 10, column = 0, pady = 5)
        ttk.Button(self.side_frame, text = "Binary Thresh", command = self.binary_threshold_action).grid(row = 12, column = 0, pady = 5)
        ttk.Button(self.side_frame, text = "Erosion", command = self.erosion_action).grid(row = 14, column = 0, pady = 5)
        ttk.Button(self.side_frame, text = "Dilation", command = self.dilation_action).grid(row = 16, column = 0, pady = 5)

        # For more photorealistic effects, visit: https://learnopencv.com/non-photorealistic-rendering-using-opencv-python-c/

    def negative_action(self):
        self.filtered_image = cv2.bitwise_not(self.edited_image)
        self.display_image(self.filtered_image)

    def bw_action(self):
        self.filtered_image = cv2.cvtColor(self.edited_image, cv2.COLOR_BGR2GRAY)
        self.display_image(self.filtered_image)

    def stylisation_action(self):
        self.filtered_image = cv2.stylization(self.edited_image, sigma_s = 1, sigma_r = 0.25)
        self.display_image(self.filtered_image)

    def sketch_action(self):
        ret, self.filtered_image = cv2.pencilSketch(self.edited_image, sigma_s = 60, sigma_r = 0.5, shade_factor = 0.01)
        # img_gray = cv2.cvtColor(self.edited_image, cv2.COLOR_BGR2GRAY)
        # img_blur = cv2.GaussianBlur(img_gray, (21, 21), 0, 0)
        # self.filtered_image = cv2.divide(img_gray, img_blur, scale=256)
        self.display_image(self.filtered_image)

    def emb_action(self):
        kernel = np.array([[-1, 0, 0,],
                          [0, 1, 0,],
                          [0, 0, 0]])
        self.filtered_image = cv2.filter2D(self.original_image, -1, kernel)
        self.display_image(self.filtered_image)

    def sepia_action(self):
        kernel = np.array([[0.272, 0.534, 0.131],
                           [0.349, 0.686, 0.168],
                           [0.393, 0.769, 0.189]])
        self.filtered_image = cv2.filter2D(self.original_image, -1, kernel)
        self.display_image(self.filtered_image)

    def binary_threshold_action(self):
        ret, self.filtered_image = cv2.threshold(self.original_image, 120, 255, cv2.THRESH_BINARY)
        self.display_image(self.filtered_image)

    def erosion_action(self):
        kernel = np.ones((5, 5), np.uint8)
        self.filtered_image = cv2.erode(self.original_image, kernel, iterations = 1)
        self.display_image(self.filtered_image)

    def dilation_action(self):
        kernel = np.ones((5, 5), np.uint8)
        self.filtered_image = cv2.dilate(self.original_image, kernel, iterations = 1)
        self.display_image(self.filtered_image)

# **********************************************************Filters Function**********************************************************

# **********************************************************Blur/Smoothning Function**********************************************************

    def blur_action(self):
        self.refresh_side_frame()
        
        ttk.Label(self.side_frame, text = "Averaging Blur", ).grid(row = 0, column = 0)
        self.average_slider = Scale(self.side_frame, from_ = 0, to = 255, orient = HORIZONTAL, command = self.averaging_action)
        self.average_slider.grid(row = 1, column = 0, pady = (0, 20))

        ttk.Label(self.side_frame, text = "Gaussian Blur").grid(row = 2, column = 0)
        self.gaussian_slider = Scale(self.side_frame, from_ = 0, to = 255, orient = HORIZONTAL, command = self.gaussian_action)
        self.gaussian_slider.grid(row = 3, column = 0, pady = (0, 20))
        
        ttk.Label(self.side_frame, text = "Median Blur").grid(row = 4, column = 0)
        self.median_slider = Scale(self.side_frame, from_ = 0, to = 255, orient = HORIZONTAL, command = self.median_action)
        self.median_slider.grid(row = 5, column = 0)

    def averaging_action(self, value):
        value = int(value)
        # This code is the alternative of the above line & works exactly similarly: value = self.average_slider.get()
        if (value % 2 == 0):
            value += 1
        self.filtered_image = cv2.blur(self.edited_image, (value, value))
        self.display_image(self.filtered_image)

    def gaussian_action(self, value):
        value = int(value)
        if (value % 2 == 0):
            value += 1
        self.filtered_image = cv2.GaussianBlur(self.edited_image, (value, value), 0)
        self.display_image(self.filtered_image)

    def median_action(self, value):
        value = int(value)
        if (value % 2 == 0):
            value += 1
        self.filtered_image = cv2.medianBlur(self.edited_image, value)
        self.display_image(self.filtered_image)

# **********************************************************Blur/Smoothning Function**********************************************************

# **********************************************************Adjust (Brightness/Contrast) Function**********************************************************

    def adjust_action(self):
        self.refresh_side_frame()
        
        ttk.Label(self.side_frame, text = "Brightness").grid(row = 0, column = 0)
        self.brightness_slider = Scale(self.side_frame, from_ = -127, to = 127, orient = HORIZONTAL, command = self.brightness_action)
        self.brightness_slider.grid(row = 1, column = 0, pady = (0, 20))
        self.brightness_slider.set(0)

        ttk.Label(self.side_frame, text = "Contrast").grid(row = 2, column = 0)
        self.contrast_slider = Scale(self.side_frame, from_ = 0, to = 2, orient = HORIZONTAL, resolution = 0.1, command = self.contrast_action)
        self.contrast_slider.grid(row = 3, column = 0, pady = (0, 20))
        self.contrast_slider.set(1)
        
        # ttk.Label(self.side_frame, text = "Saturation").grid(row = 4, column = 0)
        # self.saturation_slider = Scale(self.side_frame, from_ = -100.0, to = 100.0, orient = HORIZONTAL, resolution = 0.5)
        # self.saturation_slider.grid(row = 5, column = 0)
        # self.saturation_slider.set(0.0)

    def brightness_action(self, value):
        value = int(value)
        self.filtered_image = cv2.convertScaleAbs(self.edited_image, 1, ((value + 127) / 127))
        self.display_image(self.filtered_image)

    def contrast_action(self, value):
        value = float(value)
        self.filtered_image = cv2.convertScaleAbs(self.edited_image, alpha = value, beta = 1)
        self.display_image(self.filtered_image)

# **********************************************************Adjust (Brightness/Contrast) Function**********************************************************

# **********************************************************Rotate Function**********************************************************

    def rotate_action(self):
        self.refresh_side_frame()
        ttk.Button(self.side_frame, text = "Rotate Left ⭯", command = self.rotate_left_action).grid(row = 0, column = 0, pady = 5)
        ttk.Button(self.side_frame, text = "Rotate Right ⭮", command = self.rotate_right_action).grid(row = 1, column = 0, pady = 5)

    def rotate_left_action(self):
        self.filtered_image = cv2.rotate(self.filtered_image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        self.display_image(self.filtered_image)

    def rotate_right_action(self):
        self.filtered_image = cv2.rotate(self.filtered_image, cv2.ROTATE_90_CLOCKWISE)
        self.display_image(self.filtered_image)

# **********************************************************Rotate Function**********************************************************

# **********************************************************Flip Function**********************************************************

    def flip_action(self):
        self.refresh_side_frame()
        ttk.Button(self.side_frame, text = "Vertical Flip", command = self.vertical_action).grid(row = 0, column = 0, pady = 5)
        ttk.Button(self.side_frame, text = "Horizontal Flip", command = self.horizontal_action).grid(row = 1, column = 0, pady = 5)

    def vertical_action(self):
        self.filtered_image = cv2.flip(self.filtered_image, 0)
        self.display_image(self.filtered_image)

    def horizontal_action(self):
        self.filtered_image = cv2.flip(self.filtered_image, 1)
        self.display_image(self.filtered_image)

# **********************************************************Flip Function**********************************************************

# **********************************************************Apply/Cancel/Revert Function**********************************************************

    def apply_action(self):
        self.edited_image = self.filtered_image
        self.display_image(self.edited_image)
        
    def cancel_action(self):
        self.display_image(self.edited_image)
        
    def revert_action(self):
        self.edited_image = self.original_image.copy()
        self.display_image(self.original_image)

# **********************************************************Apply/Cancel/Revert Function**********************************************************

# **********************************************************Save Function**********************************************************

    def save_action(self):
        try:
            self.side_frame.grid_forget()
        except:
            pass
        original_file_type = self.filename.split(".")[-1]
        filename = filedialog.asksaveasfilename()
        filename = filename + "." + original_file_type
        save_as_image = self.edited_image
        cv2.imwrite(filename, save_as_image)
        self.filename = filename

# **********************************************************Save Function**********************************************************

# **********************************************************Canvas Display Function**********************************************************
        
    def display_image(self, image = None):
        self.canvas.delete("all")

        if image is None:
            image = self.edited_image.copy()
        else:
            image = image

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, channel = image.shape

        new_height = height
        new_width = width
        ratio = height / width

        if (height > 400) or (width > 300):
            if (ratio < 1):
                new_width = 300
                new_height = int(new_width * ratio)
            elif (ratio > 1):
                new_height = 400
                new_width = int(new_height / ratio)
        
        self.ratio = height / new_height

        self.new_image = cv2.resize(image, (new_width, new_height))
        self.new_image = ImageTk.PhotoImage(Image.fromarray(self.new_image))

        self.canvas.config(height = new_height, width = new_width)
        self.canvas.create_image(new_width / 2, new_height / 2, image = self.new_image)

# **********************************************************Canvas Display Function**********************************************************

root = Tk()

FrontEnd(root)

root.mainloop()