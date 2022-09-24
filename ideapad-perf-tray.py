#!/usr/bin/python

import signal
import subprocess

import gi

gi.require_version("Gtk", "3.0")
gi.require_version("AppIndicator3", "0.1")
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Gtk as gtk


class Indicator:
    def __init__(self):
        self.vbc()
        self.indicator = appindicator.Indicator.new(
            "customtray",
            "preferences-system-power",
            appindicator.IndicatorCategory.APPLICATION_STATUS,
        )
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.menu())

    def vbc(self):
        f = subprocess.check_output("ideapad-perf -vb".split()).decode("utf-8").strip()
        match f:
            case "Rapid Charge mode is on, Battery Conservation mode is off.":
                self.battery_profile = "rc"
            case "Rapid Charge mode is off, Battery Conservation mode is on.":
                self.battery_profile = "bc"
            case "Rapid Charge mode is off, Battery Conservation mode is off.":
                self.battery_profile = "off"

    def menu(self):
        menu = gtk.Menu()

        title = gtk.MenuItem(label="Battery mode")
        title.set_sensitive(False)
        menu.append(title)

        mode_1 = gtk.RadioMenuItem(label="Rapid Charge")
        menu.append(mode_1)
        if self.battery_profile == "rc":
            mode_1.set_active(True)
        mode_1.connect("activate", self.change_mode, "rc")

        mode_2 = gtk.RadioMenuItem(label="Battery Conservation", group=mode_1)
        if self.battery_profile == "bc":
            mode_2.set_active(True)
        menu.append(mode_2)
        mode_2.connect("activate", self.change_mode, "bc")

        mode_3 = gtk.RadioMenuItem(label="Off", group=mode_1)
        menu.append(mode_3)
        if self.battery_profile == "off":
            mode_3.set_active(True)
        mode_3.connect("activate", self.change_mode, "off")

        menu.append(gtk.SeparatorMenuItem())

        quit = gtk.MenuItem(label="Quit")
        menu.append(quit)
        quit.connect("activate", self.quit, "quit")

        menu.show_all()
        return menu

    def change_mode(self, source, string):
        subprocess.call(
            f"ideapad-perf -b {string}".split(),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    def quit(*args):
        gtk.main_quit(*args)


Indicator()
signal.signal(signal.SIGINT, signal.SIG_DFL)
gtk.main()
