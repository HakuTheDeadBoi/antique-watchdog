# antique-watchdog

Antique-watchdog alias antique book store watchdog.

Scheduler which allows user to import his own web scrapers to scrape the web using his own queries, creates a report and send it via email.
Scheduler itself will only maintain scheduling scripts and collecting reports.
Finding books (if they are available on particular store) is the matter of particular script, making a report too. Scheduler just call the script, receives a report, collect all reports, log everything and send.

I hope it will be useful at least for me. I hope it will be fun to code.