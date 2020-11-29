#!/usr/bin/env python3
# Copyright 2020 The Emscripten Authors.  All rights reserved.
# Emscripten is available under two separate licenses, the MIT license and the
# University of Illinois/NCSA Open Source License.  Both these licenses can be
# found in the LICENSE file.

import os
import sys
import shutil
import subprocess

script_dir = os.path.abspath(os.path.dirname(__file__))
local_src = os.path.join(script_dir, 'libc', 'musl')
local_inc = os.path.join(os.path.dirname(script_dir), 'include', 'libc')
exclude_dirs = (
  # Top level directories we don't include
  'tools', 'obj', 'lib', 'arch', 'crt', 'musl',
  # Parts of src we don't build
  'fenv', 'compat',
  # Arch-specific code we don't use
  'arm', 'x32', 'sh', 'i386', 'x86_64', 'aarch64', 'riscv64',
  's390x', 'mips', 'mips64', 'mipsn32', 'powerpc', 'powerpc64',
  'm68k', 'microblaze', 'or1k')


musl_dir = os.path.abspath(sys.argv[1])
musl_inc = os.path.join(musl_dir, 'include')


def should_ignore(name):
  return name in exclude_dirs or name[0] == '.'


def ignore(dirname, contents):
  rtn = [c for c in contents if should_ignore(c)]
  if dirname == musl_dir:
    rtn += [c for c in contents if c in ['include']]
  return rtn


def main():
  assert os.path.exists(musl_dir)
  assert os.path.exists(musl_inc)

  # Remove old version
  shutil.rmtree(local_src)
  shutil.rmtree(local_inc)

  # Copy new version into place
  shutil.copytree(musl_dir, local_src, ignore=ignore)
  shutil.copytree(musl_inc, local_inc, ignore=ignore)

  # restore emscipten-specific header tree
  subprocess.run(['git', 'checkout', f'{local_src}/arch/emscripten'])

if __name__ == '__main__':
  main()
