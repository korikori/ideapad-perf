# ideapad-perf
Battery manager to handle system performance modes and charge modes through acpi_calls (for IdeaPad 5 14are05). There is also a handy applet for your system tray.

![screenshot](https://github.com/korikori/ideapad-perf/blob/main/screenshot.png)

## Motivation

Similar to [battmngr](https://github.com/0xless/battmngr), but for the IdeaPad 5 14are05. More information is available at the [ArchWiki](https://wiki.archlinux.org/title/Lenovo_IdeaPad_5_14are05).

## Requirements

The original script requires the `acpi_call` module loaded for your kernel. In order to install and use the applet, you would also need `ruby` and `ruby-gtk3`.

## Installation

You can download the script, make it executable, and add it to your path. You can run it with `sudo`, or you can install the supplied udev rule to make /proc/acpi/call writeable to all members of the `wheel` group.

There is a pre-built package for Arch Linux available as a [release](https://github.com/korikori/ideapad-perf/releases/), including PKGBUILD and .install files if you want to build it yourself. If you don't need the systray applet for whatever reason, use the older release. 

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

## License

This project is licensed under the GPL-3.0 License.
