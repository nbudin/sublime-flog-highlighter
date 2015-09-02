#!/usr/bin/env ruby

require 'flog'
require 'json'

COMPLEXITY_THRESHOLDS = {
  note: 25,
  warning: 50,
  error: 100
}

filepath = ARGV.first

begin
  flog = Flog.new(quiet: true, continue: true, all: true)
  flog.flog filepath

  line_notes = []
  
  flog.each_by_score do |class_method, score, call_list|
    level, _ = COMPLEXITY_THRESHOLDS.select { |_, threshold| threshold <= score }.max_by { |_, threshold| threshold }
    next unless level
    
    location = flog.method_locations[class_method]
    line = location && location.gsub(/.*:/, '')

    if line
      message = "#{class_method} complexity: %0.2f" % [score]

      line_notes << {
        line: line,
        level: level,
        message: message
      }
    end
  end

  puts line_notes.to_json
rescue Racc::ParseError
  STDERR.puts "Parse error"
  exit false
rescue Exception => e
  STDERR.puts "Error while running Flog:\n#{e.class.name} - #{e.message}"
  exit false
end