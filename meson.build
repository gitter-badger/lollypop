project('lollypop',
  version: '0.9.244',
  meson_version: '>= 0.40.0'
)
i18n = import('i18n')
python = import('python3')
project_id = 'org.gnome.Lollypop'

message('Looking for dependencies')
python_bin = python.find_python()
if not python_bin.found()
    error('No valid python3 binary found')
else
    message('Found python3 binary')
endif
dependency('glib-2.0')
dependency('gobject-introspection-1.0', version: '>=1.35.9')
dependency('gtk+-3.0', version :'>=3.14')

python_dir = join_paths(get_option('prefix'), python.sysconfig_path('purelib'))
LIBEXEC_DIR = join_paths(get_option('prefix'), get_option('libexecdir'))
DATA_DIR = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
bindir = join_paths(get_option('prefix'), get_option('bindir'))

conf = configuration_data()
conf.set('PACKAGE_URL', 'https://github.com/gnumdk/lollypop')
conf.set('DATA_DIR', DATA_DIR)
conf.set('LOCALE_DIR', join_paths(get_option('prefix'), get_option('datadir'), 'locale'))
conf.set('PYTHON_DIR', python_dir)
conf.set('PYTHON_EXEC_DIR', join_paths(get_option('prefix'), python.sysconfig_path('stdlib')))
conf.set('libexecdir', LIBEXEC_DIR)
conf.set('VERSION', meson.project_version())
conf.set('PYTHON', python_bin.path())

subdir('data')
subproject('po')
subproject('help')
subdir('search-provider')

install_subdir(
  'lollypop',
  install_dir: python_dir
)

install_subdir(
  'thirdparty',
  install_dir: join_paths(python_dir, 'lollypop')
)

message('Preparing init file')
configure_file(
  input: 'lollypop.in',
  output: 'lollypop',
  configuration: conf,
  install_dir: bindir
)

configure_file(
  input: 'lollypop-cli.in',
  output: 'lollypop-cli',
  configuration: conf,
  install_dir: bindir
)

meson.add_install_script('meson_post_install.py')
