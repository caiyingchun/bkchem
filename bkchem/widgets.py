#--------------------------------------------------------------------------
#     This file is part of BKchem - a chemical drawing program
#     Copyright (C) 2002, 2003 Beda Kosata <beda@zirael.org>

#     This program is free software; you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation; either version 2 of the License, or
#     (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.

#     Complete text of GNU GPL can be found in the file gpl.txt in the
#     main directory of the program

#--------------------------------------------------------------------------
#
#
#
#--------------------------------------------------------------------------

"""set of specialized widgets, such as color-selection-buttons etc."""

from __future__ import division

import Tkinter
import tkColorChooser
import tkFont
import math
import geometry
import Pmw
import data
import re
import misc

class ColorButton( Tkinter.Button):
  """button used for color selection; has the choosen color in background and
  when pressed opens tkColorChooser.askcolor dialog"""

  def __init__( self, master=None, color=None, text=''):
    """well, init..."""
    self.master = master
    self.set_color( color)
    Tkinter.Button.__init__( self, master=master, command=self._select_color,
                             background=self.color, activebackground=self.color,
                             foreground=self.foreground_color, activeforeground=self.foreground_color,
                             text=text)

  def set_color( self, color):
    """sets the self.color and modifies self.foreground_color if needed for the text to be visible"""
    if color:
      self.color = str( color)
    else:
      self.color = None
    if not self.color:
      self.foreground_color = "#000"
      return
    elif type( color) != type(()):
      c = self.master.winfo_rgb( self.color)
    else:
      c = color
    if (c[0] + c[1] + c[2] > 128*256):
      self.foreground_color = "#000"
    else:
      self.foreground_color = "#fff"

  def _select_color( self):
    if self.color:
      color = tkColorChooser.askcolor( self.color)
    else:
      color = tkColorChooser.askcolor()
    if color[1]:
      self.set_color( color[1])
      self.rgb = color[0]
      self.configure( background=self.color, activebackground=self.color,
                      activeforeground=self.foreground_color, foreground=self.foreground_color)
      


class GraphicalAngleChooser( Tkinter.Frame):

  def __init__( self, parent, angle, line_color="#000", fill_color="#ffffff"):

    Tkinter.Frame.__init__( self, parent)
    self.canvas = Tkinter.Canvas( self, width=60, height=60)
    self.canvas.bind('<Button-1>', self._click)
    self.canvas.bind('<B1-Motion>', self._click)
    self.canvas.pack()

    self.counter = Pmw.Counter( self,
                                entryfield_value = angle,
                                entryfield_validate={ 'validator':'integer', 'min':0, 'max':360},
                                entry_width = 5,
                                entryfield_modifiedcommand = self._counter_changed,
                                increment = 10,
                                datatype = 'integer')
    self.counter.pack()

    self.angle = angle
    self._draw()

  def _draw( self):
    self._line = self.canvas.create_line( 30, 30, 30+20*math.cos( self.angle*math.pi/180), 30+20*math.sin( self.angle*math.pi/180))

  def _redraw( self):
    self.canvas.coords( self._line, 30, 30, 30+20*math.cos( self.angle*math.pi/180), 30+20*math.sin( self.angle*math.pi/180))

  def _counter_changed( self):
    try:
      self.angle = round( float( self.counter.get()))
    except ValueError:
      self.angle = 0
    self._redraw()

  def _click( self, e):
    x = e.x
    y = e.y
    self.angle = int( round( 180*geometry.clockwise_angle_from_east( x - 30, y - 30) / math.pi))
    self.counter.setentry( self.angle)

  def get( self):
    return self.angle




class FontSizeChooser( Pmw.Counter):

  def __init__( self, parent, value):
    Pmw.Counter.__init__( self,
                          parent,
                          labelpos = 'nw',
                          label_text = _('Font size'),
                          entryfield_value = value,
                          entryfield_validate={ 'validator': font_size_validator},
                          entry_width = 3,
                          increment = 1,
                          datatype = {'counter': font_size_counter})



class FontFamilyChooser( Pmw.ScrolledListBox):

  def __init__( self, parent, value):
      available_families = list( tkFont.families())
      available_families.sort()
      available_families.insert(-1, '')
      for fnt in data.always_available_fonts:
        available_families.insert(1, fnt)
      if not value in available_families:
        v = ''
      else:
        v = value
      Pmw.ScrolledListBox.__init__( self,
                                    parent,
                                    labelpos = 'nw',
                                    label_text = _('Font family'),
                                    listbox_selectmode = 'single',
                                    items = available_families,
                                    hull_relief = 'ridge')
      self.select_set( available_families.index( v))
      self.see( available_families.index( v))



class WidthCounter( Pmw.Counter):
  """the counter widget used to implement WidthChooser"""
  
  def __init__( self, parent, value, label=None):
    l = label or _('Width')
    Pmw.Counter.__init__( self,
                          parent,
                          labelpos = 'w',
                          label_text = l,
                          entryfield_value = value,
                          entryfield_validate={ 'validator':'real', 'min':0, 'max':100},
                          entry_width = 5,
                          increment = 1,
                          datatype = 'real')

class LengthCounter( Pmw.Counter):
  """the counter widget used to implement LengthChooser"""
  
  def __init__( self, parent, value, label=None):
    l = label or _('Length')
    Pmw.Counter.__init__( self,
                          parent,
                          labelpos = 'w',
                          label_text = l,
                          entryfield_value = value,
                          entryfield_validate={ 'validator':'real', 'min':0, 'max':1000},
                          entry_width = 5,
                          increment = 1,
                          datatype = 'real')

class RatioCounter( Pmw.Counter):
  """Counter used to input ratio information"""
  
  def __init__( self, parent, value, label=None):
    l = label or _('Ratio')
    Pmw.Counter.__init__( self,
                          parent,
                          labelpos = 'w',
                          label_text = l,
                          entryfield_value = value,
                          entryfield_validate={ 'validator':'real', 'min':0, 'max':1},
                          entry_width = 4,
                          increment = 0.05,
                          datatype = 'real')



class ValueWithUnitParent( Tkinter.Frame):

  def __init__( self, parent, value, counter, label=None, units={}):
    """the parent is standard widget parent, counter should be Pmw.Counter instance,
    units is a dictionary of dictionaries keyed by unit name with ratio, round and increment"""
    Tkinter.Frame.__init__( self, parent)
    self.units = units
    v, self._recent_unit = misc.split_number_and_unit( value)
    # the counter widget
    if not v:
      v = ''
    self.counter = counter( self, v, label=label)
    if self._recent_unit:
      self.counter['increment'] = self.units[self._recent_unit]['increment']
    else:
      self._recent_unit = units.keys()[0]
    self.counter.pack( side='left')
    # the unit selection widget
    us = units.keys()
    us.sort()
    self.unit = Pmw.OptionMenu( self, items=us, initialitem=self._recent_unit, command=self.unit_changed)
    self.unit.pack( side='left')

  def unit_changed( self, current):
    if self._recent_unit != current:
      unit = self.units[ current]
      ratio = unit['ratio'] / self.units[ self._recent_unit]['ratio']
      try:
        value = float( self.counter.getvalue())
      except ValueError:
        value = 0
      self.counter.setentry( str( round( value*ratio, unit[ 'round'])))
      self.counter['increment'] = unit['increment']
      #self.counter.cget('entryfield')._validationInfo['min'] *= ratio
      #self.counter['entryfield']._validationInfo['max'] *= ratio
      self._recent_unit = current


  def getvalue( self):
    return '%s%s' % (self.counter.getvalue(), self.unit.getvalue())
    

class WidthChooser( ValueWithUnitParent):

  def __init__( self, parent, value, label=None):
    ValueWithUnitParent.__init__( self, parent, value, WidthCounter, label=label,
                                  units={'cm':{'ratio':1, 'increment': 0.02, 'round': 2},
                                         'px':{'ratio':30,  'increment': 1   , 'round': 0}})


class LengthChooser( ValueWithUnitParent):

  def __init__( self, parent, value, label=None):
    ValueWithUnitParent.__init__( self, parent, value, LengthCounter, label=label,
                                  units={'cm':{'ratio':1, 'increment': 0.2, 'round': 2},
                                         'px':{'ratio':30,  'increment': 10   , 'round': 0}})



## -------------------- SUPPORT FUNCTIONS --------------------

def font_size_counter( text, factor, increment):
  if text == '':
    return 12
  i = int( text)
  i += factor * increment
  return i


def font_size_validator( input):
  if input == '':
    return Pmw.OK
  if len( input) > 3:
    return Pmw.ERROR
  if re.match( "^\d+$", input):
    i = int( input)
    if i >= 1 and i <= 64:
      return Pmw.OK
    else:
      return Pmw.PARTIAL
  return Pmw.ERROR





    
