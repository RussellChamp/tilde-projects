require 'rss'
require 'open-uri'

latestFile = "latest.txt"

latest = File.open(latestFile, "r").read if File::exists?(latestFile)
url = 'http://www.musicforprogramming.net/rss.php'
open(url) do |rss|
  feed = RSS::Parser.parse(rss)
#  puts "Title: #{feed.channel.title}"
#  puts "Comparing latest with feed"
#  puts "#{latest} -- #{feed.items[0].title}"

  if latest != feed.items[0].title then
    puts "Item #{feed.items[0].title} -- #{feed.items[0].guid}"
    File.open(latestFile, 'w') do |file|
      file.write(feed.items[0].title)
    end
  end
end
