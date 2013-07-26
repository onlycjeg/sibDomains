#!-*-encoding:utf8-*-

'''
given a domain name,
I'll find all sib domians hosted on the same DNS server
from http://www.lijiejie.com
'''

from Tkinter import *
import urllib2
import re
import tkMessageBox
import time

class domainAPP(Tk):
	def __init__(self):
		Tk.__init__(self)
		self.title('sibDomains - By LiJieJie')
		self.geometry("400x300+300+200")
		self.minsize(400,300)

		self.label = Label(self,text='Enter a domain name to search its sib domains:', \
					  anchor=W, justify=LEFT, padx=10, pady=10)
		self.label.grid(row=0, column=0, columnspan=2, sticky=W)

		self.entry = Entry(self, width=40)
		self.entry.grid(row=1, column=0, sticky=W, padx=10)
		self.entry.bind("<KeyRelease-Return>", self.cmd_click)    #bind <Enter>
		self.entry.focus_set()

		self.button = Button(self, text="search", width=10)
		self.button.grid(row=1, column=1)

		self.button.bind('<Button-1>', self.cmd_click)    #bind left mouseclick

		self.scrollbar = Scrollbar(self, orient=VERTICAL)
		self.listbox = Listbox(self, width=40, yscrollcommand = self.scrollbar.set)
		self.listbox.grid(row=2, column=0, sticky=W, padx=10, pady=20)
		self.listbox.insert(END, 'ready.')
		self.scrollbar.grid(row=2, column=1, sticky=W+N+S, pady=20)
		self.scrollbar.config(command=self.listbox.yview)


		self.mainloop()

	def cmd_click(self, event):
		self.listbox.delete(0, END)
		self.listbox.insert(END, 'search DNS server...')
		domain = self.entry.get()
		self.update()
		html_doc = urllib2.urlopen('http://who.cndns.com/?d=' + domain).read()
		match = re.search(r'Name Server:([^<]+)', html_doc)
		if not match:
			self.listbox.insert(END, 'Couldn\'t find corresponding DNS server')
			tkMessageBox.showerror(
				"Error",
				"Couldn't find DNS server for\n" + self.entry.get()
			)
			return
		DNS = match.group(1).strip()
		self.listbox.insert(END, 'DNS found: ' + DNS )
		self.fetch(DNS)

	def fetch(self, DNS):
		start = 1
		headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.94 Safari/537.4'}
		with open(self.entry.get() + '.txt', 'w') as outFile:
			while True:
				req = urllib2.Request(url='http://www.sitedossier.com/nameserver/' + DNS + '/' + str(start), headers=headers)
				try:
					html_doc = ''
					html_doc = urllib2.urlopen(req).read()
				except:
					pass
				pat = re.compile(r'<a href="/site/.*">http://(.*)</a><br>')
				links = pat.findall(html_doc)
				if not links:
					self.listbox.insert(END, 'Done.')
					break
				for link in links:
					curDomain = link.rstrip('.').strip('/')
					self.listbox.insert(END, curDomain)
					outFile.write(curDomain + '\n')
				start += 100			

app = domainAPP()
app.mainloop()







    