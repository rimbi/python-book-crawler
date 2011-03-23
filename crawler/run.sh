#!/bin/sh

crawl_list="./scrapy-ctl.py list"
crawl_exec="./scrapy-ctl.py crawl"
pattern=".(com|net|gen|org)(.tr|)$"

list=0

while getopts "o:lh" optname
do
    case "$optname" in
	o)
	    echo "Warning: Only run a site"
	    site=$OPTARG
	    ;;
	h)
	    cat << EOF
	    usage:
		./run [-o, -h] [site name]
	    -o: Optional parameter. Indicates that script should run only for a site instance.
		If site is provided as parameter, script should exit after finishes its execution.
	    
	    -l: Optional parameter. Lists the available book sites.

	    -h: Optional parameter. Prints this message.

	    [site name]: Optional parameter. Script starts from given site. If -o is provided, 'run' command should exit after executing the site.
			 If -o is not provided then, 'run' command should continue executing respectively.
	    example:
		./run -o idefix.com
			Run idefix.com then exits.

		./run -l
			List the book sites.

		./run
			Run all of the book sites.

EOF
	    exit 0
	    ;;
	l)
	    list=1
	    ;;
	:)
	    echo "HOP $OPTARG"
	    ;;
	*)
	    echo "Unknown error occured"
	    ;;
    esac
done

for line in $($crawl_list); do
    if [[ $line =~ $pattern ]]; then
	if [ -n "$site" ]; then
	    if [ "$site" != "$line" ]; then
		continue;
	    fi
	fi
	echo "Book Site: '$line'"
	if [ $list -eq 0 ]; then
	    echo "Crawling started . . ."
	    $($crawl_exec $line)
	    echo "Crawling done"
	fi
    fi
done