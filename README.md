# ideapad-perf
Battery manager to handle system performance modes and charge modes through acpi_calls (for some AMD models of Lenovo IdeaPad). There is also a handy applet for your system tray.

![screenshot](https://github.com/korikori/ideapad-perf/blob/main/screenshot2.png)

## Motivation

Similar to [battmngr](https://github.com/0xless/battmngr), but has been tested and confirmed to work on the following AMD models:
* IdeaPad 5 14ARE05 model 81YM. More information is available at the [ArchWiki](https://wiki.archlinux.org/title/Lenovo_IdeaPad_5_14are05#Power_management).
* IdeaPad 5 Pro 14ACN6 model 82L7. More information is available at the [ArchWiki](https://wiki.archlinux.org/title/Lenovo_IdeaPad_5_Pro_14ACN6#Power_management_options).

I have now built a separate branch that only includes the battery-related modes (Rapid Charge and Battery Conservation), as they should be more cross-compatible and may potentially work across Lenovo models with recent Intel CPUs too (testers welcome). An Arch package for this branch is available as a release [here](https://github.com/korikori/ideapad-perf/releases/tag/r26.2f450da).

Note that the experimental branch of `battmngr` should also work on these devices.

## Requirements

The original script requires the `acpi_call` module loaded for your kernel. In order to install and use the applet, you would also need `ruby` and `ruby-gtk3`. If you are using Wayland, please see the [relevant note](https://github.com/korikori/ideapad-perf#note-on-the-system-tray-applet-and-wayland) below.

## Installation

You can download the script, make it executable, and add it to your path. You can run it with `sudo`, or you can install the supplied udev rule to make /proc/acpi/call writeable to all members of the `wheel` group.

There is a pre-built package for Arch Linux available as a [release](https://github.com/korikori/ideapad-perf/releases/), including PKGBUILD and .install files if you want to build it yourself. If you don't need the systray applet for whatever reason, use the older release.

The applet icon used in the screenshot is `preferences-system-power.svg`, part of [Flatery Dark](https://github.com/cbrnix/Flatery).

## Usage

```
Syntax: ideapad-perf [OPTION] MODE

Options:
 -h, --help                   see this help message
 -p, --performance-mode       set performance mode
 -b, --battery-mode           set battery mode
 -c, --check                  verify both performance and battery mode
 -vp, --verify-performance    verify performance mode
 -vb, --verify-battery        verify battery mode

Valid performance modes:
 ic, cooling            Intelligent Cooling
 ep, performance        Extreme Performance
 bs, battery            Battery Saving

Valid battery modes:
 rc, rapid              Enable Rapid Charge (with Battery Conservation disabled)
 bc, conserve           Enable Battery Conservation (with Rapid Charge disabled)
 off                    Disable both Rapid Charge and Battery Conservation
```

## Note on Rapid Charge and Battery Conservation mode

As noted elsewhere, it is possible to activate both Rapid Charge and Battery Conservation on Linux. However, as this configuration is not obtainable using official Lenovo software on Windows and it would defeat the purpose of the Battery Conservation, I have chosen to explicitly prevent this - choosing one of the options will disable the other one first. If for any reason you need to achieve this effect, you can do so manually via the commands provided in the ArchWiki.

## Note on the system tray applet and Wayland

Wayland and most modern GUI toolkits do not like system tray applets. There are libraries that provide similar functionality, but the Ruby bindings for them are non-existent or outdated and difficult to build. For now, there is a simple workaround - pass `GDK_BACKEND=x11` before starting the `ideapad-perf-tray.rb` script, like so:

```
 GDK_BACKEND=x11 ideapad-perf-tray.rb
 ```
 
See [this issue](https://github.com/korikori/ideapad-perf/issues/1) for more information, as well as specific instructions on auto-starting the applet on KDE, courtesy of [@Suspycat](https://github.com/Suspycat).

## License

This project is licensed under the GPL-3.0 License.
