# BFDebug

A graphical front-end for LLDB and GDB.

# Requirements

Requires Python, and one of the following command line tools: `gdb`, `lldb-dap`, `lldb-dap-20`, or `lldb-dap` runnable through Xcode (`xcrun lldb-dap`).

Your executable must also be compiled with debug information (`-g` in `gcc` and `clang`).

# How to use

Select your executable with `Load EXE`. Select a source file with `Load Source`. If you run the program now, it will continue executing until the
program terminates. To pause execution before termination, you can set a breakpoint (a point where execution will pause) by selecting a line in the
source, and clicking `Set breakpoint`. When the breakpoint is hit, you can inspect the local variables, and go step by step through the code, or continue
until the breakpoint is hit next.
