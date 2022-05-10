#!/usr/bin/ruby
require 'gtk3'

si=Gtk::StatusIcon.new
si.set_from_icon_name("gnome-power-manager")

#check active modes and set active menu option based on that

def vbc
  vbcheck = `ideapad-perf -vb`
  if vbcheck == "Rapid Charge mode is on, Battery Conservation mode is off.".chomp
    $vb = "rc"
  elsif vbcheck == "Rapid Charge mode is off, Battery Conservation mode is on.".chomp
    $vb = "bc"
  elsif vbcheck == "Rapid Charge mode is off, Battery Conservation mode is off.".chomp
    $vb = "off"
  end
end

#setting the performance and battery modes
def setbmode(x)
  `ideapad-perf -b #{x}`
end

#check initial states
vbc

#menu
menu=Gtk::Menu.new

group = nil

label2=Gtk::MenuItem.new(label: "Battery mode")
label2.set_sensitive(false)
menu.append(label2)

group2 = nil

item4=Gtk::RadioMenuItem.new(group2, "Rapid Charge")
menu.append(item4)
item4.active = true if $vb == "rc"
item4.signal_connect("activate") { 
  if item4.active? == true
    setbmode("rc")
  end
}

item5=Gtk::RadioMenuItem.new(item4, "Battery Conservation")
menu.append(item5)
item5.active = true if $vb == "bc"
item5.signal_connect("activate") { 
  if item5.active? == true
    setbmode("bc")
  end
}
 
item6=Gtk::RadioMenuItem.new(item4, "Off")
menu.append(item6)
item6.active = true if $vb == "off"
item6.signal_connect("activate") { 
  if item6.active? == true
    setbmode("off")
  end
}

menu.append(Gtk::SeparatorMenuItem.new)

quit=Gtk::MenuItem.new(label: 'Quit')
quit.signal_connect('activate'){Gtk.main_quit}
menu.append(quit)
quit.show
menu.show_all


##Show menu on right click
si.signal_connect('popup-menu'){|tray, button, time| menu.popup(nil, nil, button, time)}

Gtk.main
