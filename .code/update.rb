#!/usr/bin/env ruby -w

require 'open-uri'

def say(message)
  puts message
  message
end

def sh(*args)
  command = args.join(' ')
  debug("$ #{command}")
  stdout = `#{command}`
  debug(stdout)
  stdout
end

def debug(message)
  say message if DEBUG
end


TLDFILE = File.expand_path('../../.tmp/tlds.txt', __FILE__)
DEBUG   = true
DATE    = Time.now.strftime('%Y-%m-%d')

sh "git pull origin master"

File.open(TLDFILE, "w+") { |f| f.write(open('https://data.iana.org/TLD/tlds-alpha-by-domain.txt').read) }
if File.read(TLDFILE).empty?
  abort("TLD list is empty")
end

stored_tlds = Dir.glob("[A-Z0-9]*").to_a
active_tlds = File.read(TLDFILE).split("\n").select { |line| line =~ /^[A-Z0-9]+/ }

removed_tlds = stored_tlds - active_tlds
removed_tlds.each do |tld|
  message = "Delete #{tld} (#{DATE})"
  sh "git rm #{tld}"
  sh "git add #{tld}"
  sh "git commit -m '#{message}'"
end

active_tlds.each do |tld|
  newtld = !File.exist?(tld)
  message = newtld ? "Create #{tld} (#{DATE})" : "Update #{tld} (#{DATE})"

  sh "touch #{tld}"
  sh "whois -h whois.iana.org #{tld} > #{tld}"

  # reset invalid updates
  if File.size(tld) == 0
    sh "git checkout #{tld}"
  end

  status = sh "git status -s"
  unless status.empty?
    sh "git add #{tld}"
    sh "git commit -m '#{message}'"
  end

  sleep(3)
end

sh "git push origin master"

