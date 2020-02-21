#!/usr/bin/python
#
# Copyright 2008-2010 Webdriver_name committers
# Copyright 2008-2010 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .chrome.options import Options as ChromeOptions
from .chrome.webdriver import WebDriver as Chrome
from .common.action_chains import ActionChains
from .common.desired_capabilities import DesiredCapabilities
from .common.proxy import Proxy
from .common.touch_actions import TouchActions
from .firefox.firefox_profile import FirefoxProfile
from .firefox.webdriver import WebDriver as Firefox
from .ie.webdriver import WebDriver as Ie
from .opera.webdriver import WebDriver as Opera
from .phantomjs.webdriver import WebDriver as PhantomJS
from .remote.webdriver import WebDriver as Remote
from .safari.webdriver import WebDriver as Safari

__version__ = '2.37.2'
