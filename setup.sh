#!/bin/bash
rm -f ./deploy.zip
zip -r ./deploy.zip $ZIPFOLDER -x ./.git\* ./.vscode\* ./deploy\*

az webapp config appsettings set -g "$AZRGNAME" -n "$AZAPPNAME" --settings "SCM_DO_BUILD_DURING_DEPLOYMENT=true" "AZTENANTID=$AZTENANTID" "AZAPPID=$AZAPPID"
if [ ! -z "$BUILDTAG" ]; then
    az webapp config appsettings set -g "$AZRGNAME" -n "$AZAPPNAME" --settings "BUILDTAG=$BUILDTAG"
fi
az webapp deployment source config-zip -g "$AZRGNAME" -n "$AZAPPNAME" --src ./deploy.zip