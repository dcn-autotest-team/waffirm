#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# *********************************************************************
# Software : PyCharm
#
# dcnhtmllog.py - 
#
# Author    :yanwh(yanwh@digitalchina.com)
#
# Version 1.0.0
#
# Copyright (c) 2004-9999 Digital China Networks Co. Ltd 
#
#
# *********************************************************************
# Change log:
#       - 2018/3/29 17:04  add by yanwh
#
# *********************************************************************
"""
Python logg to html file.
Compatable for both python2 and python3
The benefit of writing log to html: We can highlight the keyword or
the error, to make the log file more colorful and understandable.
And it includes writing log to console.
Usage:
 -instance a object of PyLogger
 -log as what you did when using python built-in logging.
"""

import logging
import logging.handlers
import os
import sys
import traceback

# Add _levelNames
logging.TABLE = 25
logging.addLevelName(logging.TABLE, 'TABLE')

#: HTML header (starts the document
START_OF_DOC_FMT = """<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>%(title)s</title>
<style type="text/css">
body, html {
background: #000000;
width: auto;
font-family: Arial;
font-size: 16px;
color: #C0C0C0;
}
h1 {
color : #FFFFFF;
border-bottom : 1px dotted #888888;
}
.box {
border : 1px dotted #818286;
padding : 5px;
margin: 5px;
width: auto;
background-color : #292929;
}
.err {
word-break:break-all; word-wrap:break-all;
color: %(err_color)s;
font-family : arial;
margin : 0;
}
.warn {
word-break:break-all; word-wrap:break-all;
color: %(warn_color)s;
font-family : arial;
margin : 0;

}
.info {
word-break:break-all; word-wrap:break-all;
color: %(info_color)s;
font-family : arial;
margin : 0;
}
.debug {
word-break:break-all; word-wrap:break-all;
color: %(dbg_color)s;
font-family : arial;
margin : 0;
}
</style>
</head>
<body>
<h1>%(title)s</h1>

<p>查看分类日志类型:
<select id="mySelect" onchange="cate_fun()">
  <option value="ALL">ALL
  <option value="DEBUG">DEBUG
  <option value="INFO">INFO
  <option value="WARNING">WARNING
  <option value="ERROR">ERROR
</select> 
</p>

<form>
搜索指定日志信息:
<input type="text" id="text1" value="ALL" size="12"/>
<input type="checkbox" id="check1" />
<input type="button" id="button1" onclick="keyword_fun()" 
value="Seach" />
</form>

<script>
var level_index = 3
var msg_index = 4
function cate_fun(){
var tab = document.getElementById("toptable");
var slct_v = document.getElementById("mySelect").value;

for(var i=0; i<tab.rows.length;i++)
{
    if (tab.rows[i].cells[level_index].innerHTML=="DEBUG" & slct_v=="DEBUG")
    {
        tab.rows[i].style.display='';
    }
    else if (tab.rows[i].cells[level_index].innerHTML=="INFO" & slct_v=="INFO")
    {
        //console.log(i)
        //console.log(tab.rows[i].cells[level_index].innerHTML)
        tab.rows[i].style.display='';
    }
    else if (tab.rows[i].cells[level_index].innerHTML=="TABLE" & slct_v=="INFO")
    {
        tab.rows[i].style.display='';
    }
    else if (tab.rows[i].cells[level_index].innerHTML=="WARNING" & slct_v=="WARNING")
    {
        tab.rows[i].style.display='';
    }
    else if (tab.rows[i].cells[level_index].innerHTML=="ERROR" & slct_v=="ERROR")
    {
        tab.rows[i].style.display='';
    }
    else
    {
        if (slct_v=="ALL"){
            tab.rows[i].style.display='';
        }
        else{
            tab.rows[i].style.display='none';
        };
    };
}
}

function keyword_fun()
{
var tab = document.getElementById("toptable");
var Keyword = document.getElementById("text1").value;
if (document.getElementById("check1").checked)
    {
        Keyword=Keyword.toLowerCase();
    }
for (var i=0;i<tab.rows.length;i++) {
    if (Keyword=="ALL" || Keyword=="all")
    {
        tab.rows[i].style.display='';
    }
    else
    {
        var td_msg=tab.rows[i].cells[msg_index].innerHTML
        if (document.getElementById("check1").checked)
            {
                td_msg=td_msg.toLowerCase();
            }
        if (td_msg.indexOf(Keyword)>=0)
            {
                //console.log(Keyword)
                tab.rows[i].style.display='';
            }
        else
            {
                //console.log(i)
                tab.rows[i].style.display='none';
            };
    };  
  };
}

</script>

<div class="box">
<table id="toptable">
"""

END_OF_DOC_FMT = """</table>
</div>
</body>
</html>
"""
MSG_FMT = """
<tr>
<td width="1"> </td>
<td width="1"> </td>
<td width="1"> </td>
<td width="30">%(levelname)s</td>
<td class="%(cssname)s">%(message)s</td>
</tr>
"""
# MSG_FMT = """
# <tr>
# <td width="200">%(asctime)s</td>
# <td width="100">%(name)s</td>
# <td width="100">%(process)d</td>
# <td width="100">%(levelname)s</td>
# <td class="%(cssname)s">%(message)s</td>
# </tr>
# """

MID_OF_DOC_FMT = """
<!--
This following table were created by addtional thread-->
<div class="box">
<table id="toptable">
"""


class CONSOLE_COLOR:
    yellow = '\x1b[1;93m'
    cyan = '\x1b[1;36m'
    magenta = '\x1b[1;35m'
    blue = '\x1b[1;34m'
    orange = '\x1b[1;33m'
    green = '\x1b[1;32m'
    red = '\x1b[1;31m'
    black = '\x1b[1;30m'
    white = '\x1b[0m'
    normal = '\x1b[0m'


class HTMLFileHandler(logging.handlers.RotatingFileHandler):
    """
    File handler specialised to write the start of doc as html and to close it
    properly.
    """
    
    def __init__(self, filename, mode='a', maxBytes=0, rotating=False, backupCount=5,
                 START_OF_DOC_FMT=None, END_OF_DOC_FMT=None, encoding=None, delay=False,
                 title="Default Title"):
        """
        Open the specified file and use it as the stream for logging.

        By default, the file grows indefinitely. You can specify particular
        values of maxBytes and backupCount to allow the file to rollover at
        a predetermined size if rotating is set to True, otherwise ratating file
        without backCount limited.

        Rollover occurs whenever the current log file is nearly maxBytes in
        length. If backupCount is >= 1, the system will successively create
        new files with the same pathname as the base file, but with count and extensions
        "_1.html", "_2.html" etc. appended to it. For example, with a backupCount of 5
        and a base file name of "app.html", you would get "app.html",
        "app_1.html", "app_2.html", ... through to "app_5.html". The file being
        written to is always "app.log" - when it gets filled up, it is closed
        and renamed to "app_1.html", and if files "app_1.html", "app_2.html" etc.
        exist, then they are renamed to "app_2.html", "app_3.html" etc.
        respectively.

        If maxBytes is zero, rollover never occurs.
        """
        
        # Rewrite RotatingFileHandler.__init__()
        self.rotating = rotating
        self.Backup_Count = backupCount
        self.title = title
        self.start_of_doc_fmt = START_OF_DOC_FMT
        if maxBytes > 0:
            mode = 'a'
        logging.handlers.BaseRotatingHandler.__init__(self, filename, \
                                                      mode, encoding, delay)
        self.maxBytes = maxBytes - len(self.start_of_doc_fmt) - len(END_OF_DOC_FMT) - 3
        
        with open(self.baseFilename, 'r+') as infile:
            data = infile.read()
            if self.title in data:
                DOC_END_LEN = len(END_OF_DOC_FMT)
                # self.stream.write(MID_OF_DOC_FMT)
                infile.seek(0 - DOC_END_LEN, 2)
                infile.write(' ' * DOC_END_LEN)
                infile.seek(0, 2)
            else:
                self.stream.write(self.start_of_doc_fmt)
        # Must flush the buffer to prevent multi-START_OF_DOC_FMT in multiprocessing
        self.flush()
    
    def emit(self, record):
        """
        Rewrite emit for BaseRotatingHandler.emit(self,record)
        Emit a record.

        Output the record to the html file, catering for rollover as described
        in doRollover().
        """
        try:
            
            if self.shouldRollover(record):
                self.stream.write(END_OF_DOC_FMT)
                self.flush()
                self.doRollover()
                self.stream.write(self.start_of_doc_fmt)
                self.flush()
            logging.FileHandler.emit(self, record)
        except Exception:
            self.handleError(record)
    
    def doRollover(self):
        """
        Rewrite doRollover for BaseRotatingHandler.doRollover(self)
        Do a rollover, as described in __init__().
        """
        if self.stream:
            self.stream.close()
            self.stream = None
        base_fn = os.path.splitext(self.baseFilename)
        
        if self.rotating:
            backupCount = self.Backup_Count
        else:
            backupCount = 1
            while True:
                if not os.path.exists(self.rotation_filename("%s_%d%s" % \
                                                             (base_fn[0], backupCount, base_fn[1]))):
                    break
                backupCount += 1
        if backupCount > 0:
            for i in range(backupCount - 1, 0, -1):
                bfn_root, bfn_ext = os.path.splitext(self.baseFilename)
                sfn = self.rotation_filename("%s_%d%s" % (bfn_root, i, bfn_ext))
                dfn = self.rotation_filename("%s_%d%s" % (bfn_root, i + 1, bfn_ext))
                if os.path.exists(sfn):
                    if self.rotating:
                        if os.path.exists(dfn):
                            os.remove(dfn)
                    os.rename(sfn, dfn)
            dfn = self.rotation_filename(base_fn[0] + "_1" + base_fn[1])
            if os.path.exists(dfn):
                os.remove(dfn)
            self.rotate(self.baseFilename, dfn)
        if not self.delay:
            self.stream = self._open()
    
    def close(self):
        # finish document
        self.stream.write(END_OF_DOC_FMT)
        self.flush()
        # super().close()
        logging.handlers.RotatingFileHandler.close(self)


class HTMLFormatter(logging.Formatter):
    """
        Formatter instances are used to convert a LogRecord to text.

    Formatters need to know how a LogRecord is constructed. They are
    responsible for converting a LogRecord to (usually) a string which can
    be interpreted by either a human or an external system. The base Formatter
    allows a formatting string to be specified. If none is supplied, the
    default value of "%s(message)" is used.

    The Formatter can be initialized with a format string which makes use of
    knowledge of the LogRecord attributes - e.g. the default value mentioned
    above makes use of the fact that the user's message and arguments are pre-
    formatted into a LogRecord's message attribute. Currently, the useful
    attributes in a LogRecord are described by:

    %(name)s            Name of the logger (logging channel)
    %(levelno)s         Numeric logging level for the message (DEBUG, INFO,
                        WARNING, ERROR, CRITICAL)
    %(levelname)s       Text logging level for the message ("DEBUG", "INFO",
                        "WARNING", "ERROR", "CRITICAL")
    %(pathname)s        Full pathname of the source file where the logging
                        call was issued (if available)
    %(filename)s        Filename portion of pathname
    %(module)s          Module (name portion of filename)
    %(lineno)d          Source line number where the logging call was issued
                        (if available)
    %(funcName)s        Function name
    %(created)f         Time when the LogRecord was created (time.time()
                        return value)
    %(asctime)s         Textual time when the LogRecord was created
    %(msecs)d           Millisecond portion of the creation time
    %(relativeCreated)d Time in milliseconds when the LogRecord was created,
                        relative to the time the logging module was loaded
                        (typically at application startup time)
    %(thread)d          Thread ID (if available)
    %(threadName)s      Thread name (if available)
    %(process)d         Process ID (if available)
    %(message)s         The result of record.getMessage(), computed just as
                        the record is emitted
    """
    
    CSS_CLASSES = {'WARNING': 'warn',
                   'INFO': 'info',
                   'DEBUG': 'debug',
                   'CRITICAL': 'err',
                   'ERROR': 'err'}
    
    def __init__(self, fmt=None, Keyword_Italic=True, Keyword_FontSize=5,
                 Keyword_tag_start='<hl>', Keyword_tag_end='</hl>'):
        # super().__init__(fmt) #Not support Python2
        logging.Formatter.__init__(self, fmt)
        
        """
        Initialize the formatter with specified format strings.
        Keyword_tag_start & Keyword_tag_end: used to highlight message.
        Keyword_Italic: Make the part of the message italic if it's decorated by 
                 Keyword_tag_*
        Keyword_FontSize: The font size of the message italic if it's decorated by 
                 Keyword_tag_*
        """
        
        self.Keyword_Italic = Keyword_Italic
        self.Keyword_FontSize = Keyword_FontSize
        self.Keyword_tag_start = Keyword_tag_start
        self.Keyword_tag_end = Keyword_tag_end
    
    def format(self, record):
        try:
            class_name = self.CSS_CLASSES[record.levelname]
        except KeyError:
            class_name = "info"
        record.message = record.getMessage()
        
        if record.levelno % 10 == 0:
            record.message = self.__rsymbol(record.message)
        
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)
        record.cssname = class_name
        if self.Keyword_Italic:
            record.message = record.message.replace(self.Keyword_tag_start,
                                                    "<font size={0:d}><i>".format(self.Keyword_FontSize))
            record.message = record.message.replace(self.Keyword_tag_end,
                                                    "</i></font>")
        else:
            record.message = record.message.replace(self.Keyword_tag_start,
                                                    "<font size={0:d}>".format(self.Keyword_FontSize))
            record.message = record.message.replace(self.Keyword_tag_end,
                                                    "</font>")
        # print record.__dict__
        return MSG_FMT % record.__dict__
    
    def __rsymbol(self, message):
        if self.Keyword_tag_start in message:
            return message
        message = message.replace('&', '&amp;')
        message = message.replace('<', '&lt;')
        message = message.replace('>', '&gt;')
        message = message.replace('"', '&quot;')
        return message


class CONFormatter(logging.Formatter):
    """
    Formats each record to console with color.
    class CONSOLE_COLOR:(defined in this file), show how to decorate the message
    that is taged by Keyword_tag_*, add or edit if you like.

    AttributeError: this error is raised if the color you chose is not in the list
                   of CONSOLE_COLOR.
    """
    
    def __init__(self, fmt=None, Keyword_tag_start='<hl>',
                 Keyword_tag_end='</hl>', msg_color={'err_color': 'red',
                                                     'warn_color': 'yellow', 'info_color': 'white',
                                                     'dbg_color': 'white'}):
        # super().__init__(fmt)
        logging.Formatter.__init__(self, fmt)
        self.msg_color = msg_color
        self.Keyword_tag_start = Keyword_tag_start
        self.Keyword_tag_end = Keyword_tag_end
    
    def format(self, record):
        try:
            console_normal = getattr(CONSOLE_COLOR, 'normal')
            if record.levelname == 'ERROR':
                console_color = getattr(CONSOLE_COLOR, self.msg_color['err_color'])
            elif record.levelname == 'CRITICAL':
                console_color = getattr(CONSOLE_COLOR, self.msg_color['err_color'])
            elif record.levelname == 'WARNING':
                console_color = getattr(CONSOLE_COLOR, self.msg_color['warn_color'])
            elif record.levelname == 'DEBUG':
                console_color = getattr(CONSOLE_COLOR, self.msg_color['dbg_color'])
            elif record.levelname == 'INFO':
                console_color = getattr(CONSOLE_COLOR, self.msg_color['info_color'])
            else:
                console_color = console_normal
        except AttributeError:
            color_keys = list(CONSOLE_COLOR.__dict__.keys())
            color_keys.remove('__doc__')
            color_keys.remove('__weakref__')
            color_keys.remove('__module__')
            color_keys.remove('__dict__')
            t, v, tb = sys.exc_info()
            sys.stderr.write('\n--- Logging error ---\n')
            traceback.print_exception(t, v, tb, None, sys.stderr)
            sys.stderr.write('\n--- Logging error ---\n')
            sys.stderr.write('Does not support color error, choose one from list:' + \
                             '\n' + str(color_keys) + '\nEdit class CONSOLE to add more.\n')
            sys.exit()
        
        record.message = record.getMessage()
        record.message = record.message.replace(self.Keyword_tag_start, '')
        record.message = record.message.replace(self.Keyword_tag_end, '')
        if record.levelno > 20:
            record.message = console_color + record.message + console_normal
        
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)
        s = self._fmt % record.__dict__
        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        '''
        if record.exc_text:
            if s[-1:] != "\n":
                s = s + "\n"
            s = s + record.exc_text
        if record.stack_info:
            if s[-1:] != "\n":
                s = s + "\n"
            s = s + self.formatStack(record.stack_info)
        '''
        if record.exc_text:
            if s[-1:] != "\n":
                s = s + "\n"
            try:
                s = s + record.exc_text
            except UnicodeError:
                # Sometimes filenames have non-ASCII chars, which can lead
                # to errors when s is Unicode and record.exc_text is str
                # See issue 8924.
                # We also use replace for when there are multiple
                # encodings, e.g. UTF-8 for the filesystem and latin-1
                # for a script. See issue 13232.
                s = s + record.exc_text.decode(sys.getfilesystemencoding(),
                                               'replace')
        return s


class HTMLLogger(logging.Logger):
    """
    Log records to html using a custom HTML formatter and a specialised
    file stream handler.
    WARNING: This just creates signgal logger channel, use logging.getLogger
    name: The html logging thread name.
    html_filename: The file name that you want to write to
    mode: Specifies the mode to open the file, if filename is specified
          (if filemode is unspecified, it defaults to 'a').
    html_title: The title of the html specified above.
    level: Set the file and console logger level to the specified level.
    HtmlmaxBytes: The size of this html file
    encoding: it is used to determine how to do the output to the stream

    html_format: The same as logging.format

    msg_color: Dict with Key is the class that you wish to show and the value
               is the color.
    Keyword_Italic: Make the part of the message italic if it's decorated by
                 Keyword_tag_*
    Keyword_FontSize: The font size of the message italic if it's decorated by
                 Keyword_tag_*
    Html_Rotating: If we need to rotate the html file if the file is over the
                   limit of HtmlmaxBytes.
    Html_backupCount: How much the files we'll back if current file is over the
                   limit of HtmlmaxBytes.
    console_log: Print log to console if Ture.

    """
    
    def __init__(self, name="html_logger", html_filename="log.html", mode='a',
                 html_title="HTML Logger", root_level=logging.DEBUG, fh_level=logging.DEBUG,
                 ch_level=logging.DEBUG, HtmlmaxBytes=1024 * 1024, encoding=None, delay=False,
                 html_format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                 msg_color={'err_color': 'red', 'warn_color': 'red',
                            'info_color': 'white', 'dbg_color': 'white'},
                 Keyword_Italic=True, Keyword_FontSize=5, Keyword_tag_start="<hl>",
                 Keyword_tag_end="</hl>", Html_Rotating=False, Html_backupCount=5,
                 console_log=True):
        
        # super().__init__(name, root_level) #Not support Python2
        logging.Logger.__init__(self, name, root_level)
        
        START_DOC_DICT = {'title': ''}
        START_DOC_DICT.update(msg_color)
        START_DOC_DICT.update({'title': html_title})
        start_of_doc_fmt = START_OF_DOC_FMT % START_DOC_DICT
        
        format_html = HTMLFormatter(html_format, Keyword_Italic, Keyword_FontSize, Keyword_tag_start, Keyword_tag_end)
        
        # FIXME: the argument should be move to another place?
        fh = HTMLFileHandler(filename=html_filename, mode=mode, maxBytes=HtmlmaxBytes, rotating=Html_Rotating,
                             backupCount=Html_backupCount,
                             START_OF_DOC_FMT=start_of_doc_fmt, END_OF_DOC_FMT=END_OF_DOC_FMT, encoding=encoding,
                             delay=delay, title=html_title)
        fh.setLevel(fh_level)
        fh.setFormatter(format_html)
        self.addHandler(fh)
        
        if console_log:
            format_con = CONFormatter(html_format, Keyword_tag_start,
                                      Keyword_tag_end, msg_color)
            ch = logging.StreamHandler()
            ch.setLevel(ch_level)
            ch.setFormatter(format_con)
            self.addHandler(ch)
    
    # using logger.table(msg) to add table which contains html symbol
    def table(self, msg, *args, **kwargs):
        if self.isEnabledFor(logging.TABLE):
            self._log(logging.TABLE, msg, args, **kwargs)
