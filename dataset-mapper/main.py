#!/usr/bin/python

import tkinter as tk
import numpy as np
from PIL import Image, ImageTk
import os
from utils import *


try:
    # Python 2
    xrange
except NameError:
    # Python 3, xrange is now named range
    xrange = range

#setting
wCanvas = 1366
hCanvas = 700
datasave = 'box.csv'
dirimg = 'images/'

class BoundingBox(tk.Tk):

	def cat_select(self, cat):
		def cat_select_function(event):
			self.current_cat = cat
			print(self.current_cat)
			return cat
		
		return cat_select_function


	def __init__(self, categories):
		self.root = tk.Tk.__init__(self)
		self.x = self.y = 0
		self.canvas = tk.Canvas(self, width=wCanvas, height=hCanvas, cursor="cross")

		self.window_width = wCanvas
		self.window_height = hCanvas

		self.canvas.pack(side="top", fill="both", expand=True)
		self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))
		self.canvas.bind("<ButtonPress-1>", self.on_button_press)
		self.canvas.bind("<B1-Motion>", self.on_move_press)
		self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

		self.canvas.focus_set()
		self.canvas.bind("<Left>", self.previmg)
		self.canvas.bind("<Right>", self.nextimg)
		self.canvas.bind("<space>", self.nextimg)
		self.canvas.bind("s", self.saveboxcord)
		self.canvas.bind("d", self.resetbox)

		self.menu_frame = tk.Frame(self.root)
		self.current_cat = categories[0]
		self.cat_buttons = []
		for ind, cat in enumerate(categories):
			btn = tk.Button(self.menu_frame,
						text = str(ind + 1) + " - " + cat,
						width = 10, height = 2,
						bg = "white", fg = "black")

			btn.bind("<Button-1>", self.cat_select(cat))
			btn.grid(row = 2, column = ind )

		for ind, cat in enumerate(categories):
			self.canvas.bind(str(ind + 1), self.cat_select(cat))

		self.menu_frame.pack()
		#add label of numbering
		self.numbering = tk.Label(self, text='0')
		self.numbering.pack(side = "bottom")

		#open data save
		self.allimg = sorted(os.listdir(dirimg))
		self.imgptr = 0
		self.img_scale = 1.0

		self.boxdata = None

		self.allcord = []

		self.allrect = []
		self.rect = None

		self.start_x = None
		self.start_y = None
		self.end_x = None
		self.end_y = None
		self.totwidth = None
		self.totheight = None
		
		self.read_index()

		while (self.allimg[self.imgptr] in self.index):
			self.imgptr += 1

		self._draw_image()
		
	def read_index(self):
		self.index = []

		boxdata = open(datasave, 'r')

		for line in boxdata:
			print(line.split(',')[0])
			self.index.append(line.split(',')[0])
		
		return

	def _draw_image(self):
		self.im = Image.open(dirimg+'/'+self.allimg[self.imgptr])
		self.img_scale = min( self.window_height / self.im.height, self.window_width / self.im.width )
		self.im = self.im.resize( (int(self.im.width * self.img_scale), int(self.im.height * self.img_scale)) )
		self.tk_im = ImageTk.PhotoImage(self.im)
		self.canvas.create_image(0,0,anchor="nw",image=self.tk_im)

	def saveboxcord(self, event):
		self.boxdata = open(datasave, 'a+')
		if (len(self.allcord) == 0):
			self.boxdata.write(self.allimg[self.imgptr] + ", skipped")
			del self.allcord[:]
			del self.allrect[:]
			self.boxdata.close()
			self.numbering.configure(text="box saved")
		else:
			for i in xrange(len(self.allcord)):
				self.boxdata.write(self.allimg[self.imgptr]+','+
				str(self.allcord[i][0])+','+
				str(self.allcord[i][1])+','+
				str(self.allcord[i][2])+','+
				str(self.allcord[i][3])+','+
				str(self.allcord[i][4])+','+
				str(self.allcord[i][5])+','+
				str(self.allcord[i][6])+','+
				str(self.img_scale)+'\n')
			for i in xrange(len(self.allrect)):
				self.canvas.delete(self.allrect[i])
			del self.allcord[:]
			del self.allrect[:]
			self.boxdata.close()
			self.numbering.configure(text="box saved")

	def resetbox(self, event):
		for i in xrange(len(self.allrect)):
			self.canvas.delete(self.allrect[i])
		del self.allcord[:]
		del self.allrect[:]
		self.numbering.configure(text="box reset")

	def nextimg(self, event):
		self.saveboxcord(event)
		for i in xrange(len(self.allrect)):
			self.canvas.delete(self.allrect[i])
		del self.allcord[:]
		del self.allrect[:]
		self.canvas.delete("all")

		self.imgptr += 1

		while (self.allimg[self.imgptr] in self.index):
			self.imgptr += 1

		if self.imgptr > len(self.allimg)-1:
			self.imgptr = 0
		self._draw_image()
		self.numbering.configure(text=str(self.imgptr))

	def previmg(self, event):
		for i in xrange(len(self.allrect)):
			self.canvas.delete(self.allrect[i])
		del self.allcord[:]
		del self.allrect[:]
		self.canvas.delete("all")

		self.imgptr -= 1
		if self.imgptr < 0:
			self.imgptr = len(self.allimg)-1
		self._draw_image()
		self.numbering.configure(text=str(self.imgptr))


	def on_button_press(self, event):
		# save mouse drag start position
		self.start_x = event.x
		self.start_y = event.y

		# create rectangle if not yet exist
		#if not self.rect:
		print(self.current_cat)
		self.canvas.create_text(event.x, event.y - 10, text = self.current_cat, fill = 'green')
		self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, outline='green', width=3)

	def on_move_press(self, event):
		curX, curY = (event.x, event.y)

		if curX > wCanvas:
			curX = wCanvas
		if curY > hCanvas:
			curY = hCanvas

		self.end_x = curX
		self.end_y = curY

		# expand rectangle as you drag the mouse
		self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)



	def on_button_release(self, event):
		self.imarray = np.array(self.im)
		self.totwidth = len(self.imarray)
		self.totheight = len(self.imarray[0])
		print(self.start_x, self.start_y, self.end_x, self.end_y, self.totwidth, self.totheight, self.current_cat)
		self.allcord.append([self.start_x, self.start_y, self.end_x, self.end_y, self.totwidth, self.totheight, self.current_cat])
		self.allrect.append(self.rect)
		print (len(self.allcord))


if __name__ == "__main__":

	categories = load_categories("categories.txt")

	draw = BoundingBox(categories)
	draw.mainloop()
