#! /usr/bin/env python3

import argparse, base64, os, platform, re, subprocess

def create_parser(version_required=False):
  parser = argparse.ArgumentParser()
  parser.add_argument('--build-type', default='Release')
  parser.add_argument('--version', required=version_required)
  parser.add_argument('--classifier')
  parser.add_argument('--system')
  parser.add_argument('--machine')
  parser.add_argument('--ndk')
  parser.add_argument('--gcc-version', default='9')
  return parser

def system():
  parser = create_parser()
  (args, _) = parser.parse_known_args()
  return args.system if args.system else {'Darwin': 'macos', 'Linux': 'linux', 'Windows': 'windows'}[platform.system()]

def native_machine():
  return {
    'AMD64': 'x64', 'x86_64': 'x64',
    'arm64': 'arm64', 'aarch64': 'arm64',
    'riscv64': 'riscv64'
  }[platform.machine()]

def machine():
  parser = create_parser()
  (args, _) = parser.parse_known_args()
  return args.machine if args.machine else native_machine()

def target_triplet():
  if (system() == 'linux'):
    return {
      'x64': 'x86_64-linux-gnu',
      'arm64': 'aarch64-linux-gnu',
      'riscv64': 'riscv64-linux-gnu'
    }.get(machine(), '')
  else:
    return ''

def version():
  parser = create_parser()
  args = parser.parse_args()

  if args.version:
    return args.version

  branches = subprocess.check_output(['git', 'branch', '--contains', 'HEAD']).decode('utf-8')
  for match in re.finditer('chrome/(m\\d+)', branches):
    version = match.group(1)
  revision = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('utf-8')
  return version + '-' + revision.strip()[:10]

def build_type():
  parser = create_parser()
  (args, _) = parser.parse_known_args()
  return args.build_type

def classifier():
  parser = create_parser()
  (args, _) = parser.parse_known_args()
  return '-' + args.classifier if args.classifier else ''

def github_headers():
  if os.environ.get('GITHUB_BASIC'):
    auth = 'Basic ' + base64.b64encode(os.environ.get('GITHUB_BASIC').encode('utf-8')).decode('utf-8')
  else:
    auth = 'token ' + os.environ.get('API_TOKEN')
  return {
    'Accept': 'application/vnd.github.v3+json',
    'Authorization': auth
  }

def ndk():
  parser = create_parser()
  (args, _) = parser.parse_known_args()
  return args.ndk if args.ndk else ''

def gcc_version():
  parser = create_parser()
  (args, _) = parser.parse_known_args()
  return args.gcc_version
