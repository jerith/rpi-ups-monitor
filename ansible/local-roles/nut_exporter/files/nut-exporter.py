#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler
import os
import socketserver
import subprocess

PORT = int(os.environ.get('NE_PORT', '9230'))
UPS = os.environ.get('NE_UPS', 'ups')

def call_upsc(ups):
    result = subprocess.run(['/bin/upsc', ups], stdout=subprocess.PIPE)
    return dict(l.split(': ') for l in result.stdout.decode('utf8').splitlines())

def field_to_metric(field):
    metric = field.replace('.', '_')
    # We use old-style formatting here to build a new-style format string.
    return '\n'.join([
        '# TYPE %s gauge' % metric,
        '%s{{ups="{ups}"}} {fields[%s]}' % (metric, field),
        '',
    ])

def fields_to_metrics(ups, fields):
    metrics = [field_to_metric(field) for field in [
        'battery.charge',
        'battery.voltage',
        'battery.voltage.high',
        'battery.voltage.low',
        'battery.voltage.nominal',
        'input.current.nominal',
        'input.frequency',
        'input.frequency.nominal',
        'input.voltage',
        'input.voltage.fault',
        'input.voltage.nominal',
        'output.voltage',
        'ups.delay.shutdown',
        'ups.delay.start',
        'ups.load',
    ]]
    # ups.status is different.
    metrics.append('\n'.join([
        '# TYPE ups_status gauge',
        'ups_status{{ups="{ups}", status="{fields[ups.status]}"}} 1',
        '',
    ]))
    return '\n'.join(metrics).format(ups=ups, fields=fields)

class NutMetrics(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != '/metrics':
            self.send_error(404)
            return
        fields = call_upsc(UPS)
        metrics = fields_to_metrics(UPS, fields).encode('utf8')
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; version=0.0.4')
        self.send_header('Content-Length', len(metrics))
        self.end_headers()
        self.wfile.write(metrics)


if __name__ == '__main__':
    httpd = socketserver.TCPServer(("", PORT), NutMetrics)
    print("serving on port", PORT)
    try:
        httpd.serve_forever()
    except:
        httpd.shutdown()
        raise
