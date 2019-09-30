#!/bin/bash 

day="$(date "+%Y-%m-%d-")"
title="$1"
ftitle="$day""${title// /_}"".md"
file="_posts/""$ftitle"
# touch "$file"

cat << EOF > "$file"
---
layout: post
title: ${title}
author:
category: 
tags: []
--- 

# ${title}

EOF

exec "$EDITOR" "$file"

