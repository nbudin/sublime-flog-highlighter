import sublime, sublime_plugin, subprocess, os, json, threading, traceback

class FlogOnSave(sublime_plugin.EventListener):
  def on_post_save(self, view):
    if view.file_name()[-3:] == '.rb':
      view.run_command('flog_highlighter')

def show_errors(window, errors, edit):
  report_panel = window.get_output_panel('flog_highlighter_error_messages')
  report_panel.insert(edit, 0, errors)
  window.run_command('show_panel', { 'panel': 'output.flog_highlighter_error_messages' })

class FlogHighlighterCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    try:
      script_name = os.path.join(sublime.packages_path(), 'sublime-flog-highlighter', 'flog_formatter.rb')
      popen = subprocess.Popen([script_name, self.view.file_name()], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      popen.wait()

      if popen.returncode == 0:
        notes = json.loads(popen.stdout.read().decode())
        if len(notes) == 0:
          return

        entire_file = sublime.Region(0, self.view.size())
        lines = self.view.split_by_newlines(entire_file)

        regions = {
          'note': [],
          'warning': [],
          'error': []
        }
        for note in notes:
          line = lines[int(note['line']) - 1]
          regions[note['level']].append(line)

        self.view.add_regions('flog_highlighter_note', regions['note'], 'string', 'bookmark', sublime.DRAW_OUTLINED)
        self.view.add_regions('flog_highlighter_warning', regions['warning'], 'invalid.illegal', 'bookmark', sublime.DRAW_OUTLINED)
        self.view.add_regions('flog_highlighter_error', regions['error'], 'invalid.illegal', 'bookmark')
      else:
        show_errors(self.view.window(), "Flog output:\n\n" + popen.stdout.read().decode('utf-8') + popen.stderr.read().decode('utf-8'), edit)
    except Exception as e:
      show_errors(self.view.window(), traceback.format_exc(), edit)

class FlogReportCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    try:
      popen = subprocess.Popen(['flog', '-d', self.view.file_name()], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      popen.wait()

      if popen.returncode == 0:
        report_panel = self.view.window().get_output_panel('flog_report')
        report_panel.insert(edit, 0, popen.stdout.read().decode())
        self.view.window().run_command('show_panel', { 'panel': 'output.flog_report' })
      else:
        show_errors(self.view.window(), self.popen.stderr.read(), edit)
    except Exception as e:
      show_errors(self.view.window(), traceback.format_exc(), edit)