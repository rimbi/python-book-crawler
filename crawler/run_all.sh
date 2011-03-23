#!/bin/sh

crawl_list="./scrapy-ctl.py list"
crawl_exec="./scrapy-ctl.py crawl"
pattern=".(com|net|gen|org)(.tr|)$"

for line in $($crawl_list); do
    if [[ $line =~ $pattern ]]; then
	echo "[run_all] Crawling $line"
	$($crawl_exec $line)
    fi
done