on run {daemon_file, agent_file, user, cur_pid, source_dir}

  set unload_service to "launchctl unload -w /Library/LaunchDaemons/com.carriez.xldesk_service.plist || true;"

  set kill_others to "pgrep -x 'xldesk' | grep -v " & cur_pid & " | xargs kill -9;"

  set copy_files to "rm -rf /Applications/xldesk.app && ditto " & source_dir & " /Applications/xldesk.app && chown -R " & quoted form of user & ":staff /Applications/xldesk.app && xattr -r -d com.apple.quarantine /Applications/xldesk.app;"

  set sh1 to "echo " & quoted form of daemon_file & " > /Library/LaunchDaemons/com.carriez.xldesk_service.plist && chown root:wheel /Library/LaunchDaemons/com.carriez.xldesk_service.plist;"

  set sh2 to "echo " & quoted form of agent_file & " > /Library/LaunchAgents/com.carriez.xldesk_server.plist && chown root:wheel /Library/LaunchAgents/com.carriez.xldesk_server.plist;"

  set sh3 to "launchctl load -w /Library/LaunchDaemons/com.carriez.xldesk_service.plist;"

  set sh to unload_service & kill_others & copy_files & sh1 & sh2 & sh3

  do shell script sh with prompt "xldesk wants to update itself" with administrator privileges
end run
