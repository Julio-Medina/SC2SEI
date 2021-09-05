#!/bin/bash


source ${TOP_DIR}/sc2sei.conf


sc2sei_ID_old(){
	ID=$1
	echo "iniciando solicitud del evento ${ID}"
	scxmldump -fPAMF -E ${ID} -o ${ID}.xml -d mysql://${USER}:${PSWD}@${SERVER}/${SCDB}
	scbulletin -3 -x -i ${ID}.xml  > ${ID}.txt


	WAV=$(ssh -q ${SSH_SERVER} find /media/HDD/seiscomp -iname ${ID}.mseed)

	if [[ -z ${WAV} ]]
	then
		echo "WAV NOT FOUND, MAKING REQUEST"
		ssh  ${SSH_SERVER} "source /home/insivumeh/.seiscomp.bash ; /opt/seiscomp/bin/REQUEST-WAV -I ${ID}"
		WAV=$(ssh ${SSH_SERVER}  "source /home/insivumeh/.bashrc ; find /media/HDD/seiscomp -iname ${ID}.mseed")
	### si funciona... pero tira errores, las cuales asumo es por variables de entorno
		if [[ -z ${WAV} ]]
		then
			echo "WAV NOT FOUND... BYE"
			exit 0
		else
			scp ${SSH_SERVER}:${WAV} .
		fi
	else
		scp ${SSH_SERVER}:${WAV} .
	fi

}


sc2sei_ID(){
	ID=$1
	echo "iniciando solicitud del evento ${ID}"
	scxmldump -fPAMF -E ${ID} -o ${ID}.xml -d mysql://${USER}:${PSWD}@${SERVER}/${SCDB}
	scbulletin -3 -x -i ${ID}.xml  > ${ID}.txt
	scevtstreams -v -E ${ID} -d mysql://${USER}:${PSWD}@${SERVER}/${SCDB} \
        -m 45,90 -R --all-stations |\
       scart -dsv -l - $ARCHIVE > ${ID}.mseed

}


while test $# -gt 0
do
	case "$1"
	in
		-H | --hours)
		shift
		if test $# -gt 0
		then
			export H=$1
		else
			echo "no hours define"
		fi
		shift
		;;

		-ID )
		shift
		if test $# -gt 0
		then
			export ID=$1
			echo "--- $ID ----"
		else
			echo "ID define"
		fi
		shift
		;;

		*)
		#### revisar esto
		echo "usage :"
		echo "sc2sei -ID [id-event]"
		echo "sc2sei -h [#hours]"
		exit
		;;
	esac
done


if [[ -e ${HOME}/.seiscomp.bash ]]
then
	source ${HOME}/.seiscomp.bash
else
	echo "no env for seiscomp"
	exit 0
fi

if [[ -n $H ]]
then
	listado -h ${H} -q
	while read ID
	do
		sc2sei_ID "${ID}"
	done < /tmp/seiscomp/listado/sc_events.txt

elif [[ -n $ID ]]
then
#	sc2sei_ID_old "${ID}"
	sc2sei_ID "${ID}"

else
	echo "usage :"
	echo "sc2sei -ID [id-event]"
	echo "sc2sei -h [#hours]"

fi

