#!/usr/bin/env python

import re
import sys
import subprocess
import telnetlib

if len(sys.argv) == 2 and sys.argv[1] == "config":
	print """
graph_title ADSL modem statistics
graph_category network
downstream_bw.label Down kbps
downstream_bw.label GAUGE
upstream_bw.label Up kbps
upstream_bw.type GAUGE
resets.label Resets
resets.type GAUGE
inp_dn.label INP down
inp_dn.type GAUGE
inp_up.label INP up
inp_up.type GAUGE
delay_dn.label Delay down (ms)
delay_dn.type GAUGE
delay_up.label Delay up (ms)
delay_up.type GAUGE
margin_dn.label Margin down (dB)
margin_dn.type GAUGE
margin_up.label Margin up (dB)
margin_up.type GAUGE
attenuation_dn.label Attenuation down (dB)
attenuation_dn.type GAUGE
attenuation_up.label Attenuation up (dB)
attenuation_up.type GAUGE
power_dn.label Power down (dB)
power_dn.type GAUGE
power_up.label Power up (dB)
power_up.type GAUGE
rcvd_fec.label Received FEC
rcvd_fec.type DERIVE
rcvd_fec.min 0
rcvd_crc.label Received CRC
rcvd_crc.type DERIVE
rcvd_crc.min 0
rcvd_hec.label Received HEC
rcvd_hec.type DERIVE
rcvd_hec.min 0
xmit_fec.label Transmit FEC
xmit_fec.type DERIVE
xmit_fec.min 0
xmit_crc.label Transmit CRC
xmit_crc.type DERIVE
xmit_crc.min 0
xmit_hec.label Transmit HEC
xmit_hec.type DERIVE
xmit_hec.min 0
frame_err.label Loss of frame
frame_err.type DERIVE
frame_err.min 0
signal_err.label Loss of signal
signal_err.type DERIVE
signal_err.min 0
power_err.label Loss of power
power_err.type DERIVE
power_err.min 0
err_time.label Error time (secs)
err_time.type DERIVE
err_time.min 0"""
	sys.exit(0)
	
net = telnetlib.Telnet("192.168.1.254")
net.read_until("Username :")
net.write("Administrator\r\n")
net.read_until("Password :")
net.write("\r\n")
net.read_until("{Administrator}=>")
net.write("adsl info expand=enabled\r\n")
info = net.read_until("{Administrator}=>")
net.write("exit\r\n")
net.close()

for line in info.split("\n"):
	m = re.search('Downstream *: +(\d+) +(\d+)', line)
	if m: print "downstream_bw.value = %s" % m.group(2) 

	m = re.search('Upstream *: +(\d+) +(\d+)', line)
	if m: print "upstream_bw.value = %s" % m.group(2)

	m = re.search('Number of resets *: +(\d+)', line)
	if m: print "resets.value = %s" % m.group(1)

	m = re.search('Uptime.*: +(\d+) days, (\d+):(\d+):(\d+)', line)
	if m:
		print "uptime.value = %s" % (int(m.group(1)) * 86400 + 
			int(m.group(2)) * 3600 + int(m.group(3)) * 60 + 
			int(m.group(4)))

	m = re.search('INP +(DMT) +: ([0-9.]+) +([0-9.]+)', line)
	if m: print "inp_dn.value = %s" % m.group(1)
	if m: print "inp_up.value = %s" % m.group(2)

	m = re.search('Delay +(ms) +: ([0-9.]+) +([0-9.]+)', line)
	if m: print "delay_dn.value = %s" % m.group(1)
	if m: print "delay_up.value = %s" % m.group(2)

	m = re.search('Margin +(dB) +: ([0-9.]+) +([0-9.]+)', line)
	if m: print "margin_dn.value = %s" % m.group(1)
	if m: print "margin_up.value = %s" % m.group(2)

	m = re.search('Attenuation +(dB) +: ([0-9.]+) +([0-9.]+)', line)
	if m: print "attenuation_dn.value = %s" % m.group(1)
	if m: print "attenuation_up.value = %s" % m.group(2)

	m = re.search('OutputPower +(dB) +: ([0-9.]+) +([0-9.]+)', line)
	if m: print "power_dn.value = %s" % m.group(1)
	if m: print "power_up.value = %s" % m.group(2)

	m = re.search('Received FEC *: +(\d+)', line)
	if m: print "rcvd_fec.value = %s" % m.group(1)

	m = re.search('Received CRC *: +(\d+)', line)
	if m: print "rcvd_crc.value = %s" % m.group(1)

	m = re.search('Received HEC *: +(\d+)', line)
	if m: print "rcvd_hec.value = %s" % m.group(1)

	m = re.search('Transmitted FEC *: +(\d+)', line)
	if m: print "xmit_fec.value = %s" % m.group(1)

	m = re.search('Transmitted CRC *: +(\d+)', line)
	if m: print "xmit_crc.value = %s" % m.group(1)

	m = re.search('Transmitted HEC *: +(\d+)', line)
	if m: print "xmit_hec.value = %s" % m.group(1)

	m = re.search('Loss of frame *: +(\d+)', line)
	if m: print "frame_err.value = %s" % m.group(1)

	m = re.search('Loss of signal *: +(\d+)', line)
	if m: print "signal_err.value = %s" % m.group(1)

	m = re.search('Loss of power *: +(\d+)', line)
	if m: print "power_err.value = %s" % m.group(1)

	m = re.search('Errored seconds *: +(\d+)', line)
	if m: print "err_time.value = %s" % m.group(1)

