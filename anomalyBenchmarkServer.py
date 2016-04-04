#!/usr/bin/env python
# Cache Agent in Agent based management and control system
# Chen Wang, chenw@cmu.edu
#!/bin/env python
import sys
import os
import subprocess as sub
import urlparse
import time

try:
    # Python 2.x
    from SocketServer import ThreadingMixIn
    from SimpleHTTPServer import SimpleHTTPRequestHandler
    from BaseHTTPServer import HTTPServer
except ImportError:
    # Python 3.x
    from socketserver import ThreadingMixIn
    from http.server import SimpleHTTPRequestHandler, HTTPServer

class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
	pass

class RequestHandler(SimpleHTTPRequestHandler):
	def do_GET(self):
		script_folder = os.path.dirname(os.path.realpath(__file__))
		try:
			if "ico" in self.command:
				return
			elif self.path.startswith('/cpu'):
				# default: just send the file
				url = self.path
				params = url.split('?')[1]
				print params
				cpu_stress_params = urlparse.parse_qs(params)
				print cpu_stress_params
				cpu_stress_workers = cpu_stress_params['N'][0]
				cpu_stress_period = cpu_stress_params['T'][0]

				# Append stress log to anomaly.log
				with open(script_folder + "/anomaly.log", "a") as logFile:
					logFile.write(str(time.time()) + ", cpu, " + str(cpu_stress_period) + ", " + str(cpu_stress_workers) + "\n")

				p = sub.Popen('stress --cpu ' + cpu_stress_workers + ' --timeout ' + cpu_stress_period, shell=True, stdout=sub.PIPE, stderr=sub.PIPE)
				# output, errors = p.communicate()

				#note that this potentially makes every file on your computer readable by the internet
				self.send_response(200)
				self.end_headers()
				# serve the HTML code to client on Google App Engine Python using webapp2
				self.wfile.write("Processing the cpu stress with " + cpu_stress_workers + " workers spinning sqrt() for " + cpu_stress_period + " seconds!")
				# self.wfile.write(output)
				return
			elif self.path.startswith('/io'):
				# default: just send the file
				url = self.path
				params = url.split('?')[1]
				print params
				io_stress_params = urlparse.parse_qs(params)
				print io_stress_params
				io_stress_workers = io_stress_params['N'][0]
				io_stress_period = io_stress_params['T'][0]

				# Append stress log to anomaly.log
				with open(script_folder + "/anomaly.log", "a") as logFile:
					logFile.write(str(time.time()) + ", io, " + str(io_stress_period) + ", " + str(io_stress_workers) + "\n")

				p = sub.Popen('stress --io ' + io_stress_workers + ' --timeout ' + io_stress_period, shell=True, stdout=sub.PIPE, stderr=sub.PIPE)

				#note that this potentially makes every file on your computer readable by the internet
				self.send_response(200)
				self.end_headers()
				# serve the HTML code to client on Google App Engine Python using webapp2
				self.wfile.write("Processing the I/O stress with " + io_stress_workers + " workers spinning rsync() for " + io_stress_period + " seconds!")
				return
			elif self.path.startswith('/mem'):
				# default: just send the file
				url = self.path
				params = url.split('?')[1]
				print params
				mem_stress_params = urlparse.parse_qs(params)
				print mem_stress_params
				mem_stress_workers = mem_stress_params['N'][0]
				mem_size_per_worker = mem_stress_params['B'][0]
				mem_stress_period = mem_stress_params['T'][0]

				# Append stress log to anomaly.log
				with open(script_folder +"/anomaly.log", "a") as logFile:
					logFile.write(str(time.time()) + ", mem, " + str(mem_stress_period) + ", " + str(mem_stress_workers) + ", " + str(mem_size_per_worker)+ "\n")

				p = sub.Popen('stress --vm ' + mem_stress_workers + ' --vm-bytes ' + mem_size_per_worker + 'M --timeout ' + mem_stress_period, shell=True, stdout=sub.PIPE, stderr=sub.PIPE)

				#note that this potentially makes every file on your computer readable by the internet
				self.send_response(200)
				self.end_headers()
				# serve the HTML code to client on Google App Engine Python using webapp2
				self.wfile.write("Processing the memory stress with " + mem_stress_workers + " workers spinning malloc()/free() with " + mem_size_per_worker + " MB per worker for " + mem_stress_period + " seconds!")
				return
			elif self.path.startswith('/bw'):
				# default: just send the file
				url = self.path
				params = url.split('?')[1]
				print params
				bw_stress_params = urlparse.parse_qs(params)
				print bw_stress_params
				bw_throttle_interface = bw_stress_params['type'][0]
				bw_capacity = bw_stress_params['X'][0]
				bw_stress_period = bw_stress_params['T'][0]
				if bw_throttle_interface is '0':
					bw_cmd = script_folder + '/limitInbound.sh ' + str(bw_stress_period) + ' ' + bw_capacity
					intf_name = 'inbound'
				else:
					bw_cmd = script_folder + '/limitOutbound.sh ' + str(bw_stress_period) + ' ' + bw_capacity
					intf_name = 'outbound'
				
				# Append stress log to anomaly.log
				with open(script_folder +"/anomaly.log", "a") as logFile:
					logFile.write(str(time.time()) + ", bw-" + intf_name + ", " + str(bw_stress_period) + ", " + str(bw_capacity) + "\n")

				p = sub.Popen(bw_cmd, shell=True, stdout=sub.PIPE, stderr=sub.PIPE)

				#note that this potentially makes every file on your computer readable by the internet
				self.send_response(200)
				self.end_headers()
				# serve the HTML code to client on Google App Engine Python using webapp2
				self.wfile.write("Throttling the bandwidth on " + intf_name + " to " + bw_capacity + "kbps for " + bw_stress_period + " seconds!")
				return
			elif self.path.startswith('/httpd'):
				# default: just send the file
				url = self.path
				params = url.split('?')[1]
				print params
				httpd_stop_params = urlparse.parse_qs(params)
				httpd_stop_period = httpd_stop_params['T'][0]
				httpd_cmd = script_folder + '/stop_httpd.sh ' + str(httpd_stop_period)
				
				# Append stress log to anomaly.log
				with open(script_folder +"/anomaly.log", "a") as logFile:
					logFile.write(str(time.time()) + ",httpd," + str(httpd_stop_period) + ",stop\n")

				p = sub.Popen(httpd_cmd, shell=True, stdout=sub.PIPE, stderr=sub.PIPE)

				#note that this potentially makes every file on your computer readable by the internet
				self.send_response(200)
				self.end_headers()
				# serve the HTML code to client on Google App Engine Python using webapp2
				self.wfile.write("Stops Apache2 httpd server for " + httpd_stop_period + " seconds!")
				return
			elif self.path.startswith('/lat'):
				# default: just send the file
				url = self.path
				params = url.split('?')[1]
				print params
				lat_params = urlparse.parse_qs(params)
				lat_period = lat_params['T'][0]
				lat_val = lat_params['L'][0]
				lat_ip = lat_params['ip'][0]
				add_lat_cmd = script_folder + '/addLatPerIP.sh ' + str(lat_period) + ' ' + str(lat_ip) + ' ' + str(lat_val)
				
				# Append stress log to anomaly.log
				with open(script_folder +"/anomaly.log", "a") as logFile:
					logFile.write(str(time.time()) + ",addlat," + str(lat_period) + "," + lat_ip + "," + lat_val + "\n")

				p = sub.Popen(add_lat_cmd, shell=True, stdout=sub.PIPE, stderr=sub.PIPE)

				#note that this potentially makes every file on your computer readable by the internet
				self.send_response(200)
				self.end_headers()
				# serve the HTML code to client on Google App Engine Python using webapp2
				self.wfile.write("Add latency " + lat_val + " for packets to prefix " + lat_ip + " for " + lat_period +" seconds!")
				return

		except IOError as e :  
			# debug     
			print e
			self.send_error(404,'File Not Found: %s' % self.path)

#==========================================================================================
# Main Function of Cache Agent
#==========================================================================================
def main(argv):
	if sys.argv[1:]:
	    port = int(sys.argv[1])
	else:
	    port = 8717

	if sys.argv[2:]:
	    os.chdir(sys.argv[2])

	server = ThreadingSimpleServer(('', port), RequestHandler)
	try:
	    while 1:
	        sys.stdout.flush()
	        server.handle_request()
	except KeyboardInterrupt:
	    print("Finished")

if __name__ == '__main__':
    main(sys.argv)
 
