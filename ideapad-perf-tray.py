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
        self.vp = None
        self.battery_profile = None
        self.vpc()
        self.vbc()
        self.indicator = appindicator.Indicator.new(
            "customtray",
            "preferences-system-power",
            appindicator.IndicatorCategory.APPLICATION_STATUS,
        )
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.menu())

    def vpc(self):
        vpcheck = (
            subprocess.check_output("ideapad-perf -vp".split()).decode("utf-8").strip()
        )
        match vpcheck:
            case "Running in Extreme Performance mode.":
                self.vp = "ep"
            case "Running in Battery Saving mode.":
                self.vp = "bs"
            case "Running in Intelligent Cooling mode.":
                self.vp = "ic"

    def vbc(self):
        vbcheck = (
            subprocess.check_output("ideapad-perf -vb".split()).decode("utf-8").strip()
        )
        match vbcheck:
            case "Rapid Charge mode is on, Battery Conservation mode is off.":
                self.battery_profile = "rc"
            case "Rapid Charge mode is off, Battery Conservation mode is on.":
                self.battery_profile = "bc"
            case "Rapid Charge mode is off, Battery Conservation mode is off.":
                self.battery_profile = "off"

    def menu(self):
        menu = gtk.Menu()

        title_performance = gtk.MenuItem(label="Performance mode")
        title_performance.set_sensitive(False)
        menu.append(title_performance)

        mode_1 = gtk.RadioMenuItem(label="Extreme Performance")
        menu.append(mode_1)
        if self.vp == "ep":
            mode_1.set_active(True)
        mode_1.connect("activate", self.change_performance_mode, "ep")

        mode_2 = gtk.RadioMenuItem(label="Battery Saving", group=mode_1)
        menu.append(mode_2)
        if self.vp == "bs":
            mode_2.set_active(True)
        mode_2.connect("activate", self.change_performance_mode, "bs")

        mode_3 = gtk.RadioMenuItem(label="Intelligent Cooling", group=mode_1)
        menu.append(mode_3)
        if self.vp == "ic":
            mode_3.set_active(True)
        mode_3.connect("activate", self.change_performance_mode, "ic")

        menu.append(gtk.SeparatorMenuItem())

        title_battery = gtk.MenuItem(label="Battery mode")
        title_battery.set_sensitive(False)
        menu.append(title_battery)

        mode_4 = gtk.RadioMenuItem(label="Rapid charge")
        menu.append(mode_4)
        if self.battery_profile == "rc":
            mode_4.set_active(True)
        mode_4.connect("activate", self.change_battery_mode, "rc")

        mode_5 = gtk.RadioMenuItem(label="Battery conservation", group=mode_4)
        if self.battery_profile == "bc":
            mode_5.set_active(True)
        menu.append(mode_5)
        mode_5.connect("activate", self.change_battery_mode, "bc")

        mode_6 = gtk.RadioMenuItem(label="Off", group=mode_4)
        menu.append(mode_6)
        if self.battery_profile == "off":
            mode_6.set_active(True)
        mode_6.connect("activate", self.change_battery_mode, "off")

        menu.append(gtk.SeparatorMenuItem())

        quit = gtk.MenuItem(label="Quit")
        menu.append(quit)
        quit.connect("activate", self.quit, "quit")

        menu.show_all()
        return menu

    def change_performance_mode(self, source, string):
        subprocess.call(
            f"ideapad-perf -p {string}".split(),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    def change_battery_mode(self, source, string):
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
