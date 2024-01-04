#!/usr/bin/env bash

############################################################
#
# Tavinus Cloud Sender 2
# cloudsend.sh
# https://github.com/tavinus/cloudsend.sh
#
# Uses curl to send files to a shared
# Nextcloud/Owncloud folder
#
# Usage: ./cloudsend.sh <file> <folderLink>
# Help:  ./cloudsend.sh -h
#
# Gustavo Arnosti Neves
# https://github.com/tavinus
#
# Contributors:
# @MG2R @gessel
#
# Get this script to current folder with:
# curl -O 'https://raw.githubusercontent.com/tavinus/cloudsend.sh/master/cloudsend.sh' && chmod +x cloudsend.sh
#
# NOTE: Cloudsend 2 changed the way password is handled and 
# is NOT compatible with cloudsend 1 calls. The -e parameter
# now does what -p parameter did (environment passwords), 
# while the -p parameter receives the password directly.
#
############################################################





CS_VERSION="2.2.8"

TRUE=0
FALSE=1

CLOUDURL=""
FOLDERTOKEN=""
INNERPATH=""

PUBSUFFIX="public.php/webdav"
HEADER='X-Requested-With: XMLHttpRequest'

CLOUDSEND_PARAMS=()
INSECURE=''
OUTFILE=''

RENAMING=$FALSE
QUIETMODE=$FALSE
GLOBBING=$FALSE
LIMITTING=$FALSE
LIMITCMD=''
RATELIMIT=''
GLOBCMD=' -g'
VERBOSE=' --progress-bar'

STTYBIN="$(command -v stty 2>/dev/null)"
BASENAMEBIN="$(command -v basename 2>/dev/null)"
FINDBIN="$(command -v find 2>/dev/null)"
SCREENSIZE="40  80"

DIRLIST=()
FILELIST=()

CURLEXIT=0
CURLRESPONSES=""
ABORTONERRORS=$FALSE





################################################################
#### CURL CALL EXAMPLE

# https://cloud.mydomain.net/s/fLDzToZF4MLvG28
# curl -k -T myFile.ext -u "fLDzToZF4MLvG28:" -H 'X-Requested-With: XMLHttpRequest' https://cloud.mydomain.net/public.php/webdav/myFile.ext





################################################################
#### MESSAGES
################################################################


# Logs message to stdout
log() {
	isQuietMode || printf "%s\n" "$@"
}


# Logs message to stdout
logSameLine() {
	isQuietMode || printf "%s" "$@"
}


# Prints program name and version
printVersion() {
        printf "%s\n" "Tavinus Cloud Sender v$CS_VERSION"
}


# Prints error messages and exits
initError() {
        printVersion >&2
        printf "%s\n" "Init Error! $1" >&2
        printf "%s\n" "Try: $0 --help" >&2
        exit 5
}


# Curl summed exit codes
# Will be 0 if no curl call had errors
curlAddExitCode() {
        ((CURLEXIT=CURLEXIT+$1))
}


# Curl appended messages
# Will probably be empty if curl was able to perfom as intended
curlAddResponse() {
        if isNotEmpty "$1"; then
                isEmpty "$CURLRESPONSES" && CURLRESPONSES="$2"$'\n'"$1" || CURLRESPONSES="$CURLRESPONSES"$'\n----------------\n'"$2"$'\n'"$1"
        fi
}


# Prints usage information (help)
usage() {
        printVersion
        printf "%s" "
Parameters:
  -h | --help              Print this help and exits
  -q | --quiet             Disables verbose messages
  -V | --version           Prints version and exits
  -r | --rename <file.xxx> Change the destination file name
  -g | --glob              Disable input file checking to use curl globs
  -k | --insecure          Uses curl with -k option (https insecure)
  -l | --limit-rate        Uses curl limit-rate (eg 100k, 1M)
  -a | --abort-on-errors   Aborts on Webdav response errors
  -p | --password <pass>   Uses <pass> as shared folder password
  -e | --envpass           Uses env var \$CLOUDSEND_PASSWORD as share password
                           You can 'export CLOUDSEND_PASSWORD' at your system, or set it at the call
                           Please remeber to also call -e to use the password set

Use:
  ./cloudsend.sh [options] <inputPath> <folderLink>
  CLOUDSEND_PASSWORD='MySecretPass' ./cloudsend.sh -e [options] <inputPath> <folderLink>

Passwords:
  Cloudsend 2 changed the way password works
  Cloudsend 0.x.x used the '-p' parameter for the Environment password (changed to -e in v2+)
  Please use EITHER -e OR -p, but not both. The last to be called will be used

    Env Pass > Set the variable CLOUDSEND_PASSWORD='MySecretPass' and use the option '-e'
  Param Pass > Send the password as a parameter with '-p <password>'

Folders:
  Cloudsend 2.2.0 introduces folder tree sending. Just use a directory as <inputPath>.
  It will traverse all files and folders, create the needed folders and send all files.
  Each folder creation and file sending will require a curl call.

Input Globbing:
  You can use input globbing (wildcards) by setting the -g option
  This will ignore input file checking and pass the glob to curl to be used
  You MUST NOT rename files when globbing, input file names will be used
  You MUST NOT send folders when globbing, only files are allowed
  Glob examples: '{file1.txt,file2.txt,file3.txt}'
                 'img[1-100].png'

Send from stdin (pipe):
  You can send piped content by using - or . as the input file name (curl specs)
  You MUST set a destination file name to use stdin as input (-r <name>)

  Use the file name '-' (a single dash) to use stdin instead of a given file
  Alternately, the file name '.' (a single period) may be specified instead of '-' to use
  stdin in non-blocking mode to allow reading server output while stdin is being uploaded

Examples:
  CLOUDSEND_PASSWORD='MySecretPass' ./cloudsend.sh -e './myfile.txt' 'https://cloud.mydomain.net/s/fLDzToZF4MLvG28'
  ./cloudsend.sh './myfile.txt' 'https://cloud.mydomain.net/s/fLDzToZF4MLvG28'
  ./cloudsend.sh 'my Folder' 'https://cloud.mydomain.net/s/fLDzToZF4MLvG28'
  ./cloudsend.sh -r 'RenamedFile.txt' './myfile.txt' 'https://cloud.mydomain.net/s/fLDzToZF4MLvG28'
  ./cloudsend.sh --limit-rate 200K -p 'MySecretPass' './myfile.txt' 'https://cloud.mydomain.net/s/fLDzToZF4MLvG28'
  ./cloudsend.sh -p 'MySecretPass' -r 'RenamedFile.txt' './myfile.txt' 'https://cloud.mydomain.net/s/fLDzToZF4MLvG28'
  ./cloudsend.sh -g -p 'MySecretPass' '{file1,file2,file3}' 'https://cloud.mydomain.net/s/fLDzToZF4MLvG28'
  cat file | ./cloudsend.sh - 'https://cloud.mydomain.net/s/fLDzToZF4MLvG28' -r destFileName

"
}





################################################################
#### GET OPTIONS
################################################################


# Checks only for quiet/verbose mode and ignores all else
parseQuietMode(){
        while :; do
                case "$1" in
                        -h|--help)
                                usage ; exit 0 ;;
                        -V|--version)
                                printVersion ; exit 0 ;;
                        -q|--quiet)
                                QUIETMODE=$TRUE
                                VERBOSE=" -s" ; break ;;
                        *)
                                isEmpty "$1" && break || shift ;;
                esac
        done

}


# Parses CLI options and parameters
parseOptions() {
        log "Tavinus Cloud Sender v$CS_VERSION"$'\n'
        while :; do
                case "$1" in
                        -q|--quiet)
                                shift ;; # already checked
                        -k|--insecure)
                                INSECURE=' -k'
                                log "> Insecure mode ON"
                                shift ;;
                        -e|--envpass|--environment)
                                loadPassword "${CLOUDSEND_PASSWORD}"
                                log "> Using password from environment"
                                shift ;;
                        -p|--password)
                                loadPassword "$2"
                                log "> Using password from parameter"
                                shift ; shift ;;
                        -r|--rename)
                                loadOutFile "${2}"
                                log "> Destination file will be renamed to \"$OUTFILE\""
                                RENAMING=$TRUE
                                shift ; shift ;;
                        -g|--glob)
                                GLOBBING=$TRUE
                                GLOBCMD=''
                                log "> Glob mode ON, input file checkings disabled"
                                shift ;;
                        -a|--abort-on-errors)
                                ABORTONERRORS=$TRUE
                                log "> Abort on errors ON, will stop execution on DAV errors"
                                shift ;;
                        -l|--limit-rate)
                                loadLimit "${2}"
                                LIMITTING=$TRUE
                                log "> Rate limit set to $RATELIMIT"
                                shift ; shift ;;
                                
                        *)
                                if isEmpty "$1"; then
                                        break ;
                                else
                                        CLOUDSEND_PARAMS=("${CLOUDSEND_PARAMS[@]}" "$1")
                                        shift ;
                                fi
                                        
                esac
        done
        
        CLOUDURL=''
        FILENAME="${CLOUDSEND_PARAMS[0]}"
        CLOUDSHARE="${CLOUDSEND_PARAMS[1]}"

        # if we have index.php in the URL, process accordingly
        if [[ "$CLOUDSHARE" == *"index.php"* ]]; then
                CLOUDURL="${CLOUDSHARE%/index.php/s/*}"
        else
                CLOUDURL="${CLOUDSHARE%/s/*}"
        fi

        # get token and sub folder
        FOLDERTOKEN="${CLOUDSHARE##*/s/}"
        INNERPATH="${FOLDERTOKEN##*\?path=}"
        FOLDERTOKEN="${FOLDERTOKEN%\?*}"
        
        if [[ "$FOLDERTOKEN" == "$INNERPATH" ]]; then
                INNERPATH=""
        else
                INNERPATH="$(decodeSlash "$INNERPATH")"
        fi

        
        if isGlobbing; then
                if isRenaming; then
                        initError $'Cannot rename output files when using globbing on input.\nAll files would get the same output name and then be overwritten.\nSend individual files if you need renaming.'
                elif isPiped "$FILENAME"; then
                        initError $'Cannot use globbing and send piped input at the same time.\nDo either one or the other.'
                fi
        else
                if ! isFile "$FILENAME" && ! isDir "$FILENAME" && ! isPiped "$FILENAME"; then
                        initError "Invalid input file/folder: $FILENAME"
                fi

                if isPiped "$FILENAME" && ! isRenaming; then
                        initError $'No output file name!\nYou need to set a destination name when reading from a pipe!\nPlease add -r <filename.ext> to your call.'
                fi
        fi

        if isEmpty "$CLOUDURL"; then
                initError "Empty URL! Nowhere to send..."
        fi

        if isEmpty "$FOLDERTOKEN"; then
                initError "Empty Folder Token! Nowhere to send..."
        fi
        log ''
}

# Parses Rate limitting
loadLimit() {
        if [ -z "$@" ]; then
                initError "Trying to set an empty rate limit"
        fi
        RATELIMIT="$@"
        LIMITCMD=' --limit-rate '"$RATELIMIT"
}


# Parses password to var or exits
loadPassword() {
        if [ -z "$@" ]; then
                initError "Trying to set an empty password"
        fi
        PASSWORD="$@"
}


# Parses destination file name to var or exits
loadOutFile() {
        if [ -z "$@" ]; then
                initError "Trying to set an empty destination file name"
        fi
        OUTFILE="$@"
}





################################################################
#### VALIDATORS
################################################################


# Dependency check
checkCurl() {
        CURLBIN="$(command -v curl 2>/dev/null)"
        isExecutable "$CURLBIN" && return $TRUE
        CURLBIN='/usr/bin/curl'
        isExecutable "$CURLBIN" && return $TRUE
        CURLBIN='/usr/local/bin/curl'
        isExecutable "$CURLBIN" && return $TRUE
        CURLBIN='/usr/share/curl'
        isExecutable "$CURLBIN" && return $TRUE
        initError "No curl found on system! Please install curl and try again!"
        exit 6
}


# Adjust Columns so the progess bar shows correctly
# Curl "space bar" has bugs that only show in special cases,
# depending on the column size of the terminal. I had lots
# of problems with this spanning multiple lines, so I fixed it
# with a max of 80 columns if it is bigger (seems to solve).
# https://github.com/curl/curl/issues/4849
getScreenSize() {
        if isExecutable "$STTYBIN"; then
                SCREENSIZE="$($STTYBIN size)"
        fi
        #export LINES=${SCREENSIZE% *}
        #export COLUMNS=$((${SCREENSIZE#* } - 1))
        COLUMNS=${SCREENSIZE#* }
        ((COLUMNS=COLUMNS-1))
        [[ $COLUMNS -gt 80 ]] && COLUMNS=80
        export COLUMNS
        #export COLUMNS=50
        #echo "LINES..: $LINES"
        #echo "COLUMNS: $COLUMNS"
}


# Returns $TRUE if $1 is a file, $FALSE otherwise
isFile() {
        [[ -f "$1" ]] && return $TRUE
        return $FALSE
}


# Returns $TRUE if $1 is a directory, $FALSE otherwise
isDir() {
        [[ -d "$1" ]] && return $TRUE
        return $FALSE
}


# Returns $TRUE if $1 is executable, $FALSE otherwise
isExecutable() {
        [[ -x "$1" ]] && return $TRUE
        return $FALSE
}


# Returns $TRUE if $1 is empty, $FALSE otherwise
isEmpty() {
        [[ -z "$1" ]] && return $TRUE
        return $FALSE
}


# Returns $TRUE if $1 is not empty, $FALSE otherwise
isNotEmpty() {
        [[ -z "$1" ]] && return $FALSE
        return $TRUE
}


# Checks if the input file is stdin (either - or .)
isPiped() {
        if [ "$1" = '-' ] || [ "$1" = '.' ] ; then
                return $TRUE
        fi
        return $FALSE        
}





################################################################
#### FLAG CHECKERS
################################################################


# If we are renaming the output, return $TRUE, else $FALSE
isRenaming() {
        return $RENAMING
}


# If we are running in Quiet Mode, return $TRUE, else $FALSE
isQuietMode() {
        return $QUIETMODE
}


# If we are globbing the input, return $TRUE, else $FALSE
isGlobbing() {
        return $GLOBBING
}


# If we should abort when curl returns a XML response, return $TRUE, else $FALSE
abortOnDavErrors() {
        return $ABORTONERRORS
}


# If have a dav error, return $TRUE, else $FALSE
hasDavErrors() {
        isEmpty "$CURLRESPONSES" && return $FALSE
        return $TRUE
}


# If have a dav error, return $TRUE, else $FALSE
checkAbort() {
        abortOnDavErrors && hasDavErrors && logResult
}





################################################################
#### HELPER FUNCTIONS


# encode URL escaping
rawUrlEncode() {
        local string="${1}"
        local strlen=${#string}
        local encoded=""
        local pos c o

        for (( pos=0 ; pos<strlen ; pos++ )); do
                c=${string:$pos:1}
                case "$c" in
                        [-_.~a-zA-Z0-9] ) o="${c}" ;;
                        * )               printf -v o '%%%02x' "'$c"
                esac
                encoded+="${o}"
        done
        echo "${encoded}"    # You can either set a return variable (FASTER) 
        REPLY="${encoded}"   #+or echo the result (EASIER)... or both... :p
}

# Escape specific chars needed
escapeChars() {
        local string="${1}"
        local strlen=${#string}
        local encoded=""
        local pos c o

        for (( pos=0 ; pos<strlen ; pos++ )); do
                c=${string:$pos:1}
                case "$c" in
                        " " ) o='%20' ;;
                        '#' ) o='%23' ;;
                        * ) o="${c}" ;;
                esac
                encoded+="${o}"
        done
        echo "${encoded}"    # You can either set a return variable (FASTER) 
        #REPLY="${encoded}"   #+or echo the result (EASIER)... or both... :p

}


# Decode '%2F' into '/'
decodeSlash() {
	isEmpty "$1" && return 9
	echo "$(echo "$1" | sed 's/\%2f/\//g' | sed 's/\%2F/\//g')"
}




################################################################
#### RUNNERS
################################################################


# Create a directory with -X MKCOL
# PROBABLY NEED TO ESCAPE WHITE SPACES OR ESCAPE ALL TO HTML CHARS
createDir() {
        isEmpty "$1" && initError 'Error! Cannot create folder with empty name.'
        getScreenSize
        logSameLine "$1 > "
        eout="$(escapeChars "$1")"
        #echo "$CURLBIN"$INSECURE --silent -X MKCOL -u "$FOLDERTOKEN":"$PASSWORD" -H "$HEADER" "$CLOUDURL/$PUBSUFFIX$INNERPATH/$1" 
        cstat="$(createDirRun "$eout" 2>&1)"
        #echo " -- $cstat"
        if ! isEmpty "$cstat"; then
                curlAddResponse "$cstat" "Send Folder: \"$eout\""
                msg="$(echo "$cstat" | grep '<s:message>' | sed -e 's/<[^>]*>//g' -e 's/^[[:space:]]*//')"
                isEmpty "$msg" && msg="$(echo "$cstat" | grep '<s:exception>' | sed -e 's/<[^>]*>//g' -e 's/^[[:space:]]*//')"
                log "$msg"
        else
                log 'OK'
        fi
        checkAbort # exits if DAV errors AND not ignoring them
}


# Create a directory with -X MKCOL
createDirRun() {
        "$CURLBIN"$INSECURE --silent -X MKCOL -u "$FOLDERTOKEN":"$PASSWORD" -H "$HEADER" "$CLOUDURL/$PUBSUFFIX$INNERPATH/$1" | cat ; test ${PIPESTATUS[0]} -eq 0
        ecode=$?
        curlAddExitCode $ecode
        return $ecode
}


# Traverse a folder and send its files and subfolders
sendDir() {
        isEmpty "$FILENAME" && initError 'Error! Cannot send folder with empty name.'
        isDir "$FILENAME" || initError 'Error! sendFolder() > "'"$FILENAME"'" is not a Folder.'

        # Load lists of folders and files to be sent
        DIRLIST=()
        FILELIST=()
        readarray -t DIRLIST < <(find "$FILENAME" -type d -printf '%P\n')
        readarray -t FILELIST < <(find "$FILENAME" -type f -printf '%P\n')
        #echo '<<DIRLIST>>' ; echo "${DIRLIST[@]}" ; echo '<<FILELIST>>' ; echo "${FILELIST[@]}"

        fbn="$("$BASENAMEBIN" "$FILENAME")"

        # MacOS / BSD readlink does not have the -f option
        # Get bash implementation from pdfScale.sh if needed
        # For now PWD seems to be enough
        if [[ "$fbn" == '.' ]]; then 
                fbn="$PWD"
                fbn="$("$BASENAMEBIN" "$fbn")"
        fi

        log "CREATING FOLDER TREE AT DESTINATION"$'\n'"==================================="$'\n'

        # Create main/root folder that is being sent
        createDir "$fbn"
        
        # Create whole directory tree at destination
        for d in "${DIRLIST[@]}"; do
                if ! isEmpty "$d"; then
                        createDir "$fbn/$d"
                fi
        done

        log $'\n'"SENDING ALL FILES FROM FOLDER TREE"$'\n'"=================================="$'\n'
        
        # Send all files to their destinations
        for f in "${FILELIST[@]}"; do 
                if ! isEmpty "$f"; then
                        OUTFILE="$fbn/$f"
                        log "$OUTFILE > "
                        sendFile "$FILENAME/$f"
                fi
        done

}


# Logs succes or failure from curl
logResult() {
        #echo "LOGRESULT: $1"
        local fileString="$("$BASENAMEBIN" "$FILENAME")"
        isRenaming && fileString="$("$BASENAMEBIN" "$FILENAME") (renamed as $OUTFILE)"
        log $'\n'"SUMMARY"$'\n'"======="$'\n'
                  
        if [ $CURLEXIT -eq 0 ]; then
                if isEmpty "$CURLRESPONSES"; then
                        log " > All Curl calls exited without errors and no WebDAV errors were detected"$'\n'" > Attempt to send completed > $fileString"
                else
                        log " > All Curl calls exited without errors, but webdav errors"$'\n'"   were detected while trying to send $fileString"$'\n\n'"Curl Log:"$'\n'"$CURLRESPONSES"
                fi
                exit 0
        fi
        log " > Curl execution errors were detected when sending > $fileString"$'\n'" > Summed Curl exit codes: $CURLEXIT"
        exit $CURLEXIT
}


# Execute curl send
sendFile() {
        if isGlobbing; then
                OUTFILE=''
        elif isEmpty "$OUTFILE"; then # If we are not renaming, use the input file name
                OUTFILE="$("$BASENAMEBIN" "$1")"
        fi
        
        getScreenSize
        eout="$(escapeChars "$OUTFILE")"
        # Send file
        #echo "$CURLBIN"$INSECURE$VERBOSE -T \""$1"\" -u \""$FOLDERTOKEN":"$PASSWORD"\" -H \""$HEADER"\" \""$CLOUDURL/$PUBSUFFIX$INNERPATH/$eout"\"
        #"$CURLBIN"$LIMITCMD$INSECURE$VERBOSE$GLOBCMD -T "$1" -u "$FOLDERTOKEN":"$PASSWORD" -H "$HEADER" "$CLOUDURL/$PUBSUFFIX$INNERPATH/$eout" | cat ; test ${PIPESTATUS[0]} -eq 0
        resp="$("$CURLBIN"$LIMITCMD$INSECURE$VERBOSE$GLOBCMD -T "$1" -u "$FOLDERTOKEN":"$PASSWORD" -H "$HEADER" "$CLOUDURL/$PUBSUFFIX$INNERPATH/$eout")"
        stat=$?
        curlAddResponse "$resp" "Send File: \"$eout\""
        curlAddExitCode $stat
        checkAbort # exits if DAV errors AND not ignoring them
}


# Send Files and Folders
sendItems() {
        if ! isGlobbing && isDir "$FILENAME"; then
                sendDir
        else
                if isGlobbing; then
                        log "SENDING CURL GLOB"$'\n'"================="$'\n'
                        log "$FILENAME > "
                else
                        log "SENDING SINGLE FILE"$'\n'"==================="$'\n'
                        log "$("$BASENAMEBIN" "$FILENAME") > "
                fi
                sendFile "$FILENAME"
        fi
}





################################################################
#### RUN #######################################################
################################################################
parseQuietMode "${@}"
parseOptions "${@}"
checkCurl
sendItems
logResult
################################################################
#### RUN #######################################################
################################################################






################################################################
exit 88 ; # should never get here
################################################################
