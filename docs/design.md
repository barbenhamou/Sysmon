# Sysmon - Design Document

This project goal is to display in real time, the usage of hardware components in the system.

## Architecture Overview:
main.py - Entry point and CLI parser. Initializer of the subsystems.

### Subsytems:
 Collector - Live data gathering through system APIs.

 Logger - Appending incoming data from the 'Collector' to the log file, at shutdown appends current data. JSON format.
 
 Display - Live rendered data, that was collected from the 'Collector'.

