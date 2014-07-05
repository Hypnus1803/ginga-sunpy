"""
Author : Rajul

To enable it, run ginga with the command
    $ ginga --plugins=SunPyDatabase

it will then be available from the "Operations" button.

"""

# importing the Ginga modules required by a Ginga Plugin 
from ginga import GingaPlugin
from ginga.misc import Widgets
from ginga.qtw.ImageViewQt import ImageViewZoom
from ginga import AstroImage
from ginga.qtw.QtHelp import QtGui, QtCore

# importing the other modules
import sys, os

# importing the SunPy databse module
from sunpy.database import Database
import sunpy.database
import sunpy

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
      return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
      return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
      return QtGui.QApplication.translate(context, text, disambig)

class sunpy_plugin(GingaPlugin.LocalPlugin):

    def __init__(self, fv, fitsimage):
        """
        This method is called when the plugin is loaded for the  first
        time.  ``fv`` is a reference to the Ginga (reference viewer) shell
        and ``fitsimage`` is a reference to the specific ImageViewCanvas
        object associated with the channel on which the plugin is being
        invoked.
        You need to call the superclass initializer and then do any local
        initialization.
        """
        super(sunpy_plugin, self).__init__(fv, fitsimage)

        # your local state and initialization code goes here

    def build_gui(self, container):
        """
        This method is called when the plugin is invoked.  It builds the
        GUI used by the plugin into the widget layout passed as
        ``container``.
        This method may be called many times as the plugin is opened and
        closed for modal operations.  The method may be omitted if there
        is no GUI for the plugin.

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

        self.msgFont = self.fv.getFont("sansFont", 12)
        tw = Widgets.TextArea(wrap=True, editable=False)
        tw.set_font(self.msgFont)
        self.tw = tw


        db_driver = Widgets.TextArea(wrap=True, editable=True)
        self.db_driver = db_driver

        db_name = Widgets.TextArea(wrap=True, editable=True)
        self.db_name = db_name
                                                  
        db_user = Widgets.TextArea(wrap=True, editable=True)
        self.db_user = db_user
        
        db_pass = Widgets.TextArea(wrap=True, editable=True)
        self.db_pass = db_pass
                                                                          
        db_driver_label = Widgets.Label(text="Driver Name")
        self.db_driver_label = db_driver_label
        
        db_name_label = Widgets.Label(text="Database Name")
        self.db_name_label = db_name_label
        
        db_user_label = Widgets.Label(text="User Name")
        self.db_user_label = db_user_label
        
        db_pass_label = Widgets.Label(text="Password")
        self.db_pass_label = db_pass_label
        
        connect_button = Widgets.Button(text="Connect")
        self.connect_button = connect_button
        connect_button.add_callback('activated', lambda w: self.connectDB())

        populate_button = Widgets.Button(text="Populate Database")
        self.populate_button = populate_button
        populate_button.add_callback('activated', lambda w: self.add_file_to_db())

        status_label = Widgets.Label(text="Status:")
        self.status_label = status_label
        
        view_button = Widgets.Button(text="View Database")
        self.view_button = view_button
        view_button.add_callback('activated', lambda w: self.view_database())
        
        add_button = Widgets.Button(text="Add file to Database")
        self.add_button = add_button
        add_button.add_callback('activated', lambda w: self.add_file())

        open_button = Widgets.Button(text="Open Database")
        self.open_button = open_button
        open_button.add_callback('activated', lambda w: self.open_sqlite_database())
        
        # Frame for instructions and add the text widget with another
        # blank widget to stretch as needed to fill emp
        fr = Widgets.Frame("Instructions")
        vbox2 = Widgets.VBox()
        vbox2.add_widget(tw)

        vbox2.add_widget(db_driver_label)
        vbox2.add_widget(db_driver)
        vbox2.add_widget(db_name_label)
        vbox2.add_widget(db_name)
        vbox2.add_widget(db_user_label)
        vbox2.add_widget(db_user)
        vbox2.add_widget(db_pass_label)
        vbox2.add_widget(db_pass)
        vbox2.add_widget(connect_button)
        vbox2.add_widget(populate_button)
        vbox2.add_widget(view_button)
        vbox2.add_widget(add_button)
        vbox2.add_widget(open_button)
        vbox2.add_widget(status_label)
	
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

    def close(self):
        """
        Example close method.  You can use this method and attach it as a
        callback to a button that you place in your GUI to close the plugin
        as a convenience to the user.
        """
        chname = self.fv.get_channelName(self.fitsimage)
        self.fv.stop_local_plugin(chname, str(self))
        return True
        
    def start(self):
        """
        This method is called just after ``build_gui()`` when the plugin
        is invoked.  This method may be called many times as the plugin is
        opened and closed for modal operations.  This method may be omitted
        in many cases.
        """
        self.tw.set_text("""This plugin is used for browsing and viewing SunPy database entries""")
        self.resume()

    def connectDB(self):
      try:
        connection_string = sunpy.config.get('database', 'url')
        global database 
        database = Database(connection_string)
      except:
        connection_string = self.get_connection_string()
        global database 
        database = Database(connection_string)
      
      # self.status_label.set_text("Status: Database Connected!!")
    
    def get_connection_string(self):
      connect_string = ''
      
      db_driver = self.db_driver.get_widget().toPlainText()
      db_name = self.db_name.get_widget().toPlainText()
      db_user = self.db_user.get_widget().toPlainText()
      db_pass = self.db_pass.get_widget().toPlainText()

      if db_driver == '':
        db_driver = 'sqlite'

      if db_name == '':
        db_name = 'sunpydb'

      if db_user != '' and db_pass != '':
        user_string = db_user + ':' + db_pass
      else:
        user_string = ''
      
      connect_string = db_driver + '://' + user_string+ '/' + db_name 
      
      self.status_label.set_text(connect_string)

      return connect_string

    def add_file_to_db(self):
      database.add_from_file('/home/rajul/Documents/FITSFiles/WFPC2u5780205r_c0fx.fits')
      database.add_from_file('/home/rajul/Documents/FITSFiles/WFPC2ASSNu5780205bx.fits')
      database.add_from_file('/home/rajul/Documents/FITSFiles/NICMOSn4hk12010_mos.fits')	        
      self.status_label.set_text(_fromUtf8("Status: Database Populated!!"))

    def database_view(self):
      self.view = Database_View()
      self.view.show()
      self.view.raise_()
      self.view.activateWindow()

    def view_database(self):
      wtable = QtGui.QTableWidget(len(database), 6)

      queries = []

      table_headers = ['id', 'Observation Time Start', 'Observation Time End', 'Instrument', 'Min Wavelength', 'Max Wavelength']
  
      for i in database:
        q = []

        q.append(i.id)
        q.append(i.observation_time_start)
        q.append(i.observation_time_end)
        q.append(i.instrument)
        q.append(i.wavemin)
        q.append(i.wavemax)

        queries.append(q)

      for i, row in enumerate(queries):
        for j, col in enumerate(row):
          item = QtGui.QTableWidgetItem(str(col))
          wtable.setItem(i, j, item)
          # wtable.add_callback('activated', lambda w: self.table_click())
      
      wtable.itemClicked.connect(self.table_click)

      wtable.setHorizontalHeaderLabels(table_headers)

      wtable.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
      # print dir(wtable)
      
      print q

      self.wtable = wtable

      # self.fv.ds.add_tab("channels", wtable, 1, "SunPyDB", tabname="sunpydb")
      
      # TODO: Fix the multiple tab opening on each update issue 
      self.fv.ds.add_tab("right", wtable, 1, "SunPyDB", tabname="sunpydb")
      self.fv.ds.raise_tab("sunpydb")

      # for w in (wtable,):
        # self.fv.ds.add_tab("channels", w, 1, "SunPyDB", tabname="sunpydb")
        # hbox.addWidget(w)
    
    def table_click(self, item):
      row = item.row()
      entry_id = int(self.wtable.item(row, 0).data(0))
      # print row
      # print "Id:", self.wtable.item(row, 0).data(0)
      # print dir(self.wtable.item(row, 0))
      entry = database.get_entry_by_id(entry_id)
      print entry.path
      
      fitsimage = ImageViewZoom(self.logger, render='widget')
      fitsimage.enable_autocuts('on')
      fitsimage.set_autocut_params('zscale')
      fitsimage.enable_autozoom('on')
      # fitsimage.set_callback('drag-drop', self.drop_file)
      fitsimage.set_bg(0.2, 0.2, 0.2)
      fitsimage.ui_setActive(True)
          
      bd = fitsimage.get_bindings()
      bd.enable_pan(True)
      bd.enable_zoom(True)
      bd.enable_cuts(True)
      bd.enable_flip(True)


      image = AstroImage.AstroImage()
      image.load_file(entry.path)
      
      fitsimage.set_image(image)
      self.fitsimage = fitsimage
      
      w = fitsimage.get_widget()
      # print dir(w)
      # w.resize(512, 512)
      
      # TODO: Fix multiple image tab open for same image issue
      # TODO: Fit image to entire available space
      self.fv.ds.add_tab("channels", w, 1, entry.path.split('/')[-1], tabname="image")
      self.fv.ds.raise_tab("image")
 
    def open_file(self):
      print 'In open file'
      res = QtGui.QFileDialog.getOpenFileName()
      # res = QtGui.QFileDialog.getOpenFileName(self, "Open FITS file", ".", "FITS files (*.fits)")
      
      print 'In open file 2'
      if isinstance(res, tuple):
        fileName = res[0].encode('ascii')
      else:
        fileName = str(res)
    
      return fileName
    
    def add_file(self):
      print 'In add from file'
      file_name = self.open_file()
      
      print file_name
      database.add_from_file(file_name)
      
      print 'file added'

    # TODO: Implement global functioning of this function
    def open_sqlite_database(self):
      print 'In open_sqlite_database()'
      file_name = self.open_file()
      db_string = 'sqlite:///' + file_name
      global sqlite_db
      sqlite_db = Database(db_string)

    
    # Methods which are not required till now
    def pause(self):
        """
        This method is called when the plugin loses focus.
        It should take any actions necessary to stop handling user
        interaction events that were initiated in ``start()`` or
        ``resume()``.
        This method may be called many times as the plugin is focused
        or defocused.  It may be omitted if there is no user event handling
        to disable.
        """
        pass

    def resume(self):
        """
        This method is called when the plugin gets focus. 
        It should take any actions necessary to start handling user
        interaction events for the operations that it does.
        This method may be called many times as the plugin is focused or
        defocused.  The method may be omitted if there is no user event
        handling to enable. 
        """
        pass
        
    def stop(self):
        """
        This method is called when the plugin is stopped. 
        It should perform any special clean up necessary to terminate
        the operation.  The GUI will be destroyed by the plugin manager
        so there is no need for the stop method to do that.
        This method may be called many  times as the plugin is opened and
        closed for modal operations, and may be omitted if there is no
        special cleanup required when stopping.
        """
        pass
        
    def redo(self):
        """
        This method is called when the plugin is active and a new
        image is loaded into the associated channel.  It can optionally
        redo the current operation on the new image.  This method may be
        called many times as new images are loaded while the plugin is
        active.  This method may be omitted.
        """
        pass
    
    def __str__(self):
        """
        This method should be provided and should return the lower case
        name of the plugin.
        """
        return 'SunPy Database Plugin'
