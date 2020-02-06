#!/bin/bash
while [[ $# -gt 0 ]]
do
    case "$1" in
        -g|--resource-group)
            AZRGNAME="$2"
            shift 2
            ;;
        -l|--location)
            AZLOCATION="$2"
            shift 2
            ;;
        -n|-n)
            AZAPPNAME="$2"
            shift 2
            ;;
        -p|--plan)
            AZAPPPLAN="$2"
            shift 2
            ;;
        -t|--tenantid)
            AZTENANTID="$2"
            shift 2
            ;;
        -a|--appid)
            AZAPPID="$2"
            shift 2
            ;;
        -z|--zipfolder)
            ZIPFOLDER="$2"
            shift 2
            ;;
        -b|--buildtag)
            BUILDTAG="$2"  
            shift 2
            ;;
    esac
done

echo "RG=$AZRGNAME, LOCATION=$AZLOCATION, PLAN=$AZAPPPLAN, APP=$AZAPPNAME, ZIPFOLDER=$ZIPFOLDER, tenantid=$AZTENANTID, AppID=$AZAPPID, BuildTag=$BUILDTAG"

rm -f ./deploy.zip
zip -r ./deploy.zip $ZIPFOLDER -x ./.git\* ./.vscode\* ./deploy\*

az webapp config appsettings set -g "$AZRGNAME" -n "$AZAPPNAME" --settings "SCM_DO_BUILD_DURING_DEPLOYMENT=true" "AZTENANTID=$AZTENANTID" "AZAPPID=$AZAPPID"
if [ ! -z "$BUILDTAG" ]; then
    az webapp config appsettings set -g "$AZRGNAME" -n "$AZAPPNAME" --settings "BUILDTAG=$BUILDTAG"
fi
az webapp deployment source config-zip -g "$AZRGNAME" -n "$AZAPPNAME" --src ./deploy.zip