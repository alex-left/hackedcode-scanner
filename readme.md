# HACKEDCODE SCANNER
python pluggable application to scan a project code to find posible hints of hacking

## REQUIREMENTS
python >= 3.3

Tested in gnu-linux systems, but should work in others POSIX systems.
Maybe works in Windows, but really, don't use Windows.

## USAGE:
```
usage: hackedcode-scanner.py [-h] [-c CONFIG] [-l LEVEL] path

Scan app project and find hints of possible hacking

positional arguments:
  path                  Path of the root of the app's project

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        path of a configuration yaml file
  -l LEVEL, --level LEVEL
                        level of output
```

#### How works:
The app scan all files of the source code with the plugins defined in a yaml configuration file.
The point is detect posible hints of hacking in your production servers, particulary in php projects.  This app doesn't make any analysis of vulnerabilites (you can do a plugin for that!). Each plugin haves their own rules. You can have
multiple yaml files to scan multiples projects in the same machine.

#### Examples:
```
$ hackedcode-scanner.py -c myproject-config.yml /path-of-myproject
```

## HOW INSTALL

1. clone the project:
```
git clone
```

2. Move to the code folder
```
cd hackedcode-scanner
```

3. You can use the app directly from source code (needs pyyaml library)
```
python3 hackedcode_scanner/main.py -c myproject-config.yml /path-of-myproject
```

4. Or you can install it with pip
```
sudo pip3 install .
```

## Plugins available
- **shell**: scan the content of files to search regex expressions. Intended to find
shebangs or strings like calls to "/bin/sh" but you can define any regex expressions.

- **git**: git can be a useful tool if is used to deploy or versioning the code in the server.
Since git can do a effiently supervision of all files, you can use it to detect
anomalies. This plugin run a "git status" and raises all results.

- **extensions**: You can scan all filenames and detect if any haves a ilegal extension

- **perms**: no file of you code should have execution permissions. This plugin scan it.

## HOW USAGE:

The behavior of the scanner is defined in a yaml config file. The default configuration contains
the rules for a drupal project. Each plugin haves his own config into key: "plugins_config.name-of-plugin". By default, the plugins try to scan all files and you must to define the exceptions, this key are common to all plugins:

- **excluded_files**: A list with files (glob supported) that should be ignored by the plugin

Some plugins have specifically configuration:

- **shell.patterns**: a list of regex expressions to find into the code

The "extensions" plugin works in inverse mode: you must define what files/paths should be scanned and which extensions should be matched:
```
  extensions:
    target_paths:
    - "sync/"
    - "sites/*/files/*"
    target_extensions:
    - '.sh'
    - '.php'
    - '.py'
```

This is the default config yaml:
```
# The default config file is based on a criteria for a Drupal project

# enable a log file
log_enabled: no
log_path: "hackedcode-scanner.log"

# the names of the enabled plugins
plugins_enabled:
  - git
  - shell
  - perms

plugin_config:
  git:
    excluded_files: []
  shell:
    excluded_files:
    - modules/
    - core/scripts/
    - ".git/"
    patterns:
    - '(/usr|/usr/local)?/bin/(ba|da|z|t|tc)?sh ?'
    - ' [A-Za-z0-9 _\-.]+\.sh '
  perms:
    excluded_files:
    - ".git/"
    - "vendor/"
    - core/scripts/
  extensions:
    target_paths:
    - "sync/"
    - "sites/*/files/*"
    target_extensions:
    - '.sh'
    - '.php'
    - '.py'
    excluded_paths:
    - sync/php/twig/*
```

## Plugin Development
By default, main program try to move to the root of the project path
(mandatory argument of the scanner) and later try to import all files in plugins
folder with the same name as are defined in the list "plugins_enabled" in the yaml
config. The main program will run a callable with name: "run_plugin(plugin_config)",
so your plugin just should accomplish this requirement.
This callable act like main function of the plugin and the parameter "plugin_config"
is the dictionary defined in "plugin_config" with the key with the same name of the plugin.
Also, is recommended import and use the "logging" library.

You can put your plugin directly in ./plugins folder of the source code if you use it from there
or into default python path, usually in /usr/local/lib/[python]/dist-packages/ (in a wide-system instalation)

## TODO
- load plugins and config files from alternatives paths.
