# Python 3 "Violent Python" Source Code

Source code for the book "Violent Python" by TJ O'Connor. The code has been fully converted to Python 3, reformatted to comply with PEP8 standards and refactored to eliminate dependency issues involving the implementation of deprecated libraries.

*A conversion similar to this one has been made available by myself on the
 source code of the book "Black Hat Python", by Justin Seitz. Check it out
  [here](https://github.com/EONRaider/blackhat-python3) if you haven't done it
   yet.*

## Usage
Simply make a new directory (DIR) for the project, create a new
 virtual environment or `venv` for it (recommended), clone this repository
  using `git clone` and install the requirements using `pip install`.

```
user@host:~/DIR$ git clone https://github.com/EONRaider/violent-python3
user@host:~/DIR$ python3 -m venv venv
user@host:~/DIR$ source venv/bin/activate
(venv) user@host:~/DIR$ pip install -r requirements.txt
```

## Notes

- The directories and files have been named in a way that they can be easily
 related to the content that is presented at each chapter.
- The frequent use of string concatenation by the author has been replaced by
 string interpolation in order to allow greater readability and conform to a
  more modern standard.
- Names of files, variables, functions, classes and methods now conform to
 PEP 8 naming standards.
- The now deprecated `optparse` library has been replaced for `argparse` 
throughout the entire source code. All argument parsing is now contained
 under the `__main__` execution scope for each file. All CLI arguments that were
  mandatory for the execution of scripts but were treated as optional in the
   original code are now implemented as positional. A *usage* prompt is now
    available for all scripts that use `argparse` by supplying a -h argument to
     the CLI. Leaving the responsibilities of both boundary and controller
      object to the CLI parser is definitely not the best choice in terms
       of software architecture, but was left as-is due to the
        necessity of conformity to the original coder's intent.
- All occurrences of `PEP 8: E722 do not use bare except` violations have
 been refactored with more specific exception clauses.
- The author has a habit of opening files/databases and leaving them in this
 state
 instead of calling the `close()` method on the open file/database objects. For
  this
  reason all instances of file and database manipulation have been refactored by
   using context managers.
- The use of comments making reference to the encoding to be used by the
 interpreter (namely, `# -*- coding: utf-8 -*-`) was eliminated due to the
  standardization of UTF-8 as the default encoding for Python 3 (replacing
   ASCII from Python 2).
- Though completely inadequate from the
     perspective of best-practices, the use of global variables was left
      untouched in preference to producing heavy deviations from the original
       code's logic.
- The code included in Chapter 5 of the book has been refactored even though in
 practical terms it can be, at best, historical. Much of its functionality
  depends not only on very specific cases outlined as examples by the author
   but also exploit vulnerabilities that ceased to be realistic in the last
    few years (such as sniffing traffic from 802.11 wireless networks that
     still rely on the WEP security algorithm for traffic encryption or, worst, that 
     maintain no security at all) or the absurd expectation of acquisition of a
      specific UAV model by the reader if he intends to see the code at work. 
      To avoid stating straight away that the effort invested in reading this
       chapter is nearly pointless, I might add that some utility can be
      extracted from the code related to the sniffing of probing and beacon requests, though.
- The code on Chapter 6 that makes reference to Google and Twitter proved
   too outdated in the way they handle current APIs to be worth the
    trouble of refactoring. If you're interested in dealing with them, 
    perform the refactoring and issue a pull request to this repository.

## Refactoring
Files not listed below can be assumed to have been refactored in one way or
 another as established in the "Notes" section.
- `chapter01/vuln_scanner.py` was structured in such a way that a non-existent file would lead to a `OSError` exception at runtime. For that
 reason the iteration control that calls `check_vulns()` was moved into the
  conditional statement defined in the main function.
- `chapter02/nmap_scan.py` implemented a main function solely for the purpose
 of calling the deprecated `optparse` library, which has been replaced by
  `argparse`. Because of that the main function was removed. An iteration
   control structure that was part of the `optparse` call in the original
    code was implemented in such a way that a new call to nmap was executed
     for each port scanned. The iteration was moved into the `nmap_scan` 
     function to prevent wasting cycles.
- `chapter02/ssh_command.py` had its initialization code moved into the
 `__main__` execution scope. The names of variables used in the outer scope
  that used to conflict with the names of parameters of functions were
   changed. The returning prompt information was originally encoded and now
    has been decoded in order to afford better readability.
- `chapter02/ssh_brute.py` imported `pxssh` as a standalone library, but in
 fact it is a library under the `pexpect` library. The bug led to a
  `ModuleNotFoundError` and has been corrected. The code itself as presented in the
   book was littered with indentation errors that made it unusable and has 
    been brought to a functioning state. 
- `chapter02/ssh_brutekey.py` required a number of pre-generated keys to work; 
furthermore the book points the reader to acquire such keys in a URL
 that currently returns a 403 response. Because of that a compressed archive
  containing the keys has been added to the `chapter02` subdirectory.
- `chapter02/ssh_botnet.py` had an unused import statement to `optparse` that
 was removed. It looks like it was a fragment from an aborted attempt to
  implement a CLI to this script. Surprisingly it was just left hanging there, 
  even in the printed version of the book. The code that initializes the
   botnet and issues its commands was organized under the `__main__` execution 
   scope for the sake of standardization. The two commands issued to the bots
    have been unified to avoid an unnecessary number of return statements.
- `chapter02/conficker.py` removed unused call to `sys` library.
- `chapter03/discover_networks.py` had to be reimplemented instead of just
 refactored. It originally not only used the deprecated `mechanize` library but
  also interacted with the WiGLE service in a way that is no longer necessary, 
  once WiGLE now provides an API. For that reason the code has been standardized
    and a new `wigle_print` function was implemented by using the `requests
    ` library to send an authenticated HTTP GET request to WiGLE. The
     response returns a JSON object that can be directly accessed, making
      the use of the `re` library also unnecessary. Exception handling was
       added to make the script capable of dealing with error response
        messages sent by the API. Notice that
     this script depends on `winreg`, which only runs on Python installations
      under the Microsoft Windows OS, and requires Administrator privileges
       during execution for access to the Registry keys. An account has to be 
       registered on https://wigle.net/account for access to the API.
- `chapter03/pdf_read.py` now uses the `PyPDF4` library instead of the
 deprecated `PyPDF`. The book refers to a specific PDF file in the text and
  it has been added to the `chapter03` subdirectory.
- `chapter03/exif_fetch.py` required a `features="html.parser"` argument on
 the call to the `BeautifulSoup` object constructor. It was added on line 15
 . This script only works on web applications that wrap images between `img`
  HTML tags (a rare practice on modern web applications that rely heavily on
  JavaScript).
- `chapter03/skype_parse.py` uses the `main.db` file as an example. It has been
 added to the `chapter03/skype_profile` subdirectory for convenience.
- `chapter03/firefox_parse.py` uses several `.sqlite` files as examples. They 
 have been added to the `chapter03/firefox_profile` subdirectory for
  convenience.
- `chapter03/iphone_messages.py` references iPhone backup files that were not
 made available by the author. Because of this the code has been refactored
  but remains untested.
- `chapter04/geo_ip.py` used the deprecated `pygeoip` library. As 
[suggested](https://github.com/appliedsec/pygeoip) by its creator, 
`geoip2` should now be used. An attempt was made to keep the newly
  implemented code as similar as possible to the original implementation on
   the book, but some changes had to be made to accommodate the new package
    structure of `geoip2` and its attributes. The database file necessary to
     run the script was downloaded from 
     [MaxMind](https://dev.maxmind.com/geoip/geoip2/downloadable/) and made
      available in the `chapter04` directory. A CLI was also implemented
     using `argparse`.
- `chapter04/print_direction.py` raised a `UnicodeDecodeError` exception when
 opening the file in the original implementation. It has been fixed by adding
  a *rb* argument to the context manager handling the file.
- `chapter04/find_ddos.py` printed the source address of the Hivemind
 attack as its destination, making the output useless. The correct *dst* 
 variable is now  displayed on stdout. The book references a file called
  `traffic.pcap` that was not made available by the author, so the code has
   been refactored but remains untested.
- `chapter04/test_domain_flux.py` returns that zero unanswered requests were
 made when analyzing the pcap file provided by the author. For some reason
  the packets themselves don't have the DNS Resource Record field value set,
  so the condition in the *dns_QR_test* function always evaluates as false. 
  That being the case, the condition evaluating the DNSRR field has been removed
   from the
   conditional statement and all UDP packets that have port 53 as their
    source are now analysed. It does result in less efficient code but at
     least it outputs the results as intended in the book.
- `chapter05/blue_bug.py` uses the `PyBluez` library, which in turn requests the
`BlueZ` library and header files as stated in its 
[installation instructions](https://github.com/pybluez/pybluez/blob/master/docs/install.rst).
These dependencies must be installed prior to installing `PyBluez` as a
 requirement. In Linux this can be performed by issuing the command 
 `apt install bluetooth libbluetooth-dev`. The original code references a 
 non-existent `client_sock` object that has been replaced by `phone_sock`.
- `chapter05/ftp_sniff.py` had a logic flaw that made it present a sniffed
 username but no password due to poor implementation of a `if... else` 
 statement. It has been corrected by replacing the conditional statement with
  a nested `if` clause.
- `chapter05/ninja_print.py` requires the `obexftp` library to work. This
 library was written for Python 2 and has not been ported 
  or replaced by an equivalent one to the present date, so the code remains
   as written by the author in its Python 2 version.
- `chapter05/__init__.py` and `chapter06/__init__.py` were added to enable
 the importing of modules from `chapter05/dup.py` and `chapter06/anon_browser.py`, 
 respectively.
 - `chapter06/anon_proxy.py` was re-implemented with the `MechanicalSoup` 
 Python 3 library. It integrates the modifications that were necessary to
  `proxy_test.py`, `useragent_test.py` and `print_cookies.py`.
- `chapter06/anon_browser.py` was also re-implemented with `MechanicalSoup` 
and went through some modifications in the code. The `cookielib` library
 was replaced by `http.cookiejar` in the constructor method for the
  *AnonBrowser* class and the parameter *user_agents* now accepts a list of
   strings instead of a tuple.
- `chapter06/link_parser.py` was refactored by using new ways to handle the
 implementations of `re` and `bs4`.

## Contributing

As a matter of common sense, first try to discuss the change you wish to make to
this repository via an issue.

1. Ensure the modifications you wish to introduce actually lead to a pull
request. The change of one line or two should be requested through an issue
 instead.
2. If necessary, update the README.md file with details relative to changes to
 the project structure.
3. Make sure the commit messages that include the modifications follow a
 standard. If you don't know how to proceed, [here](https://chris.beams.io/posts/git-commit/)
  is a great reference on how to do it.
4. Your request will be reviewed as soon as possible (usually within 48 hours).

