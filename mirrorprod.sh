#!/bin/sh

/opt/local/lib/postgresql92/bin/dropdb ballroomcms
/opt/local/lib/postgresql92/bin/createdb ballroomcms

rsync --delete -r adam@tigger.peacockhosting.net:/var/www/uconnballroom.com/data/cms_user_media/* /Users/adam/development/ballroom/ballroomcms/user_media/

ssh adam@tigger.peacockhosting.net 'pg_dump ballroomcms' | /opt/local/lib/postgresql92/bin/psql ballroomcms