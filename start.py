#!/usr/bin/env python
#
# Copyright 2015 PakTrack
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import tornado.auth
import tornado.escape
import tornado.ioloop
import tornado.web

from tornado import gen
from tornado.options import define, options, parse_command_line
from tornado.web import asynchronous, RequestHandler, Application
import tcelery
import paktrack.tasks as tasks

tcelery.setup_nonblocking_producer()

define("port", default=8888, help="run on the given port", type=int)
define("debug", default=False, help="run in debug mode")
define("db_host", default="test.pak-track.com", help="paktrack database host")
define("db_user", default="", help="paktrack database user name")
define("db_pass", default="", help="paktrack database password")
define("db_port", default=27017, help="paktrack database port", type=int)
define("db", default="paktrackDB", help="paktrack database")


class VibartionReportHandler(RequestHandler):
    @asynchronous
    @gen.coroutine
    def get(self, truck_id, package_id):
        gen.Task(
            tasks.vib_consolidated_report.apply_async,
            args=[options.db_host, options.db_port, options.db,
            options.db_user, options.db_pass,
            truck_id, package_id], queue="vibration_report")
        self.write({"data": "queued"})
        self.finish()

    @asynchronous
    @gen.coroutine
    def post(self, id):
        gen.Task(
            tasks.process_vibration.apply_async,
            args=[options.db_host, options.db_port, options.db,
            options.db_user, options.db_pass, id], queue="vibration")
        self.write({"data": "queued"})
        self.finish()


class ShockDataHandler(RequestHandler):
    @asynchronous
    @gen.coroutine
    def post(self, id):
        gen.Task(tasks.process_shock.apply_async,
            args=[options.db_host, options.db_port, options.db,
            options.db_user, options.db_pass,id], queue="shock")
        self.write({"data": "queued"})
        self.finish()


class CustomReportHandler(RequestHandler):
    @asynchronous
    @gen.coroutine
    def post(self, truck_id, package_id):
        ids = self.get_argument('ids')
        gen.Task(
            tasks.vib_custom_report.apply_async,
            args=[options.db_host, options.db_port, options.db,
            options.db_user, options.db_pass, truck_id, package_id, ids], queue="vibration_report")
        self.write({"data": "queued"})
        self.finish()


def get_routes():
    return [(r"/tasks/vibration/report/(.*)/(.*)", VibartionReportHandler),
            (r"/tasks/vibration/(.*)", VibartionReportHandler),
            (r"/tasks/shock/(.*)", ShockDataHandler),
            (r"/tasks/vibration/custom/report/(.*)/(.*)", CustomReportHandler)]


def main():
    parse_command_line()
    application = Application(get_routes())
    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
