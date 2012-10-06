#!/bin/bash

dflat=build/release/dflat
gringo=../gringo
clasp=../clasp

exchangeEnc=asp_encodings/sat/exchange.lp
exchangeDecEnc=asp_encodings/sat/exchange_decision.lp
joinEnc=asp_encodings/sat/join.lp
monolithicEnc=asp_encodings/sat/monolithic.lp

echo "width,vars,num,extraclauses,seed,sat_enum,monolithic_enum,sat_counting,monolithic_counting,sat_decision,monolithic_decision,models"

function printTime {
time=$1
exitCode=$2
case "$exitCode" in
	134 | 2)
		echo -n "memout,"
		;;
	137)
		echo -n "timeout,"
		;;
	*)
		echo -n "$time,"
		;;
esac
}

for f in $@; do
	suffix=${f##*width}
	instance_data=${suffix%%.lp}
	IFS="_/" read width vars num extraedges seed <<< "$instance_data"
	echo -n "$width,$vars,$num,$extraedges,$seed,"

	unset count

	# ENUMERATION
	read curCount time exitCode <<< $(\time -f "TIME %U %S %x" bash -c "$dflat -p enumeration -e pos -e neg -x $exchangeEnc -j $joinEnc -s $seed < $f" 2>&1 | grep "^Solutions:\|^TIME" | awk 'BEGIN { sol = 0 } /^Solutions:/ { sol = $2 } /^TIME/ { time = $2+$3; code = $4 } END { printf("%s %s %s", sol, time, code) }')
	printTime $time $exitCode

	if [[ $exitCode -eq 10 || $exitCode -eq 20 ]]; then
		count=$curCount
	fi

	read curCount time exitCode <<< $(\time -f "%U %S %x" bash -c "$gringo $f $monolithicEnc 2>/dev/null | $clasp 0" 2>&1 | tail -n5 | awk 'NR == 1 { if($0 ~ /^Models/) printf("%s ", $3); else printf("? ")} NR == 5 {printf("%s %s", $1+$2, $3)}')
	printTime $time $exitCode

	if [[ $exitCode -eq 10 || $exitCode -eq 20 ]]; then
		if [[ "$count" && $count -ne $curCount ]]; then
			echo mismatch
			exit 1
		fi
		count=$curCount
	fi

	# COUNTING
	read curCount time exitCode <<< $(\time -f "TIME %U %S %x" bash -c "$dflat -p counting -e pos -e neg -x $exchangeEnc -j $joinEnc -s $seed < $f" 2>&1 | grep "^Solutions:\|^TIME" | awk 'BEGIN { sol = 0 } /^Solutions:/ { sol = $2 } /^TIME/ { time = $2+$3; code = $4 } END { printf("%s %s %s", sol, time, code) }')
	printTime $time $exitCode

	if [[ $exitCode -eq 10 || $exitCode -eq 20 ]]; then
		if [[ "$count" && $count -ne $curCount ]]; then
			echo mismatch
			exit 2
		fi
		count=$curCount
	fi

	read curCount time exitCode <<< $(\time -f "%U %S %x" bash -c "$gringo $f $monolithicEnc 2>/dev/null | $clasp -q 0" 2>&1 | tail -n5 | awk 'NR == 1 { if($0 ~ /^Models/) printf("%s ", $3); else printf("? ")} NR == 5 {printf("%s %s", $1+$2, $3)}')
	printTime $time $exitCode

	if [[ $exitCode -eq 10 || $exitCode -eq 20 ]]; then
		if [[ "$count" && $count -ne $curCount ]]; then
			echo mismatch
			exit 3
		fi
		count=$curCount
	fi

	# DECISION
	read time exitCode <<< $(\time -f "%U %S %x" bash -c "$dflat -p decision -e pos -e neg -x $exchangeDecEnc -j $joinEnc -s $seed < $f" 2>&1 | tail -n1 | awk '{printf("%s %s", $1+$2, $3)}')
	printTime $time $exitCode

	read time exitCode <<< $(\time -f "%U %S %x" bash -c "$gringo $f $monolithicEnc 2>/dev/null | $clasp -q" 2>&1 | tail -n1 | awk '{printf("%s %s", $1+$2, $3)}')
	printTime $time $exitCode

	if [[ "$count" ]]; then
		echo "$count"
	else
		echo unknown
	fi
done
