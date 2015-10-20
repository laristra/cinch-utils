#------------------------------------------------------------------------------#
# Warning Banner
#------------------------------------------------------------------------------#

if [ -t 1 ]; then

	# see if it supports colors...
	ncolors=$(tput colors)

	if test -n "$ncolors" && test $ncolors -ge 8; then
		RED='\033[0;31m'
		YELLOW='\033[1;33m'
		NC='\033[0m' # No Color

		printf "# ${YELLOW}!!!WARNING WARNING WARNING!!!${NC}\n"
		printf "# ${RED}THIS IS NOT A STANDARD GIT FEATURE!!!${NC}\n"
		printf "# ${RED}CINCH-UTILS MUST BE INSTALLED TO"
		printf "# USE THIS SCRIPT!!!${NC}\n"
		printf "# ${YELLOW}!!!WARNING WARNING WARNING!!!${NC}\n"
	fi
fi
