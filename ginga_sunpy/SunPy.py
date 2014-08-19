"""
Author : Rajul

A Ginga global plugin called 'SunPy'

To enable it, run ginga with the command
    $ ginga --modules=SunPy

it should become active in the right panel.
"""
__all__ = ['SunPy']

# importing the Ginga modules required by a Ginga Plugin
from ginga import GingaPlugin, cmap
from ginga.misc import Widgets
from ginga.qtw.ImageViewQt import ImageViewZoom
from ginga import AstroImage
from ginga.qtw.QtHelp import QtGui, QtCore
from ginga.qtw import QtHelp

# importing the other modules
import sys, os
import numpy as np

# importing the SunPy databse module
import matplotlib as mpl
mpl.use("Agg")
from sunpy.database import Database
import sunpy.database
import sunpy
import sunpy.map
from sunpy.database.tables import display_entries
from sunpy.net import vso

class SunPy(GingaPlugin.GlobalPlugin):

    def __init__(self, fv):
        """
        This method is called when the plugin is loaded for the  first
        time.  ``fv`` is a reference to the Ginga (reference viewer) shell.

        You need to call the superclass initializer and then do any local
        initialization.
        """
        super(SunPy, self).__init__(fv)

        # Your initialization here

        # Create some variables to keep track of what is happening
        # with which channel
        self.active = None

        # Subscribe to some interesting callbacks that will inform us
        # of channel events.  You may not need these depending on what
        # your plugin does
        fv.set_callback('add-channel', self.add_channel)
        fv.set_callback('delete-channel', self.delete_channel)
        fv.set_callback('active-image', self.focus_cb)

    def build_gui(self, container):
        """
        This method is called when the plugin is invoked.  It builds the
        GUI used by the plugin into the widget layout passed as
        ``container``.
        This method could be called several times if the plugin is opened
        and closed.  The method may be omitted if there is no GUI for the
        plugin.

        This specific example uses the GUI widget set agnostic wrappers
        to build the GUI, but you can also just as easily use explicit
        toolkit calls here if you only want to support one widget set.
        """
        top = Widgets.VBox()
        top.set_border_width(4)

        # this is a little trick for making plugins that work either in
        # a vertical or horizontal orientation.  It returns a box container,
        # a scroll widget and an orientation ('vertical', 'horizontal')
        vbox, sw, orientation = Widgets.get_oriented_box(container)
        vbox.set_border_width(4)
        vbox.set_spacing(2)

        # Take a text widget to show some instructions
        self.msgFont = self.fv.getFont("sansFont", 12)
        tw = Widgets.TextArea(wrap=True, editable=False)
        tw.set_font(self.msgFont)
        self.tw = tw

        # Database Parameters
        db_parameters_frame = self.add_db_parameters_to_gui()
        vbox.add_widget(db_parameters_frame, stretch=0)

        # Database Default Values
        db_default_values_frame = self.add_db_default_values_to_gui()
        vbox.add_widget(db_default_values_frame, stretch=0)

        #Adding Buttons
        connect_db_button = Widgets.Button(text="Connect")
        self.connect_db_button = connect_db_button
        connect_db_button.add_callback('activated', lambda w: self.connect_db())

        view_db_button = Widgets.Button(text="View Database")
        self.view_db_button = view_db_button
        view_db_button.add_callback('activated', lambda w: self.view_database())

        add_file_to_db_button = Widgets.Button(text="Add file to Database")
        self.add_file_to_db_button = add_file_to_db_button
        add_file_to_db_button.add_callback('activated', lambda w: self.add_file())

        open_db_button = Widgets.Button(text="Open Database")
        self.open_db_button = open_db_button
        open_db_button.add_callback('activated', lambda w: self.open_sqlite_database())

        commit_db_button = Widgets.Button(text="Commit changes to Database")
        self.commit_db_button = commit_db_button
        commit_db_button.add_callback('activated', lambda w: self.commit_database())

        vbox.add_widget(connect_db_button)
        vbox.add_widget(view_db_button)
        vbox.add_widget(add_file_to_db_button)
        vbox.add_widget(open_db_button)
        vbox.add_widget(commit_db_button)

        # Frame for instructions and add the text widget with another
        # blank widget to stretch as needed to fill emp
        fr = Widgets.Frame("Status")
        vbox2 = Widgets.VBox()
        vbox2.add_widget(tw)
        vbox2.add_widget(Widgets.Label(''), stretch=1)
        fr.set_widget(vbox2)
        vbox.add_widget(fr, stretch=0)


        # Add a spacer to stretch the rest of the way to the end of the
        # plugin space
        spacer = Widgets.Label('')
        vbox.add_widget(spacer, stretch=1)

        # scroll bars will allow lots of content to be accessed
        top.add_widget(sw, stretch=1)

        # A button box that is always visible at the bottom
        btns = Widgets.HBox()
        btns.set_spacing(3)

        # Add a close button for the convenience of the user
        btn = Widgets.Button("Close")
        btn.add_callback('activated', lambda w: self.close())
        btns.add_widget(btn, stretch=0)
        btns.add_widget(Widgets.Label(''), stretch=1)
        top.add_widget(btns, stretch=0)

        # Add our GUI to the container
        container.add_widget(top, stretch=1)
        # NOTE: if you are building a GUI using a specific widget toolkit
        # (e.g. Qt) GUI calls, you need to extract the widget or layout
        # from the non-toolkit specific container wrapper and call on that
        # to pack your widget, e.g.:
        #cw = container.get_widget()
        #cw.addWidget(widget, stretch=1)

    def add_db_parameters_to_gui(self):
<<<<<<< HEAD
        '''
          This functions adds the components for the entry of Database
          parameters to the GUI          
        '''

=======
    	# Frame for datebase parameters
>>>>>>> 164c40fecd99baf9d1f5cb27064620ff454692d3
        db_parameters_frame = Widgets.Frame("Database Parameters")
        db_parameters_vbox = Widgets.VBox()

        db_driver = Widgets.TextEntry("sqlite")
        db_name = Widgets.TextEntry("sunpydb")
        db_user = Widgets.TextEntry()
        db_passwd = Widgets.TextEntry()

        self.db_driver = db_driver
        self.db_name = db_name
        self.db_user = db_user
        self.db_passwd = db_passwd

        db_driver_label = Widgets.Label(text="Driver Name")
        db_name_label = Widgets.Label(text="Database Name")
        db_user_label = Widgets.Label(text="User Name")
        db_passwd_label = Widgets.Label(text="Password")

        self.db_driver_label = db_driver_label
        self.db_name_label = db_name_label
        self.db_user_label = db_user_label
        self.db_passwd_label = db_passwd_label

        db_parameters_vbox.add_widget(db_driver_label)
        db_parameters_vbox.add_widget(db_driver)
        db_parameters_vbox.add_widget(db_name_label)
        db_parameters_vbox.add_widget(db_name)
        db_parameters_vbox.add_widget(db_user_label)
        db_parameters_vbox.add_widget(db_user)
        db_parameters_vbox.add_widget(db_passwd_label)
        db_parameters_vbox.add_widget(db_passwd)

        db_parameters_vbox.add_widget(Widgets.Label(''), stretch=1)
        db_parameters_frame.set_widget(db_parameters_vbox)

        return db_parameters_frame

    def add_db_default_values_to_gui(self):
        '''
          This functions adds the components for the entry of default values of
          the database to the GUI          
        '''

        db_default_values_frame = Widgets.Frame("Options")
        db_default_values_vbox = Widgets.VBox()

        # Wrapping Default Wavelength Label and ComboBox in a HBox
        default_wavelength_hbox = Widgets.HBox()
        default_wavelength_hbox.set_spacing(3)

        default_wavelength_label = Widgets.Label(text="Default Wavelength")
        self.default_wavelength_label = default_wavelength_label

        default_wavelength = Widgets.ComboBox()
        default_wavelength.insert_alpha('angstrom')
        default_wavelength.append_text('nm')
        self.default_wavelength = default_wavelength

        default_wavelength_hbox.add_widget(default_wavelength_label, stretch=0)
        default_wavelength_hbox.add_widget(default_wavelength, stretch=0)
        default_wavelength_hbox.add_widget(Widgets.Label(''), stretch=1)
        db_default_values_vbox.add_widget(default_wavelength_hbox, stretch=0)

        set_default_box = Widgets.CheckBox("Set Current Database as default")
        self.set_default_box = set_default_box
        db_default_values_vbox.add_widget(set_default_box)

        db_default_values_vbox.add_widget(Widgets.Label(''), stretch=1)
        db_default_values_frame.set_widget(db_default_values_vbox)

        return db_default_values_frame

    def connect_db(self, conn_string=''):
<<<<<<< HEAD
      '''
        This function creates a database connection based on the parameters
        specified in the GUI.

        Parameters: conn_string (string of the connection for the object) Optional
        
      '''

=======
>>>>>>> 164c40fecd99baf9d1f5cb27064620ff454692d3
    	def_wavelength = self.default_wavelength.get_widget().currentText()

    	try:
    		if conn_string == '':
    			conn_string = sunpy.config.get('database', 'url')
    		global database
    		database = Database(conn_string, default_waveunit=def_wavelength)
    	except:
    		conn_string = self.get_conn_string()
    		global database
    		database = Database(conn_string, default_waveunit=def_wavelength)

    	if self.set_default_box.get_state():
    		self.set_default_db(conn_string)

    	self.set_info("Database Connected at %s"%conn_string)
    	return database

    def get_conn_string(self):
      '''
        Gets the connection string based on the values specified in the GUI
      '''

    	conn_string = ''

    	db_driver = self.db_driver.get_text()
    	db_name = self.db_name.get_text()
    	db_user = self.db_user.get_text()
    	db_passwd = self.db_passwd.get_text()

    	if db_user != '' and db_passwd != '':
    		user_string = db_user + ':' + db_passwd
    	else:
    		user_string = ''

    	if db_driver == '':
    		db_driver = 'sqlite'

    	if db_name == '':
    		db_name = config.get('general', 'working_dir') + 'sunpydb'

    	# print db_name

    	conn_string = db_driver + '://' + user_string+ '/' + db_name
    	return conn_string

    def get_data_from_db(self):
      '''
        Gets the data from all the entries from the database and return then in
        the form of a list
      '''
    	queries = []

    	for entry in database:
    		q = []

    		q.append(entry.id)
    		q.append(entry.path.split('/')[-1])
    		q.append(entry.observation_time_start)
    		q.append(entry.observation_time_end)
    		q.append(entry.instrument)
    		q.append(entry.wavemin)
    		q.append(entry.wavemax)
    		q.append(entry.starred)

    		queries.append(q)

    	return queries

    def get_data_from_selected_entries(self, entries):
      '''
        Gets the data from seleted entries from the database and return then in
        the form of a list
      '''
    	queries = []

    	for entry in entries:
    		q = []

    		q.append(entry.id)
    		q.append(entry.path.split('/')[-1])
    		q.append(entry.observation_time_start)
    		q.append(entry.observation_time_end)
    		q.append(entry.instrument)
    		q.append(entry.wavemin)
    		q.append(entry.wavemax)
    		q.append(entry.starred)

    		queries.append(q)

    	return queries

    def view_database(self, selected_entries=None):
      '''
        Logic for creating and viewing of a tab with the database table
      '''

    	table_headers = ['id', 'File', 'Observation Time Start', 'Observation Time End', 'Instrument', 'Min Wavelength', 'Max Wavelength', 'Starred']
    	self.table_headers = table_headers

    	vbox = QtHelp.VBox()

    	filter_label = QtGui.QLabel("Filter")
    	self.filter_label = filter_label
    	filter_select = QtGui.QComboBox()

    	search_box = QtGui.QLineEdit()
    	search_box.textChanged.connect(self.query)
    	self.search_box = search_box

<<<<<<< HEAD
=======
    	# search_boxes = {}

    	# for i in table_headers:
    	# 	search = Widgets.TextEntry()
    	# 	search_boxes[i] = search.get_widget()
    	# 	search_boxes[i].textChanged.connect(self.query)

    	# self.search_boxes = search_boxes

>>>>>>> 164c40fecd99baf9d1f5cb27064620ff454692d3
    	if selected_entries == None:
    		selected_entries = database

    	queries = self.get_data_from_selected_entries(selected_entries)

    	wtable = QtGui.QTableWidget(len(queries), len(table_headers))

    	for i, row in enumerate(queries):
    		for j, col in enumerate(row):
    			item = QtGui.QTableWidgetItem(str(col))
    			wtable.setItem(i, j, item)

    	wtable.itemClicked.connect(self.on_table_row_click)
    	wtable.setHorizontalHeaderLabels(table_headers)
    	wtable.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)

    	self.wtable = wtable

    	if 'sunpydb' in self.fv.ds.get_tabnames():
    		self.fv.ds.remove_tab("sunpydb")

    	filter_select.addItems(self.table_headers[:-1])
    	self.filter_select = filter_select

    	vbox.addWidget(filter_label, stretch=0)
    	vbox.addWidget(filter_select, stretch=0)
    	vbox.addWidget(search_box)
    	vbox.addWidget(wtable, stretch=0)

    	starred_entries_box = QtGui.QCheckBox("Show starred entries only")
    	self.starred_entries_box = starred_entries_box
    	starred_entries_box.stateChanged.connect(self.starred_entries_only)

    	vbox.addWidget(starred_entries_box)

    	self.fv.ds.add_tab("right", vbox, 1, "SunPyDB", tabname="sunpydb")
    	self.fv.ds.raise_tab("sunpydb")

    def starred_entries_only(self):
      '''
        Logic for showing/unshowing the starred entries only in the database
        table
      '''

    	if self.starred_entries_box.isChecked():
    		q = self.get_starred_entries_id()
    		selected_entries = self.get_entries_from_id(q)
    		self.database_table_repaint(selected_entries)
    	else:
    		self.database_table_repaint(database)

    def query(self):
      '''
        For filtering values in the database table and displaying them
      '''
    	query_mapping = {
    		'id' : 'id',
    		'Observation Time Start' : 'observation_time_start',
    		'Observation Time End' : 'observation_time_end',
    		'Instrument' : 'instrument',
    		'Min Wavelength' : 'wavemin',
    		'Max Wavelength' : 'wavemax',
    		'File' : 'path'
    	}

    	q = self.search_box.text()
    	# print 'Query:', q

    	category = self.filter_select.currentText()
    	# print category
    	col = self.table_headers.index(category)
    	# print col

    	query_results = []

    	for i in database:
    		s = str(getattr(i, query_mapping[category]))
    		# print s
    		try:
    			if s.lower().find(q) != -1:
    				query_results.append(i.id)
    		except:
    			continue
    	# print query_results

    	q = self.get_entries_from_id(query_results)
    	self.database_table_repaint(q)

    def database_table_repaint(self, entries):
      '''
        Repaints of the database table based on the filter entered
      '''
    	self.wtable.clearContents()

    	queries = self.get_data_from_selected_entries(entries)

    	for i, row in enumerate(queries):
    		for j, col in enumerate(row):
    			item = QtGui.QTableWidgetItem(str(col))
    			self.wtable.setItem(i, j, item)

    	self.wtable.itemClicked.connect(self.on_table_row_click)

    def on_table_row_click(self, item):
      '''
        Event handler for opening a new image when a particular row entry if
        clicked
      '''
    	row = item.row()
    	col = item.column()

    	entry_id = int(self.wtable.item(row, 0).data(0))

    	entry = database.get_entry_by_id(entry_id)

    	if col == self.table_headers.index('Starred'):
    		if entry.starred:
    			database.unstar(entry)
    		else:
    			database.star(entry)

    		database.commit()
    		self.view_database()

    	image = AstroImage.AstroImage()
    	image.load_file(entry.path)

    	# TODO: Fit image to entire available space?
    	chaname = entry.path.split('/')[-1]
    	self.fv.add_image(chaname, image, chname=chaname)
    	self.fitsimage = self.fv.get_fitsimage(chaname)

    	#Create a map with only the already opened metadata for speed
    	sunpy_map = sunpy.map.Map((np.zeros([1,1]), image.get_header()))
    	cm = "{0}{1}{2}".format(sunpy_map.observatory.lower(),
    	                      sunpy_map.detector.lower(), sunpy_map.wavelength)
    	try:
    		cm = cmap.get_cmap(cm)
    		rgbmap = self.fitsimage.get_rgbmap()
    		rgbmap.set_cmap(cm)
    	except KeyError:
    		pass

    def get_starred_entries_id (self):
      '''
        Returns a list of id of the starred entries in the database
      '''
    	q = []
    	for entry in database:
    		if entry.starred:
    			q.append(entry.id)

    	return q

    def get_entries_from_id (self, entries_id):
      '''
        Returns a list of database entries based on the passed list of id only
      '''
    	q = []
    	for i in entries_id:
    		q.append(database.get_entry_by_id(i))

    	return q

    def set_default_db(self, conn_string):
      '''
        Sets the current database as default
      '''
      #TODO: To save the config change
      
      url = conn_string
      
      if 'database' not in sunpy.config.sections():
        # print sunpy.config.sections()
        sunpy.config.add_section('database')
      
      sunpy.config.set("database", "url", url)
      print "Set Default DB", sunpy.config.get("database", "url")

    def open_file(self):
      '''
        To select a file by opening a File Dialog Box
      '''
    	res = QtGui.QFileDialog.getOpenFileName()

    	if isinstance(res, tuple):
    		fileName = res[0].encode('ascii')
    	else:
    		fileName = str(res)

    	return fileName

    def add_file(self):
      '''
        Adds database entries from the selected FITS file to database
      '''
    	file_name = self.open_file()

    	print file_name
    	database.add_from_file(file_name)

    	self.set_info("File Added: %s"%file_name)

    def open_sqlite_database(self):
    	'''
    		Connects to a sqlite database by selecting it from a file box
    	'''
    	file_name = self.open_file()
    	db_conn_string = 'sqlite:///' + file_name
    	self.connect_db(db_conn_string)

    def commit_database(self):
    	'''
    		Commits the newly added files to the connected database
    	'''
      database.commit()
      self.set_info("Status: Database Committed")

    def get_channel_info(self, fitsimage):
        chname = self.fv.get_channelName(fitsimage)
        chinfo = self.fv.get_channelInfo(chname)
        return chinfo

    def set_info(self, text):
        self.tw.set_text(text)

    # CALLBACKS

    def add_channel(self, viewer, chinfo):
        """
        Callback from the reference viewer shell when a channel is added.
        """
        self.set_info("Channel '%s' has been added" % (
                chinfo.name))
        # Register for new image callbacks on this channel's canvas
        fitsimage = chinfo.fitsimage
        fitsimage.set_callback('image-set', self.new_image_cb)

    def delete_channel(self, viewer, chinfo):
        """
        Callback from the reference viewer shell when a channel is deleted.
        """
        self.set_info("Channel '%s' has been deleted" % (
                chinfo.name))
        return True

    def focus_cb(self, viewer, fitsimage):
        """
        Callback from the reference viewer shell when the focus changes
        between channels.
        """
        chinfo = self.get_channel_info(fitsimage)
        chname = chinfo.name

        if self.active != chname:
            # focus has shifted to a different channel than our idea
            # of the active one
            self.active = chname
            self.set_info("Focus is now in channel '%s'" % (
                self.active))
        return True

    def new_image_cb(self, fitsimage, image):
        """
        Callback from the reference viewer shell when a new image has
        been added to a channel.
        """
        chinfo = self.get_channel_info(fitsimage)
        chname = chinfo.name

        # Only update our GUI if the activity is in the focused
        # channel
        if self.active == chname:
            imname = image.get('name', 'NONAME')
            self.set_info("A new image '%s' has been added to channel %s" % (
                imname, chname))
        return True

    def start(self):
        """
        This method is called just after ``build_gui()`` when the plugin
        is invoked.  This method could be called more than once if the
        plugin is opened and closed.  This method may be omitted
        in many cases.
        """
        pass

    def stop(self):
        """
        This method is called when the plugin is stopped.
        It should perform any special clean up necessary to terminate
        the operation.  This method could be called more than once if
        the plugin is opened and closed, and may be omitted if there is no
        special cleanup required when stopping.
        """
        pass

    def close(self):
        self.fv.stop_global_plugin(str(self))
        return True

    def __str__(self):
        """
        This method should be provided and should return the lower case
        name of the plugin.
        """
        return 'sunpydatabase'
