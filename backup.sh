#!/bin/bash

DB_FILE=$(realpath ~/sistema-reportes-ambulancias/db.sqlite3)
DEST_LOC=$(realpath ~/backups/)
CURRENT_DATE=$(date +'%Y-%m-%d_%H_%M_%S')

cp "$DB_FILE" "$DEST_LOC/db_backup_$CURRENT_DATE.sqlite3"
echo "Backup created successfully, at: $CURRENT_DATE"
